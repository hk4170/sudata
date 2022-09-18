import sqlite3
class sqlite:
    def __init__(self,dbfile=None):
        if not dbfile:
            dbfile = 'data.db'
        self.conn = sqlite3.connect(dbfile)
        self.sql = self.conn.cursor()

    def get_tables(self):
        table = self.sql.execute("select name from sqlite_master where type='table' order by name")
        tables = []
        if not table:
            return None
        for i in table:
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
        query = ct + cs + ce
        try :
            self.sql.execute(query)
        except:
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
        item = self.get_table_item(table)
        self.delete_table(table)
        if self.create_table(table,item):
            return True
        else:
            return 
    
    def get_table_info(self,table):
        try:
            res = self.sql.execute('PRAGMA table_info({})'.format(table))
        except :
            return None
        info = []
        for i in res:
            info.append(i)
        return info
                                                       
    def get_table_item(self,table):
        table_info = self.get_table_info(table)
        if not table_info:
            return None
        item = []
        for i in table_info:
            item.append(i[1])
        return item
    
    def add_table_item(self,table,item,item_type):
        query = "alter table {} add {} {}" .format(table,item,item_type)
        try:
            self.sql.execute(query)
            self.conn.commit()
        except :
            return 
        return True
    
    def delete_table_item(self,table,item):
        table_item = self.get_table_item(table)
        data = self.get(table)
        if not table_item :
            return 
        elif item not in table_item:
            return 
        else:
            table_item.remove(item)
            if self.delete_table(table):
                self.create_table(table,table_item)
                self.insert(table,data)
                return True
            else:
                return 
            
    def get(self,table,where=None):
        table_item = self.get_table_item(table)
        if not where:
            query = 'select * from {}'.format(table)
        else:
            query = 'select * from {} where {}'.format(table,where)
        try : 
            datas =  self.sql.execute(query).fetchall()
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

    def filter_repeat(self,data):
        if not data:
            return
        data = list(data)
        for i in data:
            while data.count(i) > 1:
                data.remove(i)
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
        e = '?,' * len(table_item) 
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
        query ="delete from {} where {}".format(table,where)
        try:
            self.sql.execute(query)
            self.conn.commit()
        except :
            return 
        return True
        
    def select(self,table,item=None,where=None):
        datas = self.get(table,where=where)
        if not datas:
            return None
        if not item:
            return datas
        data  = []
        for d in datas:
            ds = {}.fromkeys(item)
            for i in item:
                if not d[i]:
                    continue
                ds[i] = d[i]
            data.append(ds)
        return data
                
    def update(self,table,where,data):
        if self.delete(table,where):
            self.insert(table,data)
            self.conn.commit()
            return True
        else:
            return 
