# -*- coding: utf-8 -*-
from PIL import Image
choice = input(':: Стеганография :: \n1 - зашифровать информацию в изображение \n2 - расшифровать информацию в изображении \n')
# path = input('Укажите путь к изображению в формате (.png): \n')  # C:\Users\mmmfe\Pictures\Saved Pictures\draw.png
path = input('Укажите путь к изображению в формате (.png): \n')  # C:\Users\mmmfe\Pictures\Saved Pictures\draw.png
img = Image.open(path)


def encode():
    # text = input('Укажите текст для стеганографии: ')  # $t3гО^?
    text = '$t3г О^?'
    text = text.decode("utf-8")
    print(text)
    for i in text:
        print(bin(ord(i)))
    return

    pixelMap = img.load()
    print(img.size[0])
    print(img.size[1])
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixelMap[i, j]
        print('Столбец')


if choice == '1':
    encode()
elif choice == '2':
    pass
else:
    print('Неизвестная комманда')



# pixelMap = img.load()  # create the pixel map
# pixel = pixelMap[0, 0].copy()
# print(pixel)
img.show()
exit = input('Нажмите Enter для выхода ')