import pymysql
class mysql:
    def __init__(self,
        db,
        host='localhost',
        user='root',
        port=3306,
        password=None,
        charset='utf8'):
        self.conn = pymysql.connect(
            host = host,
            user = user,
            port = port,
            password = password,
            database = db,
            charset = charset
        )
        self.sql =self.conn.cursor()

    def get_version(self):
        self.sql.execute("SELECT VERSION()")
        data = self.sql.fetchone()
        return "version : {}".format(data[0])
    
    def get_tables(self):
        res = self.sql.execute("show tables")
        table_res = self.sql.fetchall()
        tables = []
        if not table_res:
            return None
        for i in table_res:
            tables.append(i[0])
        return tables

    def create_table(self,table,item):
        if not table.strip() or not item:
            return 
        ct = "create table {} (".format(table)
        ca = []
        try :
            keys = list(item.keys())
        except :
            for i in item:
                a = "{} text ,".format(i)
                if i == item[-1]:
                    a = "{} text".format(i)
                ca.append(a)
        else:
            for i in keys:
                a = "{} {} ,".format(i,item[i])
                if i == keys[-1]:
                    a = "{} {}".format(i,item[i])
                ca.append(a)  
        cs = "".join(ca)
        ce =  ")"
        en = 'ENGINE=innodb DEFAULT CHARSET=utf8;'
        query = ct + cs + ce + en
        try :
            self.sql.execute(query)
        except:
            self.conn.rollback()
            return 
        return True  

    def delete_table(self,table):
        query ='drop table {}'.format(table)
        try:
          self.sql.execute(query)      
        except :
            return 
        return True

    def empty_table(self,table):     
        if table in self.get_tables():
            self.sql.execute("truncate {}".format(table))
            return True
        else:
            return 

    def get_table_info(self,table):
        try:
            res = self.sql.execute('desc {}'.format(table))
        except :
            return None
        info = []
        result = self.sql.fetchall()
        for i in result:
            info.append(i)
        return info                

    def get_table_item(self,table):
        table_info = self.get_table_info(table)
        if not table_info:
            return None
        item = []
        for i in table_info:
            item.append(i[0])
        return item   

    def filter_repeat(self,data):
        if not data:
            return
        data = list(data)
        for i in data:
            while data.count(i) > 1:
                data.remove(i)
        return data
    
    def get(self,table,where=None):
        table_item = self.get_table_item(table)
        if not where:
            query = 'select * from {}'.format(table)
        else:
            query = 'select * from {} where {}'.format(table,where)
        try :
            self.sql.execute(query)
            datas =  self.sql.fetchall()
        except :
            return  
        data = []
        if not datas:
            return
        for i in datas:
            d = {}.fromkeys(table_item)
            for v in range(len(table_item)):
                d[table_item[v]] = i[v]
            data.append(d)
        return data
    
    def insert(self,table,data):
        data = self.filter_repeat(data)
        table_item = self.get_table_item(table)
        if not table_item:
            return 
        q = 'insert into {} ('.format(table)
        u = []
        for i in table_item:
            a = '{},'.format(i)
            if i == table_item[-1]:
                a = '{}) values('.format(i)
            u.append(a)
        e = '%s,' * len(table_item) 
        r = q + ''.join(u) + e
        y = list(r)
        y[-1] = ')'
        query = ''.join(y)
        if not data:
            return
        for d in data:
            datas = []
            for i in table_item:
                try:
                    datas.append(d[i])
                except : 
                    datas.append(None)
            datas = tuple(datas)
            try :
                self.sql.execute(query,datas)
                self.conn.commit()
            except : return 
        return True   

    def delete(self,table,where):
        if not where :
            return 
        query ="delete from {} where {}".format(table,where)
        try:
            self.sql.execute(query)
            self.conn.commit()
        except :
            return 
        return True
                
    def update(self,table,data,where=None):
        if data == self.get(table):
            return 
        if where :
            self.empty_table(table)
            self.insert(table,data)
        else:
            if self.delete(table,where):
                self.insert(table,data)
                self.conn.commit()
                return True
            else:
                return 
