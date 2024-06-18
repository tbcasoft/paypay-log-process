import mysql.connector

connection = mysql.connector.connect(
    host='visa-fx-05006aa44b45542b.elb.ap-southeast-1.amazonaws.com',
    port='1234',
    database='hour_qr',
    user='aws_lambda',
    password='&o17r%FK$Ft8'
)

cursor = connection.cursor()

create_dashboard_table = '''
CREATE TABLE IF NOT EXISTS daily_overwatch_dashboard (
    id INT AUTO_INCREMENT,
    time VARCHAR(20),
    issuer VARCHAR(5), 
    rejected_job_models_invoice_count INT, 
    rejected_jobmodels_RFP_count INT,
    api_gen_target_count INT, 
    payments_CPM_count INT, 
    payments_CPM_dest_amount DECIMAL(15, 6),
    payments_MPM_count INT, 
    payments_MPM_dest_amount DECIMAL(15, 6),
    refunds_count INT, 
    refunds_sum_of_amount INT,
    PRIMARY KEY (id, time, issuer)
)
'''

cursor.execute(create_dashboard_table)

connection.commit()

cursor.close()
connection.close()