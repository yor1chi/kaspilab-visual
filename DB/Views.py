import cx_Oracle
import pandas as pd

connectionData = cx_Oracle.connect(user='User Name', password='Password name',
                                   dsn='localhost:1521/xe', encoding='UTF-8')


def notProcessed():
    try:
        with connectionData.cursor() as cursor:
            sqlSetView = """CREATE OR REPLACE VIEW V_NOTPROCESSED AS SELECT i.region, i.exchange, d.openprice,
                     d.highestprice, d.lowestprice, d.closeprice, d.adj_close,
                     ROW_NUMBER() OVER (PARTITION BY i.region ORDER BY i.region) RowNumber
                     FROM data d JOIN info i ON d.stockindex = i.stockindex
                     WHERE d.volume IS NULL AND d.key NOT IN (SELECT key FROM processed)"""
            cursor.execute(sqlSetView)
        sqlGetView = """SELECT * FROM V_NOTPROCESSED"""
        notProcessed = pd.read_sql(sqlGetView, connectionData)
        notProcessed.to_html('Views/V_NOTPROCESSED.html')
        print('Check V_NOTPROCESSED html file to see the view')
    except cx_Oracle.Error as error:
        print('Error has occurred:')
        print(error)


def Processed():
    try:
        sqlSetView = """CREATE OR REPLACE VIEW V_PROCESSED AS SELECT i.region, EXTRACT(YEAR FROM p.biddate) "Year", 
        EXTRACT(MONTH FROM p.biddate) "Month", i.exchange, MAX(p.openprice) "Maximal opening price", 
        MIN(p.lowestprice) "Minimal price over period", i.currency
        FROM processed p JOIN info i ON i.stockindex = p.stockindex
        GROUP BY i.region, EXTRACT(YEAR FROM p.biddate), EXTRACT(MONTH FROM p.biddate),
        i.exchange, i.currency
        ORDER BY region, EXTRACT(YEAR FROM p.biddate), EXTRACT(MONTH FROM p.biddate)"""
        with connectionData.cursor() as cursor:
            cursor.execute(sqlSetView)
        sqlGetView = """SELECT * FROM V_PROCESSED"""
        processed = pd.read_sql(sqlGetView, connectionData)
        processed.to_html('Views/V_PROCESSED.html')
        print('Check V_PROCESSED html file to see the view')
    except cx_Oracle.Error as error:
        print('Error has occurred:')
        print(error)
