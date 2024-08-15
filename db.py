import sqlite3

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
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO TestList (proxy_alias, proxy, url_alias, url, delay)
    VALUES (?, ?, ?, ?, ?)
    ''', (proxy_alias, proxy, url_alias, url, delay))
    conn.commit()
    conn.close()

def update_test_stats(proxy_alias, proxy, success_count, failure_count, delays, db_name='test_results.db'):
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
