import json
import pyodbc

def sql2dict(query):
    print("fetching data")
    result = []
    try:
        constr = 'DRIVER={SQL Server};SERVER=192.168.1.154\SQLEXPRESS01;DATABASE=EggitTouch-JB10337;UID=sa;PWD=asdasd'
        conn = pyodbc.connect(constr)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        for row in data:
            result.append(dict(zip(column_names, row)))
            print(row)
        conn.close()
    except Exception as e:
        print(e)
    return result

def fetch_data():
    print("fetching data")
    try:
        # constr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.154\SQLEXPRESS01;DATABASE=EggitTouch-JB10337;UID=sa;PWD=asdasd'
        constr = 'DRIVER={SQL Server};SERVER=192.168.1.154\SQLEXPRESS01;DATABASE=EggitTouch-JB10337;UID=sa;PWD=asdasd'
        conn = pyodbc.connect(constr)
        cursor = conn.cursor()
        cursor.execute("select * from HstSupplierCount")
        for row in cursor.fetchall():
            print(row)
        conn.close()
    except Exception as e:
        print(e)


def fetch_data_asdict():
    return sql2dict("select * from HstSupplierCount")

def fetch_grouped_data_asdict():
    return sql2dict("""select
    sum(d.HsdWeight) as HsdWeight,
    sum(d.HsdGradeLimit) as HsdGradeLimit,
    sum(d.HsdCount) as HsdCount,
    sum(d.HsdInfeedWeight) as HsdInfeedWeight,
    d.HsdGradeName,
    case when sum(d.HsdCount) > 0 then sum(d.HsdWeight) / sum(d.HsdCount) end as Ortalama
    ,s.SuiName
    ,h.HscId
    from HstSupplierCountDetail d
    inner join HstSupplierCount h on h.HscId = d.HsdParentId
    inner join GrdSupplierInfo s on s.SuiId = h.HscSuiId
    where 1=1
    group by d.HsdGradeName, h.HscId, s.SuiName
    """)