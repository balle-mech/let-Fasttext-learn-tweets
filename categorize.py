import re
from flask import Flask, render_template, redirect, request
import tweepy
import fasttext as ft
import MeCab
import config
from flask_sqlalchemy import SQLAlchemy

COUNT = 700    # ツイート取得数
model = ft.load_model('model.bin')  # 分類器

# flask初期設定
app =  Flask(__name__)
# SQLiteの準備
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///categorize.db'
db = SQLAlchemy(app)

# データベースの項目定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(15), nullable=False)
    num = db.Column(db.Integer)
    category = db.Column(db.String, nullable=False)
    ratio = db.Column(db.Integer, nullable=False)
    raw_tweet = db.Column(db.String)

def main(id):
    tweets = get_tweet(id)      #ツイートを取得
    results = separate_tweet(tweets)     #ツイートを分かち書き
    categorize(results, tweets)        #ツイートを分類


# 指定したユーザーのツイートを取得
def get_tweet(id):
    api = config.authTwitter() # config.pyを使ってAPI認証
    tweets = [
        tweet
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=id).items(COUNT)
        if list(tweet.text)[0] != '@'  # リプライを除外
        ]
    return tweets

# 正規表現を使ってツイートから不要な情報を削除
def format_text(text):
        text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)  # 外部リンクURL
        text=re.sub(r'@[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text) # リツイート元のユーザーID
        text=re.sub(r'＼', "", text)
        text=re.sub(r'／', "", text)
        text=re.sub(r'RT', "", text)
        text=re.sub(r'\n', " ", text)    # 改行文字
        return text

# 文書を分かち書きし単語単位に分割
def separate_tweet(tweets):
    results = []
    tagger = MeCab.Tagger('-Owakati')

    for tweet in tweets:
        content = format_text(tweet.text)
        wakati = tagger.parse(content)
        results.append(wakati)
    return results

# ツイートを学習モデルに分類させて割合表示
def categorize(results, raw_tweets):
    print('取得ツイート'+str(len(results))+'件')
    category_dic = {}
    # ツイートをカテゴリに分類し、カテゴリごとのツイート数をカウント
    for result in results:
        raw_tweet = raw_tweets[results.index(result)] # ツイート原文を取得
        result = result.replace('\n', ' ')
        ret = model.predict(result)
        cname = ret[0][0].replace('__label__', '')
        category_dic.setdefault(cname, []).append(raw_tweet.text)
    # 取得したツイートのうち、カテゴリごとの占める割合を表示
    for key in category_dic:
        tweet_num = len(category_dic[key])
        ratio = (tweet_num / len(results)) * 100
        if ratio > 0:
            print('{}系ツイート:{}%'.format(key, round(ratio, 1)))
            print('例えばこんなツイートが{}系だと判定されています。'.format(key))
            print('--------------------')
            print(category_dic[key][0])
            print('--------------------')
            ratio = round(ratio, 1)
            return key


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    user_name = request.form.get('user_name')
    error = None
    if not user_name:
        error = 'IDを入力してください。'
        return render_template('index.html', error=error)

    # メイン処理
    try:
        get_tweet(user_name)
    except Exception:
        error = 'ユーザーが見つかりませんでした。'
        return render_template('index.html', error=error)
    tweets = get_tweet(user_name)
    results = separate_tweet(tweets)
    key = categorize(results, tweets)       #ツイートを分類
    print(key)
    return render_template('result.html', category = key)


if __name__ == "__main__":
    app.run(debug=True)
