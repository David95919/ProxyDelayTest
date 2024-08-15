import asyncio
import aiohttp
import time
import json
import sqlite3
from aiohttp_socks import ProxyConnector
from collections import defaultdict

# 数据库初始化
def init_db(db_name='test_results.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TestList (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proxy_alias TEXT NOT NULL,
        proxy TEXT NOT NULL,
        url_alias TEXT NOT NULL,
        url TEXT NOT NULL,
        delay REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TestStats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proxy_alias TEXT NOT NULL,
        proxy TEXT NOT NULL,
        total_success INTEGER DEFAULT 0,
        total_failure INTEGER DEFAULT 0,
        avg_delay REAL DEFAULT 0.0,
        max_delay REAL DEFAULT 0.0,
        min_delay REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (proxy_alias, proxy)
    )
    ''')
    
    conn.commit()
    conn.close()

def insert_test_list(proxy_alias, proxy, url_alias, url, delay, db_name='test_results.db'):
    if not ENABLE_DB_STATS:
        return
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO TestList (proxy_alias, proxy, url_alias, url, delay)
    VALUES (?, ?, ?, ?, ?)
    ''', (proxy_alias, proxy, url_alias, url, delay))
    conn.commit()
    conn.close()

def update_test_stats(proxy_alias, proxy, success_count, failure_count, delays, db_name='test_results.db'):
    if not ENABLE_DB_STATS:
        return
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    avg_delay = sum(delays) / len(delays) if delays else 0
    max_delay = max(delays) if delays else 0
    min_delay = min(delays) if delays else 0

    cursor.execute('''
    INSERT INTO TestStats (proxy_alias, proxy, total_success, total_failure, avg_delay, max_delay, min_delay)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(proxy_alias, proxy) DO UPDATE SET
        total_success = excluded.total_success,
        total_failure = excluded.total_failure,
        avg_delay = excluded.avg_delay,
        max_delay = excluded.max_delay,
        min_delay = excluded.min_delay
    ''', (proxy_alias, proxy, success_count, failure_count, avg_delay, max_delay, min_delay))

    conn.commit()
    conn.close()

async def fetch(session, url, proxy_alias, url_alias, results, db_name):
    try:
        start_time = time.time()
        timeout = aiohttp.ClientTimeout(total=10)  # 设置请求超时时间为10秒
        async with session.get(url, timeout=timeout) as response:
            end_time = time.time()
            delay = end_time - start_time
            
            # 特别处理204状态码
            if response.status == 204:
                status = "成功(No Content)"
            elif response.status == 200:
                status = "成功"
            else:
                status = f"失败({response.status})"
            
            results[proxy_alias]['data'].append({
                'status': status,
                'url': url,
                'url_alias': url_alias,
                'delay': delay
            })
            
            # 将结果插入到 TestList
            insert_test_list(proxy_alias, results[proxy_alias]['proxy'], url_alias, url, delay, db_name)
    
    except asyncio.TimeoutError:
        results[proxy_alias]['data'].append({
            'status': "请求超时",
            'url': url,
            'url_alias': url_alias,
            'delay': None
        })
        # 将超时结果插入到 TestList
        insert_test_list(proxy_alias, results[proxy_alias]['proxy'], url_alias, url, None, db_name)
    except Exception as e:
        results[proxy_alias]['data'].append({
            'status': f"请求异常: {e}",
            'url': url,
            'url_alias': url_alias,
            'delay': None
        })
        # 将异常结果插入到 TestList
        insert_test_list(proxy_alias, results[proxy_alias]['proxy'], url_alias, url, None, db_name)

async def test_http_client(urls, proxy, proxy_alias, results, db_name):
    try:
        connector = ProxyConnector.from_url(proxy)
        async with aiohttp.ClientSession(connector=connector) as session:
            results[proxy_alias] = {'data': [], 'proxy': proxy}
            tasks = [fetch(session, url['url'], proxy_alias, url['alias'], results, db_name) for url in urls]
            await asyncio.gather(*tasks)
    except Exception as e:
        results[proxy_alias] = {'data': [f"无法创建会话, 错误: {e}"], 'proxy': proxy}

async def run_tests(test_urls, proxies, results, db_name):
    await test_http_clients(test_urls, proxies, results, db_name)
    
    # 分类输出
    for proxy_alias, data in results.items():
        # 计算统计数据
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
        
        # 更新 TestStats
        update_test_stats(proxy_alias, data['proxy'], success_count, failure_count, delays, db_name)

async def test_http_clients(test_urls, proxies, results, db_name):
    tasks = [test_http_client(test_urls, proxy['url'], proxy['alias'], results, db_name) for proxy in proxies]
    await asyncio.gather(*tasks)

async def periodic_test(test_urls, proxies, interval, test_count, db_name):
    all_results = defaultdict(lambda: {'data': []})  # 存储所有轮次的结果
    for i in range(test_count):
        print(f"\n开始第 {i+1} 轮测试...")
        results = defaultdict(dict)
        await run_tests(test_urls, proxies, results, db_name)
        # 合并结果到 all_results
        for proxy_alias, data in results.items():
            all_results[proxy_alias]['data'].extend(data['data'])
        if i < test_count - 1:
            print(f"\n等待 {interval} 分钟后开始下一轮测试...")
            await asyncio.sleep(interval * 60)  # 等待指定分钟数
    
    # 输出所有轮次的总结统计数据
    summarize_results(all_results)

def summarize_results(all_results):
    for proxy_alias, data in all_results.items():
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
        
        print(f"\n---  {proxy_alias} 总结 ---")
        print(f"总成功: {success_count} 总失败: {failure_count} 平均延迟: {avg_delay:.4f} 秒 最大: {max_delay:.4f} 秒 最小: {min_delay:.4f} 秒")

def load_config(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config['test_urls'], config['socks5_proxies'], config['interval'], config['test_count'], config.get('enable_db_stats', True)

# 从 JSON 文件中加载配置
test_urls, socks5_proxies, interval, test_count, ENABLE_DB_STATS = load_config('config.json')

# 初始化数据库
if ENABLE_DB_STATS:
    init_db()

# 执行持续性测试
asyncio.run(periodic_test(test_urls, socks5_proxies, interval, test_count, 'test_results.db'))
