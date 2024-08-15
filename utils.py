import json

def load_config(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config['test_urls'], config['socks5_proxies'], config['interval'], config['test_count'], config.get('enable_db_stats', True)
