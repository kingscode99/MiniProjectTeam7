from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

import certifi
ca = certifi.where();

client = MongoClient('mongodb+srv://test:sparta@cluster0.nlofzws.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/sign', methods=["POST"])
def sign_up():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    nick_receive = request.form['nick_give']

    doc = {       # 패스워드에 경우 해쉬값으로 저장해야하지만 일단은 뼈대 구축만 하겠다.
        'id': id_receive,
        'pw': pw_receive,
        'name': name_receive,
        'nick': nick_receive
    }

    db.min7_project.insert_one(doc)

    return jsonify({'msg': '변경 완료!'})

@app.route('/sign', methods=["GET"])
def show_sign():
    return render_template('sign_up.html')
@app.route('/login', methods=["GET"])
def show_login():
    return render_template('login.html')

@app.route('/main',methods=["get"])
def show_main(): # 로그인 성공시 main으로 가는지 확인하기 위함
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)