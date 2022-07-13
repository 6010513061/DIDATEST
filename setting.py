from flask import Flask,render_template,redirect,request,url_for,session
from werkzeug.utils import secure_filename
import bcrypt
import pymysql
import os
from datetime import datetime,date,timedelta,date,time
import requests
from pytesseract import pytesseract
from PIL import Image
from flight import get_api


con = pymysql.connect(host='localhost',user='root',passwd=''
,db='songkhla_welcome_arrival')
cursor = con.cursor()

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config['UPLOAD_FOLDER']='static/uploads'
ALLOWED_EXTENDSION = set(['jpeg','jpg','png','gif'])
path_to_tst = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# valid file image citizen
def allowed_file(file):
    return file.rsplit('.',1)[1].lower() in ALLOWED_EXTENDSION

# read image to str
def validate_imge_id(file):
    lst_id = []
    img = Image.open(os.path.join(app.config['UPLOADS_FOLDER'],file.filename))
    pytesseract.tesseract_cmd = path_to_tst
    txt = pytesseract.image_to_string(img)
    lst_id.append(txt)
    print(lst_id)
# check escape string
def check_escape(*args):
    lst_escape = ['\'','"','\\','/','#','!','&','$','*','%']
    for es in lst_escape:
        for ar in args:
            return es in ar

# check empty
def check_empty(*args):
    for ar in args:
        return not ar

# fetch data
def fetch_data(slc,tbl,order):
    place = "select {sl} from {tbl} order by {r} ASC".format(sl=slc,tbl=tbl,r=order)
    cursor.execute(place)
    fet_place = cursor.fetchall()
    return fet_place

# fetch Arrival
def fetch_arrival():
    arrival = "select id from Arrival_infromation"
    cursor.execute(arrival)
    fet_arr = cursor.fetchall()
    return fet_arr


# insert arrive
def insert_destination_th(*args):
    insert_depart = """insert into destination(arrive_time,subdistrict,district,province)
    values(%s,%s,%s,%s)"""
    lst_data = []
    for i in args:
        lst_data.append(i)
    cursor.execute(insert_depart,(lst_data))
    con.commit()

# insert destination national
def insert_depart_from(*args):
    insert_depart = """insert into destination(arrive_time,subdistrict
    ,district,province,country,nation_province)
    values(%s,%s,%s,%s)"""
    lst_data = []
    for i in args:
        lst_data.append(i)
    cursor.execute(insert_depart,(lst_data))
    con.commit()

# read jpeg to text
def validate_citizen(name):
    doc = aw.Document()
    build = aw.DocumentBuilder(doc)
    builder.insert_image(name)
    doc.save('output.txt')

# confirm display
# add in lst
def add_data(*args):
    lst_data=[]
    for i in args:
        lst_data.append(i)
    return display_lst(lst_data)

# display defore save
def display_lst(lst_data):
    return lst_data

#render_template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/EN')
def insert_data_en():
    return render_template('insert_arrival_eng.html'
    ,type=fetch_data(slc='*',tbl='categories',order='id')
    ,flight=fetch_data(slc='*',tbl='flight_tbl',order='des_time')
    ,dis=fetch_data(slc='*',tbl='district',order='th_district')
    ,sub=fetch_data(slc='*',tbl='subdistrict',order='th_subdistrict')
    ,pro=fetch_data(slc='*',tbl='th_province',order='th_province')
    ,country=fetch_data(slc='*',tbl='country',order='country')
    ,enpro=fetch_data(slc='*',tbl='en_province',order='code'))

# webpage for thai
@app.route('/TH')
def insert_data_th():
    return render_template('insert_arrival.html'
    ,type=fetch_data(slc='*',tbl='categories',order='id')
    ,flight=fetch_data(slc='*',tbl='flight_tbl',order='des_time')
    ,dis=fetch_data(slc='*',tbl='district',order='th_district')
    ,sub=fetch_data(slc='*',tbl='subdistrict',order='th_subdistrict')
    ,pro=fetch_data(slc='*',tbl='th_province',order='th_province')
    ,country=fetch_data(slc='*',tbl='country',order='country')
    ,enpro=fetch_data(slc='*',tbl='en_province',order='code'))

def select_id_d(sbd,dt,tpv,con):
    print(con)
    if sbd=="" or dt=="" or tpv=="":
        dp = """select id from depart where %s"""
        cursor.execute(dp,con)
        fet_dp = cursor.fetchall()
    else:
        dp = """select id from depart where subdistrict=%s and district=%s
        and th_province=%s"""
        cursor.execute(dp,(sbd,dt,tpv))
        fet_dp = cursor.fetchall()
    return fet_dp

def select_id_ds(sbd,dt,tpv):
    dp = """select id from destination where subdistrict=%s and district=%s
    and th_province=%s"""
    cursor.execute(dp,(sbd,dt,tpv))
    fet_dp = cursor.fetchall()
    return fet_dp

