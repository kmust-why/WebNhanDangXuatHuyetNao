from django.db import connection

class DBConnect:

    def getTable(self, Query):
        with connection.cursor() as cursor:
            cursor.execute(Query)
            row = cursor.fetchall()
        return row

    def noneGetTable(self, Query):
        with connection.cursor() as cursor:
            cursor.execute(Query)
            row = cursor.fetchone()    
        return row    