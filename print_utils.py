def print_results(proxy_alias, data):
    success_count = 0
    failure_count = 0
    delays = []
    for entry in data['data']:
        if 'delay' in entry and entry['delay'] is not None:
            delays.append(entry['delay'])
        if "成功" in entry['status']:
            success_count += 1
        elif "失败" in entry['status'] or "超时" in entry['status']:
            failure_count += 1
    
    avg_delay = sum(delays) / len(delays) if delays else 0
    max_delay = max(delays) if delays else 0
    min_delay = min(delays) if delays else 0

    print(f"\n---  {proxy_alias}  ---")
    print(f"成功: {success_count} 失败: {failure_count} 平均延迟: {avg_delay:.4f} 秒 最大: {max_delay:.4f} 秒 最小: {min_delay:.4f} 秒")
    
    for entry in data['data']:
        print(f"代理: {proxy_alias} - {entry['url_alias']} - {entry['url']} - {entry['status']}, 延迟: {entry['delay']:.4f} 秒" if entry['delay'] is not None else f"代理: {proxy_alias} - {entry['url_alias']} - {entry['url']} - {entry['status']}")
    
def print_summary(all_results):
    for proxy_alias, data in all_results.items():
        success_count = sum(1 for entry in data['data'] if "成功" in entry['status'])
        failure_count = sum(1 for entry in data['data'] if "失败" in entry['status'] or "超时" in entry['status'])
        delays = [entry['delay'] for entry in data['data'] if entry['delay'] is not None]
        
        avg_delay = sum(delays) / len(delays) if delays else 0
        max_delay = max(delays) if delays else 0
        min_delay = min(delays) if delays else 0
        
        print(f"\n---  {proxy_alias} 总结 ---")
        print(f"总成功: {success_count} 总失败: {failure_count} 平均延迟: {avg_delay:.4f} 秒 最大: {max_delay:.4f} 秒 最小: {min_delay:.4f} 秒")
