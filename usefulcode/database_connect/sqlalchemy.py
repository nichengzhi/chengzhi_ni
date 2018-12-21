#sql module
import sqlalchemy
from sqlalchemy import *
import pandas as pd
import numpy as np

mysql_user = 'xxxx'
mysql_password = 'xxxxx'

engine = create_engine('xxxxx', echo=False)
conn = engine.connect()
sql = """select primary_isbn13,concat(level_one, level_two,level_three),group_cat from (select PrimaryISBN13, group_concat(distinct Category separator ';') as group_cat from ingests_ebb_schedule group by PrimaryISBN13) a inner join title_to_bisac_pivot b on a.PrimaryISBN13 = b.primary_isbn13;"""
result = conn.execute(sql)
raw_data = [x for x in result]