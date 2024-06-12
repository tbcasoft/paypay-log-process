import mysql.connector

connection = mysql.connector.connect(
    host='visa-fx-05006aa44b45542b.elb.ap-southeast-1.amazonaws.com',
    port='1234',
    database='hour_qr',
    user='aws_lambda',
    password='&o17r%FK$Ft8'
)

cursor = connection.cursor()

create_raw_table = '''
CREATE TABLE IF NOT EXISTS mainnet_hour_qr_raw (
    time TIMESTAMP,
    id VARCHAR(100),
    qr VARCHAR(100),
    result_code VARCHAR(20),
    PRIMARY KEY (time, id)
)
'''

# create_analysis_table = '''
# CREATE TABLE IF NOT EXISTS mainnet_hour_qr_result (
#     id INT AUTO_INCREMENT,
#     time VARCHAR(20),
#     SUCCESS INT, 
#     MERCHANT_SUSPENDED INT, 
#     HIVEX_UNAVAILABLE_MERCHANT INT, 
#     Dynamic_QR INT, 
#     P2P INT, 
#     Others INT, 
#     Total INT,
#     SUCCESS_unique INT, 
#     MERCHANT_SUSPENDED_unique INT, 
#     HIVEX_UNAVAILABLE_MERCHANT_unique INT, 
#     Dynamic_QR_unique INT, 
#     P2P_unique INT, 
#     Others_unique INT, 
#     Total_unique INT, 
#     PRIMARY KEY (id, time)
# )
# '''

cursor.execute(create_raw_table)
# cursor.execute(create_analysis_table)

connection.commit()

cursor.close()
connection.close()