import pymysql

con = pymysql.connect(host='localhost',user='root',passwd=''
,db='songkhla_welcome_arrival')
cs = con.cursor()

# create tbl Country
# cs.execute("""
# create table country(
# id int auto_increment not null primary key,
# prefix varchar(5) not null,
# country varchar(255) not null
# )
# """)

# create tbl province
# cs.execute("""
# create table th_province(
# id int auto_increment not null primary key,
# th_province varchar(255) not null,
# en_province varchar(255) not null
# )
# """)
#
# cs.execute("""
# create table en_province(
# id int auto_increment not null primary key,
# code varchar(5) not null,
# prefix varchar(5) not null,
# province varchar(255) not null
# )
# """)

# cs.execute("""
# create table district(
# id int auto_increment not null primary key,
# th_district varchar(255) not null,
# en_district varchar(255) not null
# )
# """)
#
# cs.execute("""
# create table subdistrict(
# id int auto_increment not null primary key,
# th_subdistrict varchar(255) not null,
# en_subdistrict varchar(255) not null
# )
# """)

# cs.execute("""
# create table Depart(
# id int auto_increment not null primary key,
# subdistrict int null,
# district int null,
# th_province int null,
# en_province int null,
# country int null
# )
# """)
#
# cs.execute("""
# create table destination(
# id int auto_increment not null primary key,
# subdistrict int not null,
# district int not null,
# th_province int not null
# )
# """)
#
# cs.execute("""
# create table categories(
# id int auto_increment not null primary key,
# code varchar(5) not null,
# category varchar(255) not null
# )
# """)
#
# cs.execute("""
# create table linename(
# id int auto_increment not null primary key,
# prefix varchar(5) not null,
# linename varchar(255) not null,
# category int not null,
# foreign key(category) references categories(id)
# )
# """)
#
# cs.execute("""
# create table flight_tbl(
# id int auto_increment not null primary key,
# prefix varchar(5) not null,
# number varchar(255) not null,
# linename int not null,
# dep_time datetime not null,
# des_time datetime not null,
# depart_from int not null,
# destination int not null
# )
# """)

# cs.execute("""
# create table personal(
# id int auto_increment not null primary key,
# fname varchar(255) not null,
# lname varchar(255) not null,
# citizen_id varchar(20) not null,
# image varchar(255) not null,
# phonenumber char(10) not null,
# updated_at datetime not null
# )""")
#
# cs.execute("""
# create table arrival_infromation(
# id int auto_increment not null primary key,
# dep_time datetime not null,
# des_time datetime not null,
# depart_from int not null,
# destination int not null,
# personal int not null,
# flight_number int null
# )
# """)
#
# # altertbl
# cs.execute("""alter table depart add foreign key(subdistrict) references
# subdistrict(id)""")
# cs.execute("""alter table depart add foreign key(district) references
# district(id)""")
# cs.execute("""alter table depart add foreign key(th_province) references
# th_province(id)""")
# cs.execute("""alter table depart add foreign key(en_province) references
# en_province(id)""")
# cs.execute("""alter table depart add foreign key(country) references
# country(id)""")
#
# # destination tbl
# cs.execute("""alter table destination add foreign key(subdistrict) references
# subdistrict(id)""")
# cs.execute("""alter table destination add foreign key(district) references
# district(id)""")
# cs.execute("""alter table destination add foreign key(th_province) references
# th_province(id)""")
#
# # flight tbl
# cs.execute("""alter table flight_tbl add foreign key(linename) references
# linename(id)""")
# cs.execute("""alter table flight_tbl add foreign key(depart_from) references
# depart(id)""")
# cs.execute("""alter table flight_tbl add foreign key(destination) references
# destination(id)""")
#
# # arrival
# cs.execute("""alter table arrival_infromation add foreign key(depart_from) references
# depart(id)""")
# cs.execute("""alter table arrival_infromation add foreign key(destination) references
# destination(id)""")
# cs.execute("""alter table arrival_infromation add foreign key(personal) references
# personal(id)""")
# cs.execute("""alter table arrival_infromation add foreign key(flight_number) references
# flight_tbl(id)""")
#

cs.execute("""
create table airport(
id int auto_increment not null primary key,
prefix varchar(5) not null,
airport varchar(255) not null
)
""")

con.commit()
con.close()
print("success create database")
