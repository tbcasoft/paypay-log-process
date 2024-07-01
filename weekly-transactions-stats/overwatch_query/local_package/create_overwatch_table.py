import mysql.connector

def create_table():
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

def add_api_termination():
    connection = mysql.connector.connect(
    host='visa-fx-05006aa44b45542b.elb.ap-southeast-1.amazonaws.com',
    port='1234',
    database='hour_qr',
    user='aws_lambda',
    password='&o17r%FK$Ft8'
    )

    cursor = connection.cursor()

    modify_dashboard_table = '''
    ALTER TABLE daily_overwatch_dashboard
    ADD termination_OPT_OUT INT NOT NULL,
    ADD termination_EXPIRED_CODE INT NOT NULL,
    ADD termination_ACQUIRER_VALIDATION INT NOT NULL;
    '''

    cursor.execute(modify_dashboard_table)

    connection.commit()

    cursor.close()
    connection.close()

def add_acquire_column():
    connection = mysql.connector.connect(
    host='visa-fx-05006aa44b45542b.elb.ap-southeast-1.amazonaws.com',
    port='1234',
    database='hour_qr',
    user='aws_lambda',
    password='&o17r%FK$Ft8'
    )

    cursor = connection.cursor()

    create_dashboard_table = '''
    CREATE TABLE IF NOT EXISTS copy_of_daily_overwatch_dashboard (
    date VARCHAR(20) NOT NULL,
    acquier VARCHAR(5) NOT NULL,
    issuer VARCHAR(5) NOT NULL, 
    rejected_job_models_invoice_count INT NOT NULL, 
    rejected_jobmodels_RFP_count INT NOT NULL,
    api_gen_target_count INT NOT NULL, 
    payments_CPM_count INT NOT NULL, 
    payments_CPM_dest_amount DECIMAL(15, 6) NOT NULL,
    payments_MPM_count INT NOT NULL, 
    payments_MPM_dest_amount DECIMAL(15, 6) NOT NULL,
    refunds_count INT NOT NULL, 
    refunds_sum_of_amount INT NOT NULL,
    termination_OPT_OUT INT NOT NULL,
    termination_EXPIRED_CODE INT NOT NULL,
    termination_ACQUIRER_VALIDATION INT NOT NULL,
    PRIMARY KEY (date, acquier issuer)
    );
    '''

    cursor.execute(create_dashboard_table)

    connection.commit()

    cursor.close()
    connection.close()
add_api_termination()