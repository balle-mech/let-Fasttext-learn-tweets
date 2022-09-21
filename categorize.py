import re
from flask import Flask, render_template, request
import tweepy
import fasttext as ft
import MeCab
import config

COUNT = 700    # ツイート取得数
model = ft.load_model('/Users/fukunagaatsushi/Desktop/gitdev/CategorizeTweets/model.bin')  # 分類器

# flask初期設定
app =  Flask(__name__)


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


# ツイートを学習モデルに分類させて辞書に格納
def categorize(results, raw_tweets):
    print('取得ツイート'+str(len(results))+'件')
    category_list = []
    category_dic = {}
    # ツイートをカテゴリに分類し、カテゴリごとのツイート数をカウント
    for result in results:
        raw_tweet = raw_tweets[results.index(result)] # ツイート原文を取得
        result = result.replace('\n', ' ')
        ret = model.predict(result)     # ツイートをカテゴリ別に分類
        cname = ret[0][0].replace('__label__', '')
        # カテゴリ名をkeyに、ツイート原文をvalueとして辞書に格納
        category_dic.setdefault(cname, []).append(raw_tweet.text)
    return category_dic


# 取得したツイートのうち、カテゴリごとの占める割合を辞書に格納
def get_ratio_dic(dic, results):
    key_list = []
    ratio_list = []
    for key in dic:
        key_list.append(key)
        tweet_num = len(dic[key])   # カテゴリごとのツイート数
        ratio = tweet_num / len(results) * 100
        ratio = round(ratio, 1)
        ratio_list.append(ratio)

    # リストを辞書に変換
    ratio_dic = dict(zip(key_list, ratio_list))
    # 辞書を割合で降順にソート
    ratio_dic = dict(sorted(ratio_dic.items(), key=lambda x: x[1], reverse=True))
    return ratio_dic


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
    num = len(results)
    category_dic = categorize(results, tweets)
    ratio_dic = get_ratio_dic(category_dic, results)
    return render_template('result.html', user_name=user_name, num=num, ratio_dic=ratio_dic)


if __name__ == "__main__":
    app.run(debug=True)
