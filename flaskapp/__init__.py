from flask import Flask
from flask import render_template, request, Response, session, jsonify, make_response, redirect, flash, url_for
from datetime import datetime, date, timedelta
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from flaskapp.init_db import db_session, init_database
from flaskapp.db_models import User_info, Town_record, File_address
from werkzeug import secure_filename
import pymysql
from flask_mail import Mail, Message
import os







conn = pymysql.connect(host='localhost',
        user='root',
        password='r!',
        db='mytown_project',
        charset='utf8')


app = Flask(__name__)
app.debug = True

app.jinja_env.trim_blocks = True


@app.route("/")
def helloworld():
    return "Hello Flask World!"

@app.route("/home_page")
def home_page():
    
   
    cursor =  conn.cursor() 
                                        # left outer join 불안정해.... 이전에는 inner join
    sql = 'SELECT f.card_image, t.title, t.location FROM Town_record t inner join File_address f on t.id = f.id order by t.id desc'
    cursor.execute(sql)                     
    tr = cursor.fetchall()

    cursor.close()
    conn.close()

    print(tr)

    
    return render_template("home-page.html", tr=tr)



   
    

               


      
   #  여기서 가져오나? 데이터
   # 아니면 ajax 로?

@app.route("/product_page")
def product_page():
    return render_template("product-page.html")

@app.route("/checkout_page")
def checkout_page():
    return render_template("checkout-page.html")

@app.route("/recording_modal")
def recording():
    return render_template('macro.html')


@app.route('/mongo', methods=['GET'])
def mongoTest():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.merchandise
    collection = db.user
    results = collection.find()
    client.close()
    return render_template('mongo.html', data=results)


# Auto Managed Connection, But db_session create every request

# initialize connection
@app.before_first_request
def beforeFirstRequest():
    init_database()
# close connection
@app.teardown_appcontext
def teardown(exception):
    db_session.remove()


app.config.update(
    connect_args={"options": "-c timezone=utc"},
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.route('/sign_up', methods = ['POST'])
def sign_up():
   
   email = request.form.get('email')
   passwd = request.form.get('passwd')
   passwd2 = request.form.get('passwd2')
   name = request.form.get('name')
   

   if passwd != passwd2:
        
        flash("암호를 정확히 입력하세요!!")
        return redirect("/home_page")
      
    
   else:
      u = User_info(email, passwd, name, True)
      try:
         db_session.add(u)
         db_session.commit() 

      except:
         db_session.rollback()

         
      flash("%s 님, 가입을 환영합니다!" % nickname)
      return redirect("/home_page")

    


@app.route('/sign_in', methods=['POST'])
def login_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    u = User_info.query.filter('email = :email and passwd = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
    if u is not None:
        session['loginUser'] = { 'userid': u.id, 'name': u.name }
        if session.get('next'):
            next = session.get('next')
            del session['next']
            return redirect(next)
        return redirect('/')
    else:
        
        return "해당 사용자가 없습니다!!"

@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']

    return redirect('/')   



@app.route('/record', methods= ['POST'])
def record():

   name = request.form.get('name')
   title = request.form.get('title')
   location = request.form.get('location')
   describe = request.form.get('describe')

   # print(writer)
   # print(title)
   # print(location)
   # print(describe)

   r = Town_record(name, title, location, describe)
   try:
      db_session.add(r)
      db_session.commit() 

   except:
      db_session.rollback()

    
   return redirect("/home_page")


@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      #저장할 경로 + 파일명
      f.save('flaskapp/static/img/uploads/' + secure_filename(f.filename))

      img_address = '../static/img/uploads/' + secure_filename(f.filename)
      print(img_address)

      f = File_address(img_address)
      try:
         db_session.add(f)
         db_session.commit() 

      except:
         db_session.rollback()

   return redirect("/home_page")
   

@app.route("/email", methods=['post', 'get'])
def email_test():

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": os.environ['EMAIL_USER'],
        "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
    }

    app.config.update(mail_settings)
    mail = Mail(app)
    
    if request.method == 'POST':
        
        subject = request.form['subject']
        sender_email = request.form['email_sender']
        content = request.form['email_content']
        
        
        
            
        with app.app_context():
            msg = Message(subject=sender_email,  ### sender 변수로 발송자 email을 받을 수 없으니
                        sender= sender_email,
                        recipients=["paulo9428@naver.com"], # use your email for testing
                        body= content)
            mail.send(msg)
        
        
        
        if not mail.send(msg):
            return render_template('email.html', content="이메일 보내졌습니다")
        else:
            return render_template('email.html', content="이메일 발송이 실패했습니다")
    
    else:
        return render_template('email.html')
    
    

    

    # if __name__ == '__main__':
    #     with app.app_context():
    #         msg = Message(subject="Hello",
    #                     sender=app.config.get("MAIL_USERNAME"),
    #                     recipients=["paulo9428@naver.com"], # use your email for testing
    #                     body="This is a test email I sent with Gmail and Python!")
    #         mail.send(msg)

    


# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'joonsoolee14'
# app.config['MAIL_PASSWORD'] = ''
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

# @app.route("/email", methods=['post', 'get'])
# def email_test():
    
#     if request.method == 'POST':
#         senders = request.form['email_sender']
#         receiver = request.form['email_receiver']
#         content = request.form['email_content']
#         receiver = receiver.split(',')
        
#         for i in range(len(receiver)):
#             receiver[i] = receiver[i].strip()
            
#         print(receiver)
        
#         result = send_email(senders, receiver, content)
        
#         if not result:
#             return render_template('email.html', content="Email is sent")
#         else:
#             return render_template('email.html', content="Email is not sent")
        
#     else:
#         return render_template('email.html')
    
# def send_email(senders, receiver, content):
#     try:
#         mail = Mail(app)
#         msg = Message('Title', sender = senders, recipients = receiver)
#         msg.body = content
#         mail.send(msg)
#     except Exception:
#         pass 
#     finally:
#         pass    
      



 
   



 
  
   







 









