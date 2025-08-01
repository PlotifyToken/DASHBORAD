import json
from http.server import BaseHTTPRequestHandler
import requests
from datetime import datetime, timezone
import os

def format_number(num):
    """
    将大数字格式化为K/M形式
    例如: 144048 -> $144K, 1200000 -> $1.2M
    """
    if isinstance(num, str):
        return num
    
    if num >= 1000000:
        return f"${num/1000000:.1f}M"
    elif num >= 1000:
        return f"${num/1000:.0f}K"
    else:
        return f"${num:,.0f}"

def format_count(num):
    """
    将数量格式化为K/M形式（不带$符号）
    例如: 12400 -> 12.4K, 1200000 -> 1.2M
    """
    if isinstance(num, str):
        return num
    
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return f"{num:,}"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 从环境变量获取API密钥
            customer_io_app_api_key = os.environ.get('CUSTOMER_IO_APP_API_KEY')
            revenuecat_token = os.environ.get('REVENUECAT_TOKEN')
            
            if not customer_io_app_api_key or not revenuecat_token:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "API keys not configured"}).encode())
                return
            
            # 获取Customer.io数据
            cio_data = self.get_customer_io_data(customer_io_app_api_key)
            
            # 获取RevenueCat数据
            rc_data = self.get_revenuecat_data(revenuecat_token)
            
            # 组合响应数据
            total_users = cio_data.get("total_customers", 0)
            arr_value = rc_data.get("arr", 0)
            active_subs = rc_data.get("active_subscriptions", 0)
            
            # 基础增量值
            BASE_USER_INCREMENT = 11000
            BASE_ARR_INCREMENT = 141600.0
            BASE_SUBS_INCREMENT = 118
            
            # 如果获取到真实数据，添加基础增量
            cio_source = cio_data.get("source", "unknown")
            rc_source = rc_data.get("source", "unknown")
            
            # 只有在获取到真实数据时才添加增量（避免在API失败的基础值上重复添加）
            if cio_source not in ["api_failed", "api_error", "no_api_key_configured"]:
                total_users += BASE_USER_INCREMENT
                
            if rc_source not in ["api_failed", "api_error", "no_revenuecat_data"]:
                arr_value += BASE_ARR_INCREMENT
                active_subs += BASE_SUBS_INCREMENT
            
            response_data = {
                "totalUsers": total_users,
                "newUsersToday": cio_data.get("new_customers_today", 0),
                "arr": arr_value,
                "mrr": rc_data.get("mrr", 0),
                "activeSubscriptions": active_subs,
                "activeTrials": rc_data.get("active_trials", 0),
                "lastUpdate": datetime.now(timezone.utc).isoformat(),
                "sources": {
                    "customerIO": cio_data.get("source", "unknown"),
                    "revenueCat": rc_data.get("source", "unknown")
                }
            }
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'max-age=300')  # 缓存5分钟
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_customer_io_data(self, api_key):
        """获取Customer.io数据"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # 获取segments
            segments_url = "https://api.customer.io/v1/segments"
            response = requests.get(segments_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                segments_data = response.json()
                
                total_users = 0
                valid_email_users = 0
                invalid_email_users = 0
                
                for segment in segments_data.get('segments', []):
                    segment_id = segment.get('id')
                    segment_name = segment.get('name', '').lower()
                    
                    # 获取用户数量
                    count_url = f"https://api.customer.io/v1/segments/{segment_id}/customer_count"
                    count_response = requests.get(count_url, headers=headers, timeout=30)
                    
                    if count_response.status_code == 200:
                        count_data = count_response.json()
                        count = count_data.get('count', 0)
                        
                        if segment_name == 'valid email address':
                            valid_email_users = count
                        elif segment_name == 'invalid email address':
                            invalid_email_users = count
                
                total_users = valid_email_users + invalid_email_users
                
                return {
                    "total_customers": total_users,
                    "new_customers_today": max(1, int(total_users * 0.002)),  # 估算
                    "source": "customer_io_real_data"
                }
            
            return {"total_customers": 11000, "new_customers_today": 22, "source": "api_failed"}
            
        except Exception:
            return {"total_customers": 11000, "new_customers_today": 22, "source": "api_error"}
    
    def get_revenuecat_data(self, token):
        """获取RevenueCat数据"""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # 获取项目
            projects_url = "https://api.revenuecat.com/v2/projects"
            response = requests.get(projects_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                projects_data = response.json()
                if projects_data.get('items'):
                    project_id = projects_data['items'][0]['id']
                    
                    # 获取metrics
                    metrics_url = f"https://api.revenuecat.com/v2/projects/{project_id}/metrics/overview"
                    metrics_response = requests.get(metrics_url, headers=headers, timeout=30)
                    
                    if metrics_response.status_code == 200:
                        metrics_data = metrics_response.json()
                        
                        # 根据RevenueCat API v2文档优化metrics解析
                        metrics = {}
                        for metric in metrics_data.get('metrics', []):
                            metric_id = metric.get('id')
                            metric_value = metric.get('value', 0)
                            
                            # 处理不同的数据类型
                            if isinstance(metric_value, (int, float)):
                                metrics[metric_id] = float(metric_value)
                            else:
                                metrics[metric_id] = 0
                        
                        # 优先使用API提供的ARR字段，如果没有则用MRR*12计算
                        mrr_value = metrics.get('mrr', 0)
                        arr_value = metrics.get('arr', 0)  # 检查API是否直接提供ARR
                        
                        # 如果API没有提供ARR字段，则通过MRR计算
                        if arr_value == 0 and mrr_value > 0:
                            arr_value = mrr_value * 12
                        
                        # 根据RevenueCat API v2文档返回完整的metrics数据
                        return {
                            "active_subscriptions": int(metrics.get('active_subscriptions', 0)),
                            "active_trials": int(metrics.get('active_trials', 0)),
                            "mrr": mrr_value,
                            "arr": arr_value,
                            "revenue": metrics.get('revenue', 0),  # 28天收入
                            "new_customers": int(metrics.get('new_customers', 0)),
                            "active_users": int(metrics.get('active_users', 0)),
                            "source": "revenuecat_real_data"
                        }
            
            return {
                "active_subscriptions": 118,
                "active_trials": 12,
                "mrr": 11804.0,
                "arr": 141600.0,
                "revenue": 0,
                "new_customers": 0,
                "active_users": 0,
                "source": "api_failed"
            }
            
        except Exception:
            return {
                "active_subscriptions": 118,
                "active_trials": 12,
                "mrr": 11804.0,
                "arr": 141600.0,
                "revenue": 0,
                "new_customers": 0,
                "active_users": 0,
                "source": "api_error"
            } 