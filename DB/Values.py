import cx_Oracle
import csv
from datetime import datetime

connectionData = cx_Oracle.connect(user='User Name', password='Password name',
                                   dsn='localhost:1521/xe', encoding='UTF-8')


def setData(url1, url2=None, url3=None):
    try:
        connection = connectionData
        with connection.cursor() as cursor:
            with open(url1, "r") as csv_file:
                csvReader = csv.reader(csv_file)
                next(csvReader)
                for lines in csvReader:
                    lines[2] = datetime.strptime(lines[2], '%Y-%m-%d')
                    for i in range(3, 9):
                        if lines[i] == 'null':
                            lines[i] = ''
                        lines[i] = lines[i].replace('.', ',')
                    cursor.execute(
                        "INSERT INTO data (Key, StockIndex, BidDate, OpenPrice, HighestPrice, "
                        "LowestPrice, ClosePrice, Adj_close, Volume) "
                        "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)",
                        (lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], lines[6], lines[7], lines[8]))
            connection.commit()
            print('Insertion into table executed successfully!')

            if url2:
                with connection.cursor() as cursor:
                    with open(url2, "r") as csv_file:
                        csvReader = csv.reader(csv_file)
                        next(csvReader)
                        for lines in csvReader:
                            cursor.execute(
                                "INSERT INTO info (Region, Exchange, StockIndex, Currency) "
                                "VALUES (:1, :2, :3, :4)",
                                (lines[0], lines[1], lines[2], lines[3]))
                    connection.commit()
                    print('Insertion into table executed successfully!')

            if url3:
                with connection.cursor() as cursor:
                    with open(url3, "r") as csv_file:
                        csvReader = csv.reader(csv_file)
                        for lines in csvReader:
                            lines[2] = datetime.strptime(lines[2], '%Y-%m-%d')
                            for i in range(3, 10):
                                if lines[i] == 'null':
                                    lines[i] = ''
                                lines[i] = lines[i].replace('.', ',')
                            cursor.execute(
                                "INSERT INTO processed (Key, StockIndex, BidDate, OpenPrice, HighestPrice, LowestPrice,"
                                " ClosePrice, Adj_close, Volume, CloseUSD) "
                                "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)",
                                (lines[0], lines[1], lines[2], lines[3], lines[4], lines[5],
                                 lines[6], lines[7], lines[8], lines[9]))
                    connection.commit()
                    print('Insertion into table executed successfully!')
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)
