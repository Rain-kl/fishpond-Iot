import sqlite3
from datetime import datetime
from typing import List, Optional

from config import db_path
from .model import ZXDataModel


class ZXDataDB:
    """ZXDataModel的数据库操作类"""

    def __init__(self, db_path: str = "data/zx_data.db"):
        """初始化数据库连接"""
        self.db_path = db_path
        self._create_table_if_not_exists()

    def _get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)

    def _create_table_if_not_exists(self):
        """如果表不存在，则创建表"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
                       CREATE TABLE IF NOT EXISTS zx_data
                       (
                           addr    TEXT PRIMARY KEY,
                           TYPE    TEXT,
                           PN      TEXT,
                           A0      TEXT,
                           A1      TEXT,
                           A2      TEXT,
                           A3      TEXT,
                           A4      TEXT,
                           A5      TEXT,
                           A6      TEXT,
                           A7      TEXT,
                           D1      TEXT,
                           updated TEXT
                       )
                       """
        )

        # 检查表中是否已经有A1-A3字段，如果没有则添加
        cursor.execute("PRAGMA table_info(zx_data)")
        columns = [column[1] for column in cursor.fetchall()]

        # 如果是旧版本的表结构，添加新的字段
        if "A1" not in columns:
            cursor.execute("ALTER TABLE zx_data ADD COLUMN A1 TEXT")
        if "A2" not in columns:
            cursor.execute("ALTER TABLE zx_data ADD COLUMN A2 TEXT")
        if "A3" not in columns:
            cursor.execute("ALTER TABLE zx_data ADD COLUMN A3 TEXT")

        conn.commit()
        conn.close()

    def insert(self, addr: str, model: ZXDataModel) -> bool | None:
        """插入一条记录，使用指定的addr作为主键，返回是否插入成功"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                           INSERT INTO zx_data (addr, TYPE, PN, A0, A1, A2, A3, A4, A5, A6, A7, D1, updated)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           """,
                (
                    addr,
                    model.TYPE,
                    model.PN,
                    model.A0,
                    model.A1,
                    model.A2,
                    model.A3,
                    model.A4,
                    model.A5,
                    model.A6,
                    model.A7,
                    model.D1,
                    model.updated,
                ),
            )

            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            # addr已存在的情况
            conn.rollback()
            success = False
        finally:
            conn.close()

        return success

    def update(self, addr: str, model: ZXDataModel) -> bool:
        """更新指定addr的记录，只更新非空字段"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 获取当前记录
        cursor.execute("SELECT * FROM zx_data WHERE addr = ?", (addr,))
        record = cursor.fetchone()

        if not record:
            self.insert(addr, model)
            return True

        # 构建更新语句和参数
        update_fields = []
        params = []

        # 检查每个字段，只更新非空的
        if model.TYPE:
            update_fields.append("TYPE = ?")
            params.append(model.TYPE)

        if model.PN:
            update_fields.append("PN = ?")
            params.append(model.PN)

        if model.A0:
            update_fields.append("A0 = ?")
            params.append(model.A0)

        if model.A1:
            update_fields.append("A1 = ?")
            params.append(model.A1)

        if model.A2:
            update_fields.append("A2 = ?")
            params.append(model.A2)

        if model.A3:
            update_fields.append("A3 = ?")
            params.append(model.A3)

        if model.A4:
            update_fields.append("A4 = ?")
            params.append(model.A4)

        if model.A5:
            update_fields.append("A5 = ?")
            params.append(model.A5)

        if model.A6:
            update_fields.append("A6 = ?")
            params.append(model.A6)

        if model.A7:
            update_fields.append("A7 = ?")
            params.append(model.A7)

        if model.D1:
            update_fields.append("D1 = ?")
            params.append(model.D1)

        # 总是更新updated字段
        update_fields.append("updated = ?")
        if model.updated:
            params.append(model.updated)
        else:
            params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # 添加addr参数
        params.append(addr)

        # 如果没有字段需要更新，则返回
        if not update_fields:
            conn.close()
            return False

        # 执行更新
        query = f"UPDATE zx_data SET {', '.join(update_fields)} WHERE addr = ?"
        cursor.execute(query, params)

        conn.commit()
        conn.close()
        return cursor.rowcount > 0

    def delete(self, addr: str) -> bool:
        """删除指定addr的记录"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM zx_data WHERE addr = ?", (addr,))

        result = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return result

    def get_by_addr(self, addr: str) -> Optional[ZXDataModel]:
        """根据addr获取记录"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM zx_data WHERE addr = ?", (addr,))
        record = cursor.fetchone()

        conn.close()

        if not record:
            return None

        # 将记录转换为模型对象
        columns = [column[0] for column in cursor.description]
        values = dict(zip(columns, record))

        # 移除addr字段
        if "addr" in values:
            del values["addr"]

        return ZXDataModel(**values)

    def get_all(self) -> List[dict]:
        """获取所有记录，返回包含addr和模型的字典列表"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM zx_data")
        records = cursor.fetchall()

        result = []
        columns = [column[0] for column in cursor.description]

        for record in records:
            values = dict(zip(columns, record))

            # 分离addr和其他属性
            addr = values.pop("addr")
            model = ZXDataModel(**values)

            result.append({"addr": addr, "model": model})

        conn.close()
        return result

    def search(self, **kwargs) -> ZXDataModel | list[dict] | None:
        """根据条件搜索记录，返回包含addr和模型的字典列表"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 构建查询条件
        conditions = []
        params = []

        for key, value in kwargs.items():
            if key == "addr" and value:
                conditions.append("addr LIKE ?")
                params.append(f"%{value}%")
            elif hasattr(ZXDataModel, key) and value:
                conditions.append(f"{key} LIKE ?")
                params.append(f"%{value}%")

        # 如果没有条件，返回所有记录
        if not conditions:
            return self.get_all()

        query = f"SELECT * FROM zx_data WHERE {' AND '.join(conditions)}"
        cursor.execute(query, params)
        records = cursor.fetchall()

        result = []
        columns = [column[0] for column in cursor.description]

        for record in records:
            values = dict(zip(columns, record))

            # 分离addr和其他属性
            addr = values.pop("addr")
            model = ZXDataModel(**values)
            conn.close()
            return model
        conn.close()
        return None


zx_db = ZXDataDB(db_path)
