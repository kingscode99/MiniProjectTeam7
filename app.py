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
    print(title_receive, comment_receive)

    doc = {'title': title_receive, 'comment': comment_receive}
    db.mini.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


# @app.route("/first/main/post", methods=["GET"])
# def main_get():
#     post_list = list(db.login.find({}, {'_id': False}))
#     return jsonify({'msg': '등록 완료',post_list:'샘플샘플'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)