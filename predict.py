from learning import model_learn

model = model_learn('train.txt')
ret = model.predict('モンハンで誰か協力プレイしてくれる人いませんか')

print(ret)