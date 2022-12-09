from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/first", methods=["POST"])
def login_post():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': '등록 완료',sample_receive:'샘플샘플'})

@app.route("/first", methods=["GET"])
def login_get():
    login_list = list(db.login.find({}, {'_id': False}))
    return jsonify({'msg': '등록 완료',login_list:'샘플샘플'})

@app.route("/first/main", methods=["POST"])
def main_post():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': '등록 완료', sample_receive:'샘플샘플'})

@app.route("/first/main", methods=["GET"])
def main_get():
    post_list = list(db.login.find({}, {'_id': False}))
    return jsonify({'msg': '등록 완료',post_list:'샘플샘플'})

@app.route("/first/main/post", methods=["POST"])
def main_post():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': '등록 완료', sample_receive:'샘플샘플'})

@app.route("/first/main/post", methods=["GET"])
def main_get():
    post_list = list(db.login.find({}, {'_id': False}))
    return jsonify({'msg': '등록 완료',post_list:'샘플샘플'})