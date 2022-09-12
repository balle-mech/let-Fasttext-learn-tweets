import fasttext as ft

# トレーニングデータにより学習器を作る
def model_learn(txtfile):
    model = ft.train_supervised(input=txtfile)
    return model

model = model_learn('train.txt')
model.save_model("model.bin")
