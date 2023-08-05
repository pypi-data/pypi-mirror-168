
from typing import Optional
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, exc


class PDO:
    def __init__(self, host: Optional[str] = "localhost", port: Optional[int] = 3306, dbname: Optional[str] = "",
                 user: Optional[str] = None, password: Optional[str] = "", charset: Optional[str] = 'UTF8',
                 connection_url: Optional[str] = None):
        if connection_url is None:
            connection_url = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(
                user, password, host, port, dbname, charset
            )
        self.engine = create_engine(connection_url)

    def update(self, sql: str, args: [] = []):
        """
        执行 UPDATE 或者 DELETE 更新语句，返回值为 PyMYSQL native 数据
        :param sql:
        :param args:
        :return:
        """
        return self.engine.execute(sql, args)

    def select(self, sql: str, args: [] = None):
        """
        查询数据库
        :param sql:
        :param args:
        :return:
        """
        return pd.read_sql(sql, self.engine, params=args)

    def scalar(self, sql: str, args: [] = None):
        data = self.select(sql, args)
        if data.shape[0] > 0:
            return data.values[0][0]
        else:
            return None

    def one(self, sql: str, args: [] = None):
        """
        查询第一行数据
        """
        data = self.select(sql, args)
        return data.iloc[0].to_dict() if data.shape[0] > 0 else None

    def to_sql(self, data: pd.DataFrame, table_name: str, init_db: bool = False, index: bool = False):
        """
        将 DataFrame 保存到数据库
        :param data: 数据
        :param table_name: 目标表名
        :param index:
        :param if_exists:
        :param init_db: 是否初始化数据库
        :return:
        """
        if data.shape[0] == 0:
            return

        data = data.replace({np.nan: None})

        if init_db:
            try:
                data.to_sql(table_name, self.engine, index=False, if_exists='append')
            except exc.IntegrityError as e:
                pass
            except Exception as ex:
                raise ex

        keys = data.keys()
        values = data.values.tolist()

        key_sql = '`' + '`,`'.join(keys) + "`"
        value_sql = ','.join(['%s'] * data.shape[1])

        # 插入语句，若数据已存在则更新数据
        insert_data_str = """ insert into %s (%s) values (%s) ON DUPLICATE KEY UPDATE""" % (
            table_name, key_sql, value_sql)
        update_str = ','.join([" `{key}` = VALUES(`{key}`)".format(key=key) for key in keys])
        insert_data_str += update_str

        # 提交数据库操作
        # print(insert_data_str)
        try:
            self.engine.execute(insert_data_str, values)
        except Exception as ex:
            print(ex)
            raise ex

    def read_sql(self, sql: str, args: [] = None):
        """
        alias of select
        :param sql:
        :param args:
        :return:
        """
        return self.select(sql, args)

    def exists(self, sql: str, args: [] = None):
        """
        判断数据是否存在
        :param sql:
        :param args:
        :return:
        """
        data = self.select(sql, args)
        return data.shape[0] > 0