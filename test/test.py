# -*- coding: utf-8 -*-
"""
    @Time   : 2025/5/17 11:11
    @Author : mxy
"""


import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(device)

import mysql.connector

try:
    conn = mysql.connector.connect(
        host="47.98.150.68",
        user="root",
        password="r0mxy1q2w3e4r",
        database="fastgpt"
    )
    print("连接成功！")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    print(cursor.fetchall())
    conn.close()
except Exception as e:
    print(f"连接失败: {e}")