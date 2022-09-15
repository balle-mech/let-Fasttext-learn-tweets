import re
import MeCab
from time import sleep
import config

COUNT = 100    # ツイート取得数
train_idx = 80    # トレーニングデータ%
SET = 30    # セット数×100件のツイートを取得
KEYWORDS = ['エンジニア', 'ゲーム', 'アニメ']


def main():
    tweets = get_tweet()      #ツイートを取得
    result = separate_tweet(tweets)     #ツイートを分かち書き
    write_txt(result)        #ツイートをファイルに書き込み

# TwitterからKEYWORDに関連するツイートを取得
def get_tweet():
    api = config.authTwitter() # API認証
    tweets = api.search_tweets(q=KEYWORD, count=COUNT)
    return tweets

# 正規表現を使ってツイートから不要な情報を削除
def format_text(text):
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)  # 外部リンクURL
    text = re.sub(r'@[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)  # ユーザーID
    text = re.sub(r'＼', "", text)
    text = re.sub('／', "", text)
    text = re.sub('RT', "", text)
    text = re.sub('\n', "", text) # 改行文字
    return text

# 文書を分かち書きし単語単位に分割
def separate_tweet(tweets):
    results = []
    tagger = MeCab.Tagger('-Owakati')

    for tweet in tweets:
        content = format_text(tweet.text)
        wakati = tagger.parse(content)
        results.append(' , '.join(['__label__' + KEYWORD, wakati])) # ツイートごとにラベルを付与
    return results

# 学習モデル用と評価用のテキストファイルを作成
def write_txt(results):
    idx = 0
    with open('train_' + KEYWORD + '.txt', 'a') as f_train,\
        open('test' + KEYWORD + '.txt', 'a') as f_test:
        for result in results:
            if idx < train_idx:
                f_train.write(result)
            else:
                f_test.write(result)
            idx += 1

        print("{}ツイート100件取得{}セット目".format(KEYWORD, i))

if __name__ == '__main__':
    for i in range(SET):
        for KEYWORD in KEYWORDS:
            main()
        print('15秒待機')
        sleep(15)
