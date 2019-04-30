from flask import Flask
from flask import session, render_template, request
from datetime import datetime, date
from flask import g , Response, make_response, url_for
from pymongo import MongoClient
from werkzeug import secure_filename
from flaskapp import init_database

app = Flask(__name__)
app.debug = True

app.jinja_env.trim_blocks = True


@app.route("/")
def helloworld():
    return "Hello Flask World!"

@app.route("/home_page")
def home_page():
    return render_template("home-page.html")

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


#업로드 HTML 렌더링
@app.route('/upload')
def render_file():
   return render_template('upload.html')

#파일 업로드 처리
@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      
      f = request.files['file']
      #저장할 경로 + 파일명
      f.save('flaskapp/uploads/' + secure_filename(f.filename))
      return 'uploads 디렉토리 -> 파일 업로드 성공!'

if __name__ == '__main__':
    #서버 실행
   app.run(debug = True)

# Auto Managed Connection, But db_session create every request

# initialize connection
@app.before_first_request
def beforeFirstRequest():
    init_database()
# close connection
@app.teardown_appcontext
def teardown(exception):
    db_session.remove()


@app.route('/regist', methods=['GET'])
def regist():
    return render_template("regist.html")

@app.route('/regist', methods=['POST'])
def regist_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    
    name = request.form.get('name')


   u = User_info(name, email, passwd, True)
   try:
      db_session.add(u)
      db_session.commit() 

   except:
      db_session.rollback()

   flash("%s 님, 가입을 환영합니다!" % name)
   return redirect("/login")







 









