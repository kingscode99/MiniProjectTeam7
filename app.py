from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.b6vbteu.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/first/main/post", methods=["POST"])
def main_post():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    doc = {'title': title_receive, 'comment': comment_receive}
    db.projects.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


@app.route("/first/main/profile", methods=["POST"])
def main_profile():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    db.users.update_one({'id': id_receive}, {'$set': {'name': name_receive}})
    db.users.update_one({'id': id_receive}, {'$set': {'pw': pw_receive}})
    return jsonify({'msg': '변경 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)