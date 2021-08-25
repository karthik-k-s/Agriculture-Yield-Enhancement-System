from flask_mysqldb import MySQL
import mysql.connector


mydb = mysql.connector.connect(
host="localhost",
user="root",
passwd="Alohomora")
mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE test2")
mycursor.execute("USE agriculture")
#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
mycursor.execute("create table IF NOT EXISTS farmer (fid bigint auto_increment primary key, username varchar(50), email varchar(40),mobileno varchar(10),lang varchar(20),pass varchar(20), doc int(3))")
mycursor.execute("create table IF NOT EXISTS crop(crop_id int auto_increment primary key,crop_name varchar(50),nit_req double(7,2),phosp_req double(7,2),potash_req double(7,2));")
mycursor.execute("create table IF NOT EXISTS land(lid int auto_increment primary key,land_size double(15,2),nit_req double(15,2),phosp_req double(15,2),potash_req double(15,2),fk_fid bigint,foreign key(fk_fid) references farmer(fid) ON DELETE CASCADE);")
mycursor.execute("create table IF NOT EXISTS region(did bigint auto_increment primary key,district_name varchar(50),crops_grown varchar(40))")

mycursor.execute("insert into land values(default,2.5,195.99,25.89,135.81,1);")



mycursor.execute("insert into crop values(default,'Groundnut',25,20,30);")
mycursor.execute("insert into crop values(default,'Cotton',100,50,50);")
mycursor.execute("insert into crop values(default,'Paddy',150,50,50);")
mycursor.execute("insert into crop values(default,'Ragi',60,30,30);")
mycursor.execute("insert into crop values(default,'Maize',150,75,40);")
mycursor.execute("insert into crop values(default,'Wheat',120,60,40);")
mydb.commit()
mycursor.close()