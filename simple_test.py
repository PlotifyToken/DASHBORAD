#!/usr/bin/env python3
"""
简单API测试
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone

# 设置API密钥
os.environ['CUSTOMER_IO_APP_API_KEY'] = '4da41dd5d42c3edb11415201fc1c024a'
os.environ['REVENUECAT_TOKEN'] = 'sk_EWEOIOZJEmiXoDOMkywmrklkuLwXi'

def test_customer_io():
    """测试Customer.io API"""
    print("🔍 测试Customer.io API...")
    
    api_key = os.environ.get('CUSTOMER_IO_APP_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # 获取segments
        segments_url = "https://api.customer.io/v1/segments"
        response = requests.get(segments_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            segments_data = response.json()
            print(f"✅ Customer.io连接成功，找到 {len(segments_data.get('segments', []))} 个segments")
            
            total_users = 0
            for segment in segments_data.get('segments', []):
                segment_id = segment.get('id')
                segment_name = segment.get('name', '').lower()
                
                if segment_name in ['valid email address', 'invalid email address']:
                    count_url = f"https://api.customer.io/v1/segments/{segment_id}/customer_count"
                    count_response = requests.get(count_url, headers=headers, timeout=30)
                    
                    if count_response.status_code == 200:
                        count_data = count_response.json()
                        count = count_data.get('count', 0)
                        total_users += count
                        print(f"   📊 {segment.get('name')}: {count} 用户")
            
            print(f"   👥 总用户数: {total_users}")
            return total_users
        else:
            print(f"❌ Customer.io API错误: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Customer.io错误: {e}")
        return 0

def test_revenuecat():
    """测试RevenueCat API"""
    print("\n💰 测试RevenueCat API...")
    
    token = os.environ.get('REVENUECAT_TOKEN')
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 获取项目
        projects_url = "https://api.revenuecat.com/v2/projects"
        response = requests.get(projects_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            projects_data = response.json()
            if projects_data.get('items'):
                project = projects_data['items'][0]
                project_id = project['id']
                project_name = project['name']
                print(f"✅ RevenueCat连接成功，项目: {project_name}")
                
                # 获取metrics
                metrics_url = f"https://api.revenuecat.com/v2/projects/{project_id}/metrics/overview"
                metrics_response = requests.get(metrics_url, headers=headers, timeout=30)
                
                if metrics_response.status_code == 200:
                    metrics_data = metrics_response.json()
                    
                    metrics = {}
                    for metric in metrics_data.get('metrics', []):
                        metrics[metric.get('id')] = metric.get('value', 0)
                    
                    active_subs = int(metrics.get('active_subscriptions', 0))
                    mrr = float(metrics.get('mrr', 0))
                    arr = mrr * 12
                    
                    print(f"   ⭐ 活跃订阅: {active_subs}")
                    print(f"   💵 MRR: ${mrr}")
                    print(f"   💰 ARR: ${arr}")
                    
                    return {
                        'active_subscriptions': active_subs,
                        'mrr': mrr,
                        'arr': arr
                    }
        
        print(f"❌ RevenueCat API错误: {response.status_code if 'response' in locals() else 'Unknown'}")
        return {}
        
    except Exception as e:
        print(f"❌ RevenueCat错误: {e}")
        return {}

def main():
    """主测试函数"""
    print("🚀 UnlockLand API 简单测试")
    print("=" * 50)
    
    # 测试Customer.io
    total_users = test_customer_io()
    
    # 测试RevenueCat
    rc_data = test_revenuecat()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print(f"   👥 总用户: {total_users}")
    print(f"   ⭐ 活跃订阅: {rc_data.get('active_subscriptions', 0)}")
    print(f"   💰 ARR: ${rc_data.get('arr', 0)}")
    
    # 生成测试数据JSON
    test_data = {
        "totalUsers": total_users,
        "activeSubscriptions": rc_data.get('active_subscriptions', 0),
        "arr": rc_data.get('arr', 0),
        "mrr": rc_data.get('mrr', 0),
        "lastUpdate": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "customerIO": "real_data" if total_users > 0 else "failed",
            "revenueCat": "real_data" if rc_data else "failed"
        }
    }
    
    print(f"\n📄 生成测试数据:")
    print(json.dumps(test_data, indent=2))
    
    if total_users > 0 and rc_data:
        print("\n🎉 所有API测试通过！可以部署了")
        return True
    else:
        print("\n❌ 部分API测试失败")
        return False

if __name__ == "__main__":
    main() 