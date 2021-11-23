from PIL import Image
choice = input(':: Стеганография :: \n1 - зашифровать информацию в изображение \n2 - расшифровать информацию в изображении \n')
path = input('Укажите путь к изображению в формате (.png): \n')  # C:\Users\mmmfe\Pictures\Saved Pictures\draw.png
img = Image.open(path)  # C:\Users\mmmfe\Pictures\Saved Pictures\stego_img.png


def encode():
    text = input('Введите текст для стеганографии (без символов русского алфавита): ')  # Slave
    text += 'MIFed'  # обозначение конца текста
    stego_text = ''
    for i in text:
        sign = bin(ord(i))[2:]
        if len(sign) < 7:
            sign = '0' + sign
        stego_text += sign
    if len(stego_text) > img.size[0] * img.size[1] * 3:
        return 'Размер картинки слишком маленький для введённого вами текста'
    i_stego_text = 0
    end_stego_text = len(stego_text)
    new_img = img.copy()
    pixel_array = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixel_array[i, j]
            new_pixel = list(pixel)
            if i_stego_text != end_stego_text:
                new_pixel[0] = int(str(bin(pixel[0]))[:-1] + stego_text[i_stego_text], 2)
                i_stego_text += 1
            if i_stego_text != end_stego_text:
                new_pixel[1] = int(str(bin(pixel[1]))[:-1] + stego_text[i_stego_text], 2)
                i_stego_text += 1
            if i_stego_text != end_stego_text:
                new_pixel[2] = int(str(bin(pixel[2]))[:-1] + stego_text[i_stego_text], 2)
                i_stego_text += 1
            new_img.putpixel((i, j), tuple(new_pixel))
    new_img.show()
    choose_path = input('- Напишите адрес директории, где хотите сохранить стего-картинку \n- Введите 0 и картинка сохранится рядом с программой: ')
    if choose_path == '0':
        new_img.save('stego_img.png')
    else:
        new_img.save(choose_path + '\stego_img.png')


def decode():
    last_bits = ''
    pixelMap = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixelMap[i, j]
            last_bits += str(bin(pixel[0]))[-1] + str(bin(pixel[1]))[-1] + str(bin(pixel[2]))[-1]
    if '10011011001001100011011001011100100' in last_bits:
        stego_text = last_bits[0:last_bits.index('10011011001001100011011001011100100')]   # MIFed - обозначение конца в бинарном виде
    else:
        print('Картинка не была зашифрована через эту программу')
        return
    text = ''
    for i in range(len(stego_text)//7):
        text += chr(int('0b' + stego_text[7 * i:7 * i+7], 2))
    print(text)


if choice == '1':
    encode()
elif choice == '2':
    decode()
else:
    print('Неизвестная комманда')
exit = input('Нажмите Enter для выхода ')
