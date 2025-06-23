# -*- coding: utf-8 -*-
"""
    @Time   : 2025/6/23 20:24
    @Author : mxy
"""
from fastapi import FastAPI, HTTPException, APIRouter
import mysql.connector
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
router = APIRouter()

# 数据库连接配置
db_config = {
    "host": "47.98.150.68",
    "user": "root",
    "password": "r0mxy1q2w3e4r",
    "database": "fastgpt"
}

# 定义数据模型（对应T_ADS_INDEX表）
class AdsIndex(BaseModel):
    REC_ID: str
    ACCOUNT: str
    INDEX_CODE: Optional[str] = None
    INDEX_NAME: Optional[str] = None
    DIS_FLAG: Optional[str] = None
    PROD_DATE: Optional[str] = None
    INDEX_VALUE: Optional[float] = None
    IND_UNIT: Optional[str] = None

# 获取数据库连接
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据库连接失败: {e}")

# 创建表（如果不存在）
@app.on_event("startup")
async def startup_event():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS T_ADS_INDEX (
            REC_ID VARCHAR(32) PRIMARY KEY,
            ACCOUNT VARCHAR(4),
            INDEX_CODE VARCHAR(15) NULL COMMENT '指标代码',
            INDEX_NAME VARCHAR(20) NULL COMMENT '指标名称',
            DIS_FLAG VARCHAR(2) NULL COMMENT '日期维度',
            PROD_DATE VARCHAR(8) NULL COMMENT '日期',
            INDEX_VALUE DECIMAL(15, 6) NULL COMMENT '指标值',
            IND_UNIT VARCHAR(5) NULL COMMENT '指标单位'
        )
        """)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建表失败: {e}")
    finally:
        cursor.close()
        conn.close()

# 添加记录
@router.post("/ads_index/")
async def create_ads_index(item: AdsIndex):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO T_ADS_INDEX 
        (REC_ID, ACCOUNT, INDEX_CODE, INDEX_NAME, DIS_FLAG, PROD_DATE, INDEX_VALUE, IND_UNIT)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item.REC_ID, item.ACCOUNT, item.INDEX_CODE, item.INDEX_NAME,
            item.DIS_FLAG, item.PROD_DATE, item.INDEX_VALUE, item.IND_UNIT
        ))
        conn.commit()
        return {"message": "记录添加成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"添加记录失败: {e}")
    finally:
        cursor.close()
        conn.close()

# 获取所有记录
@router.get("/getAll/")
async def read_ads_index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM T_ADS_INDEX")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取记录失败: {e}")
    finally:
        cursor.close()
        conn.close()

# 获取单个记录
@router.get("/ads_index/{rec_id}")
async def read_ads_index_item(rec_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM T_ADS_INDEX WHERE REC_ID = %s", (rec_id,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="记录未找到")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取记录失败: {e}")
    finally:
        cursor.close()
        conn.close()

# 更新记录
@router.put("/ads_index/{rec_id}")
async def update_ads_index_item(rec_id: str, item: AdsIndex):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        UPDATE T_ADS_INDEX SET 
        ACCOUNT = %s, INDEX_CODE = %s, INDEX_NAME = %s, 
        DIS_FLAG = %s, PROD_DATE = %s, INDEX_VALUE = %s, IND_UNIT = %s
        WHERE REC_ID = %s
        """, (
            item.ACCOUNT, item.INDEX_CODE, item.INDEX_NAME,
            item.DIS_FLAG, item.PROD_DATE, item.INDEX_VALUE, item.IND_UNIT, rec_id
        ))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="记录未找到")
        conn.commit()
        return {"message": "记录更新成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"更新记录失败: {e}")
    finally:
        cursor.close()
        conn.close()

# 删除记录
@router.delete("/ads_index/{rec_id}")
async def delete_ads_index_item(rec_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM T_ADS_INDEX WHERE REC_ID = %s", (rec_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="记录未找到")
        conn.commit()
        return {"message": "记录删除成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"删除记录失败: {e}")
    finally:
        cursor.close()
        conn.close()