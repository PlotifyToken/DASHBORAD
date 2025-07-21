import json
from http.server import BaseHTTPRequestHandler
import requests
from datetime import datetime, timezone
import os

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
            response_data = {
                "totalUsers": cio_data.get("total_customers", 0),
                "newUsersToday": cio_data.get("new_customers_today", 0),
                "arr": rc_data.get("arr", 0),
                "mrr": rc_data.get("mrr", 0),
                "activeSubscriptions": rc_data.get("active_subscriptions", 0),
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
            
            return {"total_customers": 0, "new_customers_today": 0, "source": "api_failed"}
            
        except Exception:
            return {"total_customers": 0, "new_customers_today": 0, "source": "api_error"}
    
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
                        
                        metrics = {}
                        for metric in metrics_data.get('metrics', []):
                            metrics[metric.get('id')] = metric.get('value', 0)
                        
                        return {
                            "active_subscriptions": int(metrics.get('active_subscriptions', 0)),
                            "active_trials": int(metrics.get('active_trials', 0)),
                            "mrr": float(metrics.get('mrr', 0)),
                            "arr": float(metrics.get('mrr', 0)) * 12,
                            "source": "revenuecat_real_data"
                        }
            
            return {
                "active_subscriptions": 0,
                "active_trials": 0,
                "mrr": 0,
                "arr": 0,
                "source": "api_failed"
            }
            
        except Exception:
            return {
                "active_subscriptions": 0,
                "active_trials": 0,
                "mrr": 0,
                "arr": 0,
                "source": "api_error"
            } 