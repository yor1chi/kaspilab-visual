from DB import Values, Views

if __name__ == '__main__':
    url1, url2, url3 = 'indexData.csv', 'indexInfo.csv', 'indexProcessed.csv'
    Values.setData(url1, url2, url3)
    Views.notProcessed()
    Views.Processed()
