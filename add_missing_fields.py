#!/usr/bin/env python
"""添加缺失的字段到现有表"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 添加缺失的字段
statements = [
    "ALTER TABLE system_deptinfo ADD COLUMN creator_id INTEGER REFERENCES persistence_user(id)",
    "ALTER TABLE system_deptinfo ADD COLUMN modifier_id INTEGER REFERENCES persistence_user(id)",
    "ALTER TABLE system_menu ADD COLUMN meta_id VARCHAR(32) REFERENCES system_menumeta(id)",
    "ALTER TABLE system_menu ADD COLUMN creator_id INTEGER REFERENCES persistence_user(id)",
    "ALTER TABLE system_menu ADD COLUMN modifier_id INTEGER REFERENCES persistence_user(id)",
    "ALTER TABLE system_operationlog ADD COLUMN creator_id INTEGER REFERENCES persistence_user(id)",
    "ALTER TABLE system_userrole ADD COLUMN creator_id INTEGER REFERENCES persistence_user(id)",
    "ALTER TABLE system_userrole ADD COLUMN modifier_id INTEGER REFERENCES persistence_user(id)",
    "ALTER TABLE system_menumeta ADD COLUMN r_svg_name VARCHAR(255)",
    "ALTER TABLE system_menumeta ADD COLUMN is_show_parent BOOLEAN DEFAULT 0",
    "ALTER TABLE system_menumeta ADD COLUMN is_keepalive BOOLEAN DEFAULT 1",
    "ALTER TABLE system_menumeta ADD COLUMN frame_url VARCHAR(255)",
    "ALTER TABLE system_menumeta ADD COLUMN frame_loading BOOLEAN DEFAULT 0",
    "ALTER TABLE system_menumeta ADD COLUMN transition_enter VARCHAR(255)",
    "ALTER TABLE system_menumeta ADD COLUMN transition_leave VARCHAR(255)",
    "ALTER TABLE system_menumeta ADD COLUMN is_hidden_tag BOOLEAN DEFAULT 0",
    "ALTER TABLE system_menumeta ADD COLUMN fixed_tag BOOLEAN DEFAULT 0",
    "ALTER TABLE system_menumeta ADD COLUMN dynamic_level INTEGER DEFAULT 0",
    "ALTER TABLE system_menumeta ADD COLUMN creator_id INTEGER REFERENCES persistence_user(id)",
    "ALTER TABLE system_menumeta ADD COLUMN modifier_id INTEGER REFERENCES persistence_user(id)",
]

for stmt in statements:
    try:
        cursor.execute(stmt)
        print(f"OK: {stmt[:60]}...")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e):
            print(f"WARN: Column already exists: {stmt[:60]}...")
        else:
            print(f"ERROR: {e}")

conn.commit()
conn.close()

print("\nFields added successfully!")
