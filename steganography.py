from PIL import Image
choice = input(':: Стеганография :: \n1 - зашифровать информацию в изображение \n2 - расшифровать информацию в изображении \n')
path = input('Укажите путь к изображению в формате (.png): \n')  # C:\Users\mmmfe\Pictures\Saved Pictures\cat.png
img = Image.open(path)  # C:\Users\mmmfe\Pictures\Saved Pictures\stego_img.png


def encode():
    depth = int(input('Введите глубину шифрования (не больше 8): '))
    if depth > 8:
        print('Выберите глубину шифрования меньше 8')
        return
    bin_depth = str(bin(depth - 1))
    if len(bin_depth) < 5:
        bin_depth = '0b' + '0' * (5 - len(bin_depth)) + bin_depth[2:]
    text = input('Введите текст для стеганографии (без символов русского алфавита): ')  # Slave
    text += 'MIFed'  # обозначение конца текста
    stego_text = ''
    for i in text:
        sign = bin(ord(i))[2:]
        if len(sign) < 7:
            sign = '0' + sign
        stego_text += sign
    print(len(stego_text))
    print(img.size[0], img.size[1])
    if len(stego_text) > (img.size[0] * img.size[1] - 1) * 3 * depth:
        print('Размер картинки слишком маленький для введённого вами текста')
        return
    print(stego_text)
    i_stego_text = 0
    end_stego_text = len(stego_text)
    new_img = img.copy()
    pixel_array = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixel_array[i, j]
            new_pixel = list(pixel)
            for k in range(3):
                if i_stego_text != end_stego_text:
                    print(bin(pixel[k]))
                    len_px = len(str(bin(pixel[k])))
                    px = '0b' + '0' * (10 - len_px) + str(bin(pixel[k]))[2:len_px]
                    print(px)
                    if i_stego_text + depth > end_stego_text:
                        depth = end_stego_text - i_stego_text
                    new_pixel[k] = int(px[:-depth] + stego_text[i_stego_text:i_stego_text+depth], 2)
                    print(bin(new_pixel[k]))
                    print('---')
                    i_stego_text += depth
            new_img.putpixel((i, j), tuple(new_pixel))
    print(i, j)
    print(pixel_array[i, j])
    dp = [str(bin(pixel_array[i, j][0])), str(bin(pixel_array[i, j][1])), str(bin(pixel_array[i, j][2]))]
    depth_pixel = [int(dp[0][0:len(dp[0])-1] + bin_depth[2], 2), int(dp[1][0:len(dp[1])-1] + bin_depth[3], 2), int(dp[2][0:len(dp[2])-1] + bin_depth[4], 2)]
    new_img.putpixel((i, j), tuple(depth_pixel))
    new_img.show()
    choose_path = input('- Напишите адрес директории, где хотите сохранить стего-картинку \n- Введите 0 и картинка сохранится рядом с программой: ')
    if choose_path == '0':
        new_img.save('stego_img.png')
    else:
        new_img.save(choose_path + '\stego_img.png')
        print('Картинка сохранена по пути: ' + choose_path +'\stego_img.png')


def decode():
    last_bits = ''
    pixel_array = img.load()
    depth_pixel = pixel_array[img.size[0]-1, img.size[1]-1]
    depth = int('0b' + str(bin(depth_pixel[0]))[-1] + str(bin(depth_pixel[1]))[-1] + str(bin(depth_pixel[2]))[-1], 2) + 1
    print(depth)  # (244, 121, 125)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixel_array[i, j]
            last_bits += str(bin(pixel[0]))[-depth:] + str(bin(pixel[1]))[-depth:] + str(bin(pixel[2]))[-depth:]
    print(last_bits)
    if '10011011001001100011011001011100' in last_bits:
        stego_text = last_bits[0:last_bits.index('10011011001001100011011001011100')]   # MIFed - обозначение конца в бинарном виде
    else:
        print('Картинка не была зашифрована через эту программу')
        return
    text = ''
    try:
        for i in range(len(stego_text)//7):
                text += chr(int('0b' + stego_text[7 * i:7 * i+7], 2))
    except ValueError:
        print(text)
    print(text)


if choice == '1':
    encode()
elif choice == '2':
    decode()
else:
    print('Неизвестная комманда')
exit = input('Нажмите Enter для выхода ')
