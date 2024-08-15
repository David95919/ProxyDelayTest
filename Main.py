import asyncio
import time  # 添加这一行以导入 time 模块
from utils import load_config
from db import init_db
from print_utils import print_results, print_summary
from test_http import test_http_client

async def run_tests(test_urls, proxies, results, enable_db_stats):
    tasks = [test_http_client(test_urls, proxy['url'], proxy['alias'], results, enable_db_stats) for proxy in proxies]
    await asyncio.gather(*tasks)
    
    for proxy_alias, data in results.items():
        print_results(proxy_alias, data)
    
    if enable_db_stats:
        from db import update_test_stats
        for proxy_alias, data in results.items():
            success_count = sum(1 for entry in data['data'] if "成功" in entry['status'])
            failure_count = sum(1 for entry in data['data'] if "失败" in entry['status'] or "超时" in entry['status'])
            delays = [entry['delay'] for entry in data['data'] if entry['delay'] is not None]
            update_test_stats(proxy_alias, data['proxy'], success_count, failure_count, delays, 'test_results.db')

def periodic_test(test_urls, socks5_proxies, interval, test_count, db_name):
    all_results = {proxy['alias']: {'data': [], 'proxy': proxy['url']} for proxy in socks5_proxies}
    
    for round_num in range(1, test_count + 1):
        results = {}
        asyncio.run(run_tests(test_urls, socks5_proxies, results, ENABLE_DB_STATS))
        
        for proxy_alias, data in results.items():
            if proxy_alias not in all_results:
                all_results[proxy_alias] = {'data': [], 'proxy': data['proxy']}
            all_results[proxy_alias]['data'].extend(data['data'])
        
        if round_num < test_count:  # 仅在不是最后一轮时进行等待
            print(f"\n等待 {interval} 分钟后进行下一轮测试...")
            time.sleep(interval * 60)  # 休眠指定的分钟数
    
    # 打印总结
    print_summary(all_results)

if __name__ == "__main__":
    test_urls, socks5_proxies, interval, test_count, ENABLE_DB_STATS = load_config('config.json')
    
    if ENABLE_DB_STATS:
        init_db()
    
    periodic_test(test_urls, socks5_proxies, interval, test_count, 'test_results.db')
