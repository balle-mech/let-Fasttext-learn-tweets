import fasttext as ft

model = ft.load_model('model.bin')

ret = model.test('test.txt')
print(ret)