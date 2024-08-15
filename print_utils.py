from colorama import Fore, Style, init
init()  # 初始化 colorama

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

    print(f"\n---  {Fore.CYAN}{proxy_alias}{Style.RESET_ALL}  ---")
    print(f"{Fore.GREEN}成功:{Style.RESET_ALL} {success_count} {Fore.RED}失败:{Style.RESET_ALL} {failure_count} "
          f"{Fore.BLUE}平均延迟:{Style.RESET_ALL} {avg_delay:.4f} 秒 {Fore.BLUE}最大:{Style.RESET_ALL} {max_delay:.4f} 秒 "
          f"{Fore.BLUE}最小:{Style.RESET_ALL} {min_delay:.4f} 秒")
    
    for entry in data['data']:
        if entry['delay'] is not None:
            status_color = Fore.GREEN if "成功" in entry['status'] else Fore.RED
            print(f"代理: {Fore.CYAN}{proxy_alias}{Style.RESET_ALL} - {Fore.YELLOW}{entry['url_alias']}{Style.RESET_ALL} - "
                  f"{Fore.MAGENTA}{entry['url']}{Style.RESET_ALL} - {status_color}{entry['status']}{Style.RESET_ALL}, "
                  f"延迟: {Fore.BLUE}{entry['delay']:.4f} 秒{Style.RESET_ALL}")
        else:
            status_color = Fore.GREEN if "成功" in entry['status'] else Fore.RED
            print(f"代理: {Fore.CYAN}{proxy_alias}{Style.RESET_ALL} - {Fore.YELLOW}{entry['url_alias']}{Style.RESET_ALL} - "
                  f"{Fore.MAGENTA}{entry['url']}{Style.RESET_ALL} - {status_color}{entry['status']}{Style.RESET_ALL}")

def print_summary(all_results):
    for proxy_alias, data in all_results.items():
        success_count = sum(1 for entry in data['data'] if "成功" in entry['status'])
        failure_count = sum(1 for entry in data['data'] if "失败" in entry['status'] or "超时" in entry['status'])
        delays = [entry['delay'] for entry in data['data'] if entry['delay'] is not None]
        
        avg_delay = sum(delays) / len(delays) if delays else 0
        max_delay = max(delays) if delays else 0
        min_delay = min(delays) if delays else 0
        
        print(f"\n---  {Fore.CYAN}{proxy_alias}{Style.RESET_ALL} 总结 ---")
        print(f"{Fore.GREEN}总成功:{Style.RESET_ALL} {success_count} {Fore.RED}总失败:{Style.RESET_ALL} {failure_count} "
              f"{Fore.BLUE}平均延迟:{Style.RESET_ALL} {avg_delay:.4f} 秒 {Fore.BLUE}最大:{Style.RESET_ALL} {max_delay:.4f} 秒 "
              f"{Fore.BLUE}最小:{Style.RESET_ALL} {min_delay:.4f} 秒")
