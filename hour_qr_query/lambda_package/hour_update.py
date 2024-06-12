import mysql.connector
from query import get_query
from hour import set_time
import update_db

db_connection = mysql.connector.connect(
    host='visa-fx-05006aa44b45542b.elb.ap-southeast-1.amazonaws.com',
    port='1234',
    database='visa_fx',
    user='aws_lambda',
    password='&o17r%FK$Ft8'
)


s, e = set_time()
event_streams = get_query(s_time=s, e_time=e)

update_db.update_analysis_table(connection=db_connection, start_time=s, log_event_streams=event_streams)
update_db.update_raw_table(connection=db_connection, log_event_streams=event_streams)

db_connection.close()