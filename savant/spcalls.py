from models import DBconn
import sys


class SPcalls:
    def __init__(self):
        pass

    def spcall(self, qry, param, commit=False):
        qry = qry
        param = param

        try:
            dbo = DBconn()
            cursor = dbo.getcursor()
            cursor.callproc(qry, param)
            res = cursor.fetchall()
            if commit:
                dbo.dbcommit()
            return res

        except:
            res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]
            print "res", res
        return res


