from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

import certifi

# 각자 파이몽고 계정으로 테스트해주세요~
from pymongo import MongoClient
ca=certifi.where()
client = MongoClient("mongodb+srv://lcoeda:test@Cluster1.vpb9hys.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.test

SECRET_KEY = 'PROJECT_7'

import jwt

# import datetime

import hashlib

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.min7_project.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign', methods=["GET"])
def show_sign():
    return render_template('sign_up.html')

@app.route('/api/sign', methods=["post"])
def def_sign():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    nick_receive = request.form['nick_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_hash,
        'name': name_receive,
        'nick': nick_receive
    }

    db.min7_project.insert_one(doc)

    return jsonify({'msg': '변경 완료!'})

@app.route('/main',methods=["GET"])
def show_main(): # 로그인 성공시 main으로 가는지 확인하기 위함
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)