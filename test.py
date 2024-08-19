import pyodbc
import pandas as pd

# 连接信息
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_server_name;"
    "DATABASE=your_database_name;"
    "UID=your_username;"
    "PWD=your_password"
)

# 建立连接
conn = pyodbc.connect(conn_str)

# SQL 查询
query = "SELECT * FROM your_table"

# 读取查询结果到 DataFrame
df = pd.read_sql(query, conn)

# 关闭连接
conn.close()

# 显示 DataFrame 的前几行
print(df.head())

# DataFrame 基本信息
print(df.info())