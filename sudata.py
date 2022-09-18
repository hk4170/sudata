#!/usr/bin/python3
from csvloader import csvloader
from mysql import mysql
from sqlite import sqlite 
import fire
import csv
from os.path import isdir
from os.path import isfile
from os import mkdir, system,listdir

class sudata:
    def db2csv(self,dbfile,table=None,zip=False):
        db = sqlite(dbfile)
        if table : 
            fload = '.'
        else:
            fload = dbfile.split('.')[0]
            if not isdir(fload):
                mkdir(fload)
        for tables in db.get_tables():
            if table and tables != table:
                continue 
            data = db.get(tables)
            item = db.get_table_item(tables)
            csv_file = '{}/{}.csv'.format(fload,tables)
            with open(csv_file,'w') as file:
                write = csv.DictWriter(file,item)
                write.writeheader()
                write.writerows(data)
                print("table:{} Done".format(tables))
        if zip:
            with zipfile.ZipFile("{}.zip".format(fload),'w') as zfile:
                for file in listdir(fload):
                    zfile.write('{}/{}'.format(fload,file))
                zfile.close()
            system("rm -rf {} ".format(fload))            
            print("Store in {}.zip".format(fload))

    def db2mysql(self,dbfile,mysqldb=None,host=None,user=None,password=None):
        db = sqlite(dbfile)
        if not mysqldb:
            mysqldb = dbfile.split('.')[0]
        try:
            sql = mysql(db=mysqldb,host=host,user=user,password=password)
        except:
            exit("Access denied!!")
        if not db.get_tables():
            return 
        for table in db.get_tables():
            sqltables = sql.get_tables()
            if sqltables and table in sqltables:
                sql.empty_table(table)
            else:
                sql.create_table(table,db.get_table_item(table))
            data = db.get(table)
            if not data:
                print("table: {} Not data!!".format(table))
                continue
            if sql.insert(table,data):
                print("table: {} Done".format(table))

    def csv2db(self,csvfile,dbfile=None):
        if isdir(csvfile):
            if '/' in csvfile:
                csvfile = csvfile.split("/")[0]
            files = []
            for file in listdir(csvfile):
                file = "{}/{}".format(csvfile,file)
                files.append(file)
            if not dbfile:
                dbfile = '{}.db'.format(csvfile.split('/')[0])
        elif isfile(csvfile):
            files = []
            files.append(csvfile)
            csvfile = '.'
            if not dbfile:
                print("Not set --dbfile!!!")
                print("Store in data.db")
        db = sqlite(dbfile)
        for file in files:
            data = csvloader(file)
            try:
                table_name = file.split('/')[1].split('.')[0]
            except:
                table_name = file.split('.')[0]
            try:
                db.create_table(table_name,data.header)
            except: continue
            if db.insert(table_name,data):
                print("table: {} Done!".format(table_name))
            else:
                exit("Error !!!")

    def csv2mysql(self,csvfile,table=None,mysqldb=None,host=None,user=None,password=None):
        if isdir(csvfile):
            files = []
            for file in listdir(csvfile):
                file = "{}/{}".format(csvfile,file)
                files.append(file)
            if not mysqldb:
                mysqldb = csvfile.split('/')[0]
        elif isfile(csvfile):
            files = []
            files.append(csvfile)
            csvfile = '.'
            if not mysqldb:
                exit("Error Need set --mysqldb !!!")
        sql = mysql(db=mysqldb,host=host,user=user,password=password)
        for file in files:
            data = csv_loader(file)
            try:
                table_name = file.split('/')[1].split('.')[0]
            except:
                table_name = file.split('.')[0]

            sql.create_table(table_name,data.header)
            if sql.insert(table_name,data):
                print("table: {} Done!".format(table_name))
            else:
                exit("Error !!!")
       
    def mysql2csv(self,mysqldb,csv_dir=None,table=None,host=None,user=None,password=None,zip=False):
        try:
            sql = mysql(mysqldb,host=host,user=user,password=password)
        except:
            exit("Access Denied !!!")
        if table :
            fload = '.'
        else:
            if not csv_dir:
                fload = mysqldb
            else:
                fload = csv_dir
            if not isdir(fload):
                mkdir(fload)
        if not sql.get_tables(): 
            exit("Not table !!")
        for tables in sql.get_tables():
            if table and table != tables:
                continue
            with open('{}/{}.csv'.format(fload,tables),'w',encoding='utf-8') as file:
                data = sql.get(tables)
                item = sql.get_table_item(tables)
                write = csv.DictWriter(file,item)
                write.writeheader()
                if data:
                    write.writerows(data)
            print('table: {} Done!'.format(tables))
        if zip:
            with zipfile.ZipFile("{}.zip".format(fload),'w') as zfile:
                for file in listdir(fload):
                    zfile.write('{}/{}'.format(fload,file))
                zfile.close()
            system("rm -rf {} ".format(fload))            
            print("Store in {}.zip".format(fload))

    def mysql2db(self,mysqldb,dbfile=None,host=None,user=None,password=None):
        try:
            sql = mysql(mysqldb,host=host,user=user,password=password)
        except:
            exit("Access Denied !!!")
        if not dbfile:
            dbfile = '{}.db'.format(mysqldb)
        db = sqlite(dbfile)
        if not sql.get_tables():
            exit("Not table!!")
        for table in sql.get_tables():
            data = sql.get(table)
            item = sql.get_table_item(table)
            db.create_table(table,item)
            if not data:
                print("table: {} Not data!".format(table))
                continue
            if db.insert(table,data):
                print('table: {} Done!'.format(table))

    def mysql_excel():
        pass
    
if __name__ == '__main__':
    fire.Fire(sudata)