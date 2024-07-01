import pymysql
import os

def create_issuers_table():
    db_connection = pymysql.connect(
        host=os.environ["db_host"],
        port=int(os.environ["db_port"]),
        database=os.environ["db_name"],
        user=os.environ["db_username"],
        password=os.environ["db_password"]
    )

    cursor = db_connection.cursor()

    create_dashboard_table = '''
    CREATE TABLE IF NOT EXISTS hivex_system_report_issuers (
    week_date VARCHAR(20) NOT NULL,
    acquier VARCHAR(5) NOT NULL,
    issuer VARCHAR(5) NOT NULL, 
    get_invoice_latency_median DECIMAL(7, 1) NOT NUll,
    get_invoice_latency_p99 DECIMAL(7, 1) NOT NUll,
    pay_latency_median DECIMAL(7, 1) NOT NUll,
    pay_latency_p99 DECIMAL(7, 1) NOT NUll,
    conf_page_latency_median DECIMAL(7, 1) NOT NUll,
    conf_page_latency_p99 DECIMAL(7, 1) NOT NUll,
    PRIMARY KEY (week_date, acquier, issuer)
    )
    '''

    cursor.execute(create_dashboard_table)

    db_connection.commit()

    cursor.close()
    db_connection.close()
    

def create_weekly_stat_table():
    db_connection = pymysql.connect(
        host=os.environ["db_host"],
        port=int(os.environ["db_port"]),
        database=os.environ["db_name"],
        user=os.environ["db_username"],
        password=os.environ["db_password"]
    )

    cursor = db_connection.cursor()

    create_dashboard_table = '''
    CREATE TABLE IF NOT EXISTS hivex_system_report_weekly_stat (
    week_date VARCHAR(20) NOT NULL,
    data_name VARCHAR(50) NOT NULL,
    data_value VARCHAR(20) NOT NULL,
    PRIMARY KEY (week_date, data_name)
    )
    '''

    cursor.execute(create_dashboard_table)

    db_connection.commit()

    cursor.close()
    db_connection.close()