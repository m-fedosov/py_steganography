from PIL import Image
from math import log10
choice = input(':: Стеганография (Михаил Федосов):: '
               '\n1 - зашифровать информацию в изображении '
               '\n2 - расшифровать информацию в изображении \n')
path = input('Укажите путь к изображению-контейнеру в формате (.png): '
             '\n')  # C:\Users\mmmfe\Pictures\Saved Pictures\draw.png
img = Image.open(path)  # C:\Users\mmmfe\Pictures\Saved Pictures\stego_img.png


def your_message(message_type):
    if message_type == 1:  # byte str
        bit_bits = input('Введите битовую последовательность: ')
        bit_bits += '100110101001001010001100110010101100100'  # обозначение конца строки
        bit_bits = '01' + bit_bits  # обозначение битовой строки для автоматической дешифровки
        if len(bit_bits) > img.size[0] * img.size[1] * 3:
            print(f'Размер картинки слишком маленький для введённой последовательности бит \n'
                  f'Количество бит скрытой инвормации: {str(len(bit_bits))} \n'
                  f'в картинке свободных бит для скрытия: {str(img.size[0] * img.size[1] * 3)} ')
            exit()
        return bit_bits
    elif message_type == 2:  # txt xtr
        choose_input = int(input('Выберите: \nВвести текст врчную - 1 \nОткрыть файл (название.txt) - 2\n'))
        if choose_input == 1:
            text = input('Введите текст для стеганографии (без символов русского алфавита): ')  # Slave
        elif choose_input == 2:
            text_file = input('Введите путь к файлу .txt: \n')  # D:\Загрузки\lord.txt
            text = open(text_file, 'r').read()
        else:
            print('Некорректный ввод в строке выше')
            exit()
        text += 'MIFed'  # обозначение конца текста
        bit_text = '10'  # обозначение текст для автоматической дешифровки
        for i in text:
            sign = bin(ord(i))[2:]
            if len(sign) < 8:
                sign = '0' * (8 - len(sign)) + sign
            bit_text += sign
        if len(bit_text) > img.size[0] * img.size[1] * 3:
            print(f'Размер картинки слишком маленький для введённой последовательности бит \n'
                  f'Количество бит скрытой инвормации: {str(len(bit_text))} \n'
                  f'в картинке свободных бит для скрытия: {str(img.size[0] * img.size[1] * 3)}')
            exit()
        return bit_text
    elif message_type == 3:  # img
        path_stego = input(
            'Укажите путь к изображению в формате (.png), которое хотите скрыть:'
            ' \n')  # C:\Users\mmmfe\Pictures\Saved Pictures\draw.png
        img_stego = Image.open(path_stego)
        pixel_array = img_stego.load()
        stego_pixels = '11'  # обозначение картинки для дешифровки
        for i in range(2):  # зашифровываю размеры скрытого изображения. Макс 4096 * 4096
            stego_pixels += '0' * (12 - len(str(bin(img_stego.size[i]))[2:])) + str(bin(img_stego.size[i]))[2:]
        for i in range(img_stego.size[0]):
            for j in range(img_stego.size[1]):
                pixel = pixel_array[i, j]
                for k in range(3):
                    stego_pixels += '0' * (8 - len(str(bin(pixel[k]))[2:])) + str(bin(pixel[k]))[2:]

        stego_pixels += '100110101001001010001100110010101100100'  # Обозначение конца строки
        if len(stego_pixels) > img.size[0] * img.size[1] * 3:
            print('Размер картинки слишком маленький для скрытия в ней вашей картинки: '
                  '\n- выберите картинку для зашифрования меньшего размера'
                  '\n- предложите картинку большего разрешения на первом шаге')
            exit()
        return stego_pixels
    else:
        print('Некорректный ввод')
    exit()


def save_picture(image):
    image_name = input('Введите название файла для сохранения (название.png): \n')
    choose_path = input('- Напишите адрес директории, где хотите сохранить стего-картинку \n'
                        '- Введите 0 и картинка сохранится рядом с программой: ')
    if choose_path == '0':
        image.save(image_name)
    else:
        path_picture = (choose_path + '\\' + image_name)
        image.save(path_picture)
        print(f'Картинка сохранена по пути:\n {path_picture}')


def encode():
    choose_type = int(input('Выберите тип файла для стеганографии: \n'
                            'Битовая последовательность - 1 \n'
                            'Текстовая строка - 2 \n'
                            'Изображение - 3 \n'))
    stego_text = your_message(choose_type)
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
                    new_pixel[k] = int(str(bin(pixel[k]))[:-1] + stego_text[i_stego_text], 2)
                    i_stego_text += 1
            new_img.putpixel((i, j), tuple(new_pixel))
    new_img.show()
    save_picture(new_img)
    print('Рассчитать показатели качества встраивания? \nда - 1\nнет - 2')
    choose_psnr = int(input())
    if choose_psnr == 1:
        print('~~Емкость~~ \n(сколько битов встроенной информации приходится на каждый пиксель изображения):')
        b = len(stego_text)  # размер сообщения в битах
        m = img.size[0]  # ширина изображения-контейнера
        n = img.size[1]  # высота изображения-контей1нера
        print(b / (m * n))
        print('~~Незаметность~~ \n(отражает различие между изображениями до и после встраивания)')
        cnt_dfrnt = 0
        original_px_array = pixel_array
        change_px_array = new_img.load()
        for i in range(m):
            for j in range(n):
                original_pixel = list(original_px_array[i, j])
                change_pixel = list(change_px_array[i, j])
                for k in range(3):
                    if original_pixel[k] != change_pixel[k]:
                        cnt_dfrnt += 1  # не возвожу в квадрат, т.к. 1^2 = 1

        mse = cnt_dfrnt/(m * n * 3)  # среднеквадратичная ошибка
        psnr = 10 * log10(255**2/(mse**2))  # пиковое отношение сигнал-шум
        print(f'значение PSNR: {psnr} dB')


def decode_by_type(bits):
    stego_type = bits[:2]
    if stego_type == '01':  # битовая строка
        print(bits[2:])
    elif stego_type == '10':  # текст
        stego_text = bits[2:]
        text = ''
        for i in range(len(stego_text) // 8):
            text += chr(int('0b' + stego_text[8 * i:8 * i + 8], 2))
        print(text)
    elif stego_type == '11':  # картинка
        stego_bits = bits[26:]
        x = int(bits[2:14], 2)
        y = int(bits[14:26], 2)
        i_px = 0
        your_image = Image.new("RGB", (x, y), (0, 0, 0))
        for i in range(x):
            for j in range(y):
                new_px = [0, 0, 0]
                for k in range(3):
                    new_px[k] = int(stego_bits[i_px: i_px+8], 2)
                    i_px += 8
                your_image.putpixel((i, j), tuple(new_px))
        your_image.show()
        save_picture(your_image)
    else:
        print('Код надёжный как швейцарские часы, но где-то есть ошибка')
        exit()


def decode():
    last_bits = ''
    pixel_array = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixel_array[i, j]
            last_bits += str(bin(pixel[0]))[-1] + str(bin(pixel[1]))[-1] + str(bin(pixel[2]))[-1]
    if '100110101001001010001100110010101100100' in last_bits:
        stego_text = last_bits[0:last_bits.index('100110101001001010001100110010101100100')]
        # MIFed - обозначение конца в бинарном виде
    else:
        print('Картинка не была зашифрована через эту программу')
        return
    return decode_by_type(stego_text)


if choice == '1':
    encode()
elif choice == '2':
    decode()
else:
    print('Неизвестная комманда')
exit = input(':: Нажмите Enter для выхода ::')
