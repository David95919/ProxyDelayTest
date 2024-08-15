CREATE TABLE TestList (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 主键，自动递增
    proxy_alias TEXT NOT NULL,                -- 代理的别名，例如 "代理1"
    proxy TEXT NOT NULL,                      -- 代理的信息，例如 "socks5://192.168.2.1:10086"
    url_alias TEXT NOT NULL,                  -- 测试网站别名，例如 "Google"
    url TEXT NOT NULL,                        -- 测试网站 URL，例如 "http://www.gstatic.com/generate_204"
    delay REAL NOT NULL,                      -- 延迟，以秒为单位，例如 "1.6251"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 插入记录时的创建时间
);

CREATE TABLE TestStats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 主键，自动递增
    proxy_alias TEXT NOT NULL,                -- 代理的别名，例如 "代理1"
    proxy TEXT NOT NULL,                      -- 代理的信息，例如 "socks5://192.168.2.1:10086"
    total_success INTEGER DLEFAUT 0,          -- 总成功次数，默认为 0
    total_failure INTEGER DEFAULT 0,          -- 总失败次数，默认为 0
    avg_delay REAL DEFAULT 0.0,               -- 平均延迟，单位为秒，默认为 0.0
    max_delay REAL DEFAULT 0.0,               -- 最大延迟，单位为秒，默认为 0.0
    min_delay REAL DEFAULT 0.0                -- 最小延迟，单位为秒，默认为 0.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 插入记录时的创建时间
    UNIQUE (proxy_alias, proxy)               -- 添加复合唯一约束
);
