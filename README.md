# 运行
```bash
pip install requirements.txt
python Main.py
```

# 配置
1. socks5_proxies 代理列表
2. test_urls 测试网站
3. interval 测试间隔
4. test_count 测试次数
5. enable_db_stats是否开启数据库

# 输出
```bash
开始第 2 轮测试...

---  代理1  ---
成功: 5 失败: 1 平均延迟: 3.2857 秒 最大: 5.5251 秒 最小: 0.1845 秒
代理: 代理1 - MicroSoft - http://www.msftconnecttest.com/connecttest.txt - 成功, 延迟: 0.1845 秒
代理: 代理1 - Firefox - https://detectportal.firefox.com/success.txt - 成功, 延迟: 0.2684 秒
代理: 代理1 - Google - http://www.gstatic.com/generate_204 - 成功(No Content), 延迟: 5.2148 秒
代理: 代理1 - Cloudflare - http://cp.cloudflare.com/ - 成功(No Content), 延迟: 5.2359 秒
代理: 代理1 - Apple - http://www.apple.com/library/test/success.html - 成功, 延迟: 5.5251 秒
代理: 代理1 - V2ex - http://www.v2ex.com/generate_204 - 请求超时

---  代理2  ---
成功: 6 失败: 0 平均延迟: 1.7235 秒 最大: 3.0475 秒 最小: 1.3188 秒
代理: 代理2 - MicroSoft - http://www.msftconnecttest.com/connecttest.txt - 成功, 延迟: 1.3188 秒
代理: 代理2 - Google - http://www.gstatic.com/generate_204 - 成功(No Content), 延迟: 1.3284 秒
代理: 代理2 - Cloudflare - http://cp.cloudflare.com/ - 成功(No Content), 延迟: 1.3359 秒
代理: 代理2 - Firefox - https://detectportal.firefox.com/success.txt - 成功, 延迟: 1.6537 秒
代理: 代理2 - Apple - http://www.apple.com/library/test/success.html - 成功, 延迟: 1.6567 秒
代理: 代理2 - V2ex - http://www.v2ex.com/generate_204 - 成功(No Content), 延迟: 3.0475 秒

---  代理1 总结 ---
总成功: 11 总失败: 1 平均延迟: 1.6786 秒 最大: 5.5251 秒 最小: 0.1845 秒

---  代理2 总结 ---
总成功: 12 总失败: 0 平均延迟: 1.8402 秒 最大: 3.2345 秒 最小: 1.3188 秒
```