@app.route('/addflight')
def add_flight():
    m_api = get_api()
    am = m_api.api()
    pm = m_api.api2()
    line = am["arrivals"]
    num = fetch_data(slc="number",tbl='numbers',order='id')
    while datetime.now() <= datetime.strptime('18:00','%H:%M'):
        for i in range(len(line)):
            if line[i]["number"] not in num:
                insert = """insert into numbers(prefix,number) values(%s,%s)"""
                cursor.execute(insert,(str(line[i]["number"])[0:2],line[i]["number"]))
            sel_depart = """select depart.en_province from depart,
            th_province,en_province where th_province.en_province=%s or en_province.province=%s"""
            cursor.execute(sel_depart,(line[i]["airline"]["name"],line[i]["airline"]["name"]))
            fet_pro = cursor.fetchall()
            # fetch thid
            sel_thid = """select id from th_province where en_province=%s"""
            cursor.execute(sel_thid,line[i]["airline"]["name"])
            fet_thid = cursor.fetchall()
            # fetch enid
            num_like = """select id from numbers where number=%s"""
            cursor.execute(num_like,line[i]["number"])
            fet_numlike = cursor.fetchone()
            line_like = """select id from linename where linename=%s"""
            cursor.execute(line_like,line[i]["airline"]["name"])
            fet_linelike = cursor.fetchone()
            # select airport id
            air_like = """select id,location,prefix from airport where iata=%s"""
            cursor.execute(air_like,line[i]["airport"]["iata"])
            fet_air = cursor.fetchall()
            location=None
            id=None
            prefix = None
            for f in fet_air:
                id = f[0]
                prefix=f[2]
                location = f[1]
            if prefix=="TH":
                pro = """select id from th_province where en_province=%s"""
                cursor.execute(pro,location)
                fet_pro = cursor.fetchone()
            else:
                pro = """select id from en_province where province=%s"""
                cursor.execute(pro,location)
                fet_pro = cursor.fetchone()
            insert_flight = """insert into flight_tbl(number,linename
            ,dep_time,des_time,depart_from,destination) values(%s,%s,%s,%s,%s,%s)"""
            cursor.execute(insert_flight,(fet_numlike,fet_linelike
            ,line[i]["departure"]["scheduledTimeLocal"],line[i]["arrival"]["scheduledTimeLocal"]
            ,fet_pro,'90'))
            con.commit()
            print("success")
    else:
        line = pm['arrivals']
    print("can not update")
    return redirect(url_for('index'))

    # lst = j["arrivals"][0]
    # print(lst["departure"]["airport"])
    # print(j["arrivals"][0]["number"])


# insert data add in database
# @app.route('/addflight',methods=['POST','GET'])
# def add_trans():
#     if request.method=="POST":
#         line = request.form['linename']
#         num = request.form['number']
#         ddate = request.form['ddate']
#         dcountry = request.form['dcountry']
#         dth_province = request.form['dth_province']
#         den_province = request.form['den_province']
#         print("den:",den_province)
#         ddistrict = request.form['ddistrict']
#         dsubdistrict = request.form['dsubdistrict']
#         # destination
#         dsprovince = request.form['dsprovince']
#         dsdistrict = request.form['dsdistrict']
#         dssubdistrict = request.form['dssubdistrict']
#         dsdate = request.form['dsdate']
#         error = None
#         if check_empty(line,num,ddate)==True:
#             error = "กรุณากรอกข้อมูลให้ครบถ้วน!"
#         elif check_empty(dsdate,dsprovince,dsdistrict,dssubdistrict)==True:
#             error = "กรุณากรอกข้อมูลให้ครบถ้วน!"
#         if error is None:
#             conn="country='{c}' and en_province='{d}'".format(c=dcountry,d=den_province)
#             depart = select_id_d(dsubdistrict,ddistrict,dth_province,conn)
#             des = select_id_ds(dssubdistrict,dsdistrict,dsprovince)
#             lst_data = []
#             if len(depart)==0:
#                 if den_province=="":
#                     insert_dp = """insert into depart(subdistrict,district
#                     ,th_province) values(%s,%s,%s)"""
#                     cursor.execute(insert_dp,(dsubdistrict,ddistrict,dth_province))
#                     con.commit()
#                 else:
#                     insert_dp2 = """insert into depart(country,en_province)
#                     values(%s,%s)"""
#                     cursor.execute(insert_dp2,(dcountry,den_province))
#                     con.commit()
#                 insert_ds = """insert into destination(subdistrict,district
#                 ,th_province) values(%s,%s,%s)"""
#                 cursor.execute(insert_ds,(dssubdistrict,dsdistrict,dsprovince))
#                 con.commit()
#             lst_data = [dsubdistrict,ddistrict,dth_province,conn,dssubdistrict
#             ,dsdistrict,dsprovince,num,line,ddate,dsdate]
#         return redirect(url_for('add_to_flight',lst_data=lst_data))
#     return redirect(url_for('add_flight'))
#
# @app.route('/adddlight/<lst_data>')
# def add_to_flight(lst_data):
#     print(lst_data)
#     conn = ""
#     if lst_data[0] is None:
#         idd = select_id_d("","","",lst_data[3])
#         print("None:",idd)
#     else:
#         idd = select_id_d(lst_data[0],lst_data[1],lst_data[2],conn)
#         print("Yes:",idd)
#         ids = select_id_ds(lst_data[4],lst_data[5],lst_data[6])
#         print('idd:',idd,"ids:",ids)
#         insert = """insert into flight_tbl(number,linename,dep_time,des_time
#         ,depart_from,destination) values(%s,%s,%s,%s,%s,%s)"""
#         cursor.execute(insert,(lst_data[7],lst_data[8],lst_data[9],lst_data[10],idd,ids))
#         con.commit()
#         session['success']="add flight successfully"
#     return redirect(url_for('add_flight'))


