import psycopg2
import pandas as pd
 
dbname = "x"
host = "xxxxus-east-1.redshift.amazonaws.com"
redshift_user='xx'
redshift_password='xxx'

conn_string = "dbname=%s port='5439' user=%s password=%s host=%s" %(dbname, redshift_user, redshift_password, host)
print "Connecting to database\n        ->%s" % (conn_string)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
cursor.execute("select email, referral_source from ebb_list_data a left join ebb_list_data_emails b on a.profile_id = b.profile_id")
data = cursor.fetchall()
feed = pd.DataFrame(data)
cursor.close()