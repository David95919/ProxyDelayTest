import aiohttp
import asyncio
import time
from aiohttp_socks import ProxyConnector

async def fetch(session, url, proxy_alias, url_alias, results, db_name, enable_db_stats):
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
            if enable_db_stats:
                from db import insert_test_list
                insert_test_list(proxy_alias, results[proxy_alias]['proxy'], url_alias, url, delay, 'test_results.db')
    
    except asyncio.TimeoutError:
        results[proxy_alias]['data'].append({
            'status': "请求超时",
            'url': url,
            'url_alias': url_alias,
            'delay': None
        })
        # 将超时结果插入到 TestList
        if enable_db_stats:
            from db import insert_test_list
            insert_test_list(proxy_alias, results[proxy_alias]['proxy'], url_alias, url, None, 'test_results.db')
    except Exception as e:
        results[proxy_alias]['data'].append({
            'status': f"请求异常: {e}",
            'url': url,
            'url_alias': url_alias,
            'delay': None
        })
        # 将异常结果插入到 TestList
        if enable_db_stats:
            from db import insert_test_list
            insert_test_list(proxy_alias, results[proxy_alias]['proxy'], url_alias, url, None, 'test_results.db')

async def test_http_client(urls, proxy, proxy_alias, results, enable_db_stats):
    try:
        connector = ProxyConnector.from_url(proxy)
        async with aiohttp.ClientSession(connector=connector) as session:
            results[proxy_alias] = {'data': [], 'proxy': proxy}
            tasks = [fetch(session, url['url'], proxy_alias, url['alias'], results, 'test_results.db', enable_db_stats) for url in urls]
            await asyncio.gather(*tasks)
    except Exception as e:
        results[proxy_alias] = {'data': [f"无法创建会话, 错误: {e}"], 'proxy': proxy}
