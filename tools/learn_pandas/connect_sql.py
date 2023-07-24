import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine('mysql+pymysql://root:198957wanmm@localhost:3306/new_api_case')
# 读取数据
df = pd.read_sql_table('test_result', engine)
# print(df)
query = '''
select * from test_result where api_id =21
'''

df1 = pd.read_sql_query(query, engine)
print(df1)

# 写数据
df.to_sql(name='test_reuslt2', con=engine, if_exists='append', index=False)


