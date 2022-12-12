from flask import Flask, render_template, request, jsonify, redirect, url_for, session
app = Flask(__name__)


from pymongo import MongoClient


import certifi
ca = certifi.where();
client = MongoClient('mongodb+srv://test:sparta@cluster0.pkogdim.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)

db = client.dbsparta

SECRET_KEY = 'SPARTA'

import jwt

import hashlib

import datetime


@app.route('/')
def show_home():
    return render_template('login.html')


@app.route('/login')
def show_login():
    return render_template('login.html')


@app.route('/sign')
def show_sign():
    return render_template('sign_up.html')


@app.route('/main')
def show_main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.min7_project.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"], id=payload['id'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/api/sign', methods=["POST"])
def sign_up():
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

    return jsonify({'msg': '가입 완료!'})


@app.route('/api/login', methods=["POST"])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.min7_project.find_one({'id': id_receive, 'pw': pw_hash})
    print(result)
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=500)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/board', methods=['GET'])
def board_get():
    user_list = list(db.min7_project.find({}, {'_id': False}))
    post_list = list(db.projects.find({}, {'_id': False}))
    return jsonify({'users': user_list, 'posts': post_list})


@app.route("/api/post", methods=["POST"])
def main_post():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    country_receive = request.form['country_give']
    doc = {'title': title_receive, 'comment': comment_receive,'country': country_receive}
    db.projects.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route('/api/country', methods=['GET'])
def show_country():
    kr_list = len(list(db.projects.find({'country':'KR'}, {'_id': False})))
    jp_list = len(list(db.projects.find({'country': 'JP'}, {'_id': False})))
    cn_list = len(list(db.projects.find({'country': 'CN'}, {'_id': False})))
    ot_list = len(list(db.projects.find({'country': 'OT'}, {'_id': False})))
    return jsonify(kr_list, jp_list, cn_list, ot_list)

@app.route("/api/profile/change", methods=["POST"])
def profile_change():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']
    # 비밀번호를 sha256문자열로 바꿔주기
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # 이미지 받아오기 코드 작성

    if id_receive == '':
        return jsonify({'msg': 'id를 입력하세요'})
    elif db.min7_project.find_one({'id': id_receive}) is None:
        return jsonify({'msg': '일치하는 id가 없습니다.'})

    if pw_receive == '' and nick_receive == '':
        return jsonify({'msg': '값을 입력하세요'})

    # 여기에 이미지 저장코드 작성하기

    if pw_hash == db.min7_project.find_one({'id': id_receive})['pw']:
        return jsonify({'msg': '같은 비밀번호입니다.'})

    if pw_receive != '':
        db.min7_project.update_one({'id': id_receive}, {'$set': {'pw': pw_hash}})

    if nick_receive == db.min7_project.find_one({'id': id_receive})['nick']:
        return jsonify({'msg': '같은 닉네임입니다.'})

    if nick_receive != '':
        db.min7_project.update_one({'id': id_receive}, {'$set': {'nick': nick_receive}})

    return jsonify({'msg': '변경 완료!'})


@app.route("/api/profile/delete", methods=["POST"])
def profile_delete():
    id_receive = request.form['id_give']
    if id_receive == '':
        return jsonify({'msg': 'id를 입력하세요'})
    elif db.min7_project.find_one({'id': id_receive}) is None:
        return jsonify({'msg': '일치하는 id가 없습니다.'})
    else:
        db.min7_project.delete_one({'id': id_receive})
        return jsonify({'msg': '탈퇴가 완료되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)