# user insert fname lname tel id image
#depart country province district subdistrict datetime
#destination  province district subdistrict datetime
# transport type :type if not car choose model
# 	firstname	lastname	citizen_id_passport	image
# phonenumber	updated_at	transport	depart_from	destination	trans_type

#insert data to database from form
@app.route('/insert',methods=['POST','GET'])
def insert_arrival_to_db():
    if request.method=="POST":
        firstname = request.form['fname']
        lastname = request.form['lname']
        citizen = request.form['id']
        file = request.files['file']
        phone = request.form['phonenumber']
        trans_type = request.form['type']
        # airline or train or public transport
        number = request.form['number']
        # depart data
        depart_date = request.form['depart_date']
        depart_subdistrict = request.form['depart_subdistrict']
        depart_district = request.form['depart_district']
        depart_th_province = request.form['depart_th_province']
        depart_country = request.form['depart_country']
        depart_en_province= request.form['depart_en_province']

        # destination data
        des_date = request.form['des_date']
        des_subdistrict = request.form['des_subdistrict']
        des_district = request.form['des_district']
        des_province = request.form['des_th_province']
        # cheak empty
        error = None
        if check_empty(firstname,lastname,citizen,file,phone,trans_type) ==True:
            error = "Error"
        elif check_empty(depart_date,depart_subdistrict,depart_district,depart_th_province)==True:
            error = "Error"
        elif check_empty(des_date,des_subdistrict,des_district,des_province)==True:
            error = "Error"
        elif check_escape(firstname,lastname,citizen,phone)==True:
            error = "Error"
        if error is None:
            date = datetime.now()
            # get path image to save
            if allowed_file(file.filename)==True:
                filename=secure_filename(file.filename)
                print(filename)
                get_type = file.content_type.replace('image/','.')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],citizen+get_type))
                # insert into depart
                conn="country={c} and en_province={d}".format(c=depart_country
                ,d=depart_en_province)
                depart = select_id_d(depart_subdistrict,depart_district,depart_th_province,conn)
                des = select_id_ds(des_subdistrict,des_district,des_province)
                if depart_district==" " and depart_th_province==" ":
                    insert_depart = """insert into Depart(en_province,country)
                    values(%s,%s)"""
                    cursor.execute(insert_depart,(depart_en_province,depart_country))
                else:
                    insert_depart = """insert into Depart(subdistrict,district
                    th_province,en_province,country)
                    values(%s,%s,%s,%s,%s)"""
                    cursor.execute(insert_depart,(depart_subdistrict
                    ,depart_district,depart_th_province,depart_en_province
                    ,depart_country))
                des = """select id  from destination where subdistrict=%s and
                district=%s and th_province=%s"""
                cursor.execute(des,(des_subdistrict,des_district,des_province))
                fet_des = cursor.fetchall()
                if len(fet_des)==0:
                    insert_des = """insert into destination(subdistrict
                    ,district,th_province) values(%s,%s,%s)"""
                    cursor.execute(insert_des,(des_subdistrict,des_district,des_province))
                # set depart id
                # insert to arrival_infromation databases
                delta = datetime.now()-timedelta(1)
                # insert personal data
                insert_per = """insert into personal(
                fname,lname,citizen_id,image,phonenumber,updated_at
                )values(%s,%s,%s,%s,%s,%s)"""
                cursor.execute(insert_per,(firstname,lastname,citizen
                ,citizen+get_type,phone,date))

                selec = """select id from personal where citizen_id=%s and
                updated_at>%s"""
                cursor.execute(selec,(citizen,delta))
                fet_id = cursor.fetchall()
                id = None
                for d in fet_id:
                    id = d[0]
                se_idp = """select id from depart where subdistrict=%s
                and district=%s and th_province=%s or en_province=%s and country=%s"""
                cursor.execute(se_idp,(depart_subdistrict,depart_district
                ,depart_th_province,depart_en_province,depart_country))
                idp = cursor.fetchall()
                se_ids = """select id from destination where subdistrict=%s
                and district=%s and th_province=%s"""
                cursor.execute(se_ids,(des_subdistrict,des_district,des_province))
                ids = cursor.fetchall()
                print("idd:",idp,"ids:",ids)
                print(number)
                insert_err = """
                insert into arrival_infromation(dep_time,des_time,depart_from
                ,destination,personal,flight_number,category)
                values(%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(insert_err,(depart_date,des_date,idp[0]
                ,ids[0],id,number,trans_type))
                con.commit()
                return redirect(url_for('insert_data_th'))
            session['error']=error
    return redirect(url_for('insert_data_th'))


if __name__=='__main__':
    app.run(debug=True)
