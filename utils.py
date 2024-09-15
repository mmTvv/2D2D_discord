from PIL import Image, ImageDraw, ImageFont
import json
from time import sleep
from javascript import require, On, Once

# Карты стилей и цветов

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

class Tab():
    def __init__(self):

        self.color_map = {
            '0': (0, 0, 0),
            '1': (0, 0, 170),
            '2': (0, 170, 0),
            '3': (0, 170, 170),
            '4': (170, 0, 0),
            '5': (170, 0, 170),
            '6': (250, 170, 0),
            '7': (170, 170, 170),
            '8': (85, 85, 85),
            '9': (85, 85, 255),
            'a': (85, 255, 85),
            'b': (85, 255, 255),
            'c': (255, 85, 85),
            'd': (255, 85, 255),
            'e': (255, 255, 85),
            'f': (255, 255, 255)
        }
        self.colors = {
            "dark_red": "4",
            "red": "c",
            "gold": "6",
            "yellow": "e",
            "dark_green": "2",
            "green": "a",
            "aqua": "b",
            "dark_aqua": "3",
            "dark_blue": "1",
            "blue": "9",
            "light_purple": "d",
            "dark_purple": "5",
            "white": "f",
            "gray": "7",
            "dark_gray": "8",
            "black": "0"
        }
        self.style_map = {
            'l': 'bold',
            'm': 'strikethrough',
            'n': 'underline',
            'o': 'italic'
        }
        self.mineflayer = require('mineflayer')
        self.bot = self.mineflayer.createBot({"host": '109.248.206.65', "port": 25565, "username": 'fleshka', "version": '1.18.2'})
        sleep(10)
        self.bot.chat('/l 123123p')
        sleep(2)

    def login(self):
        self.bot = self.mineflayer.createBot({"host": '109.248.206.65', "port": 25565, "username": 'fleshka', "version": '1.18.2'})
        sleep(10)
        self.bot.chat('/l 123123p')
        sleep(2)
        
        

    def get_tab_data(self):
        header = self.bot.tablist.header.json.valueOf()
        footer = self.bot.tablist.footer.json.valueOf()
        players = self.bot.players.valueOf()
        if 'extra' not in header:
            self.login()
        header, players, footer = self.get_tab_data()
        return header, players, footer

    def draw_colored_text(self, header, footer, players, font_path, output_image, background_image_path=None):
        # Открываем фоновое изображение или создаём новое
        if background_image_path:
            base_image = Image.open(background_image_path).convert('RGBA')
        else:
            base_image = Image.new('RGBA', (1000, 800), (255, 255, 255, 255))
        
        draw = ImageDraw.Draw(base_image)
        font_large = ImageFont.truetype(font_path, 22)  # Размер шрифта для header и footer
        font_small = ImageFont.truetype(font_path, 22)  # Размер шрифта для игроков

        line_height_large = 25  # Высота строки для header и footer
        line_height_small = 27  # Высота строки для игроков

        def apply_style(draw, text, x, y, font, color, style):
            bbox = draw.textbbox((x, y), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            if style == 'bold':
                for offset in [-1, 0, 1]:
                    draw.text((x + offset, y), text, font=font, fill=color)
            elif style == 'strikethrough':
                draw.text((x, y), text, font=font, fill=color)
                y_center = y + text_height / 2
                draw.line((x, y_center, x + text_width, y_center), fill=color, width=2)
            elif style == 'underline':
                draw.text((x, y), text, font=font, fill=color)
                underline_y = y + text_height + 2
                draw.line((x, underline_y, x + text_width, underline_y), fill=color, width=2)
            elif style == 'italic':
                draw.text((x, y), text, font=font, fill=color)
            else:
                draw.text((x, y), text, font=font, fill=color)

        def calculate_text_width(line, font):
            x = 0
            words = line.split('&')
            for word in words:
                if len(word) > 0:
                    style_code = word[0]
                    text_part = word[1:]
                    bbox = draw.textbbox((x, 0), text_part, font=font)
                    text_width = bbox[2] - bbox[0]
                    x += text_width
            return x

        def calculate_total_text_size(lines, font, line_height):
            total_width = 0
            total_height = len(lines) * line_height
            for line in lines:
                line_width = calculate_text_width(line, font)
                total_width = max(total_width, line_width)
            return total_width, total_height

        def draw_text_block(y, text_lines, draw, font, line_height):
            current_style = ''
            x = 50
            for line in text_lines:
                line_width = calculate_text_width(line, font)
                x = (base_image.width - line_width) // 2
                words = line.split('&')
                for word in words:
                    if len(word) > 0:
                        style_code = word[0]
                        text_part = word[1:]

                        if style_code in self.color_map:
                            current_color = self.color_map[style_code]
                        elif style_code in self.style_map:
                            current_style = self.style_map[style_code]
                        elif style_code == 'r':
                            current_color = (0, 0, 0)
                            current_style = ''

                        apply_style(draw, text_part, x, y, font, current_color, current_style)
                        
                        bbox = draw.textbbox((x, y), text_part, font=font)
                        text_width = bbox[2] - bbox[0]
                        x += text_width
                
                y += line_height

            return y

        # Подготовка текста
        header_lines = header.split('&n')
        footer_lines = footer.split('&n')
        player_lines = [f"{i + 1} {player}" for i, player in enumerate(players)]
        print(player_lines)
        
        # Вычисляем размеры текста
        header_height = calculate_total_text_size(header_lines, font_large, line_height_large)[1]
        footer_height = calculate_total_text_size(footer_lines, font_large, line_height_large)[1]
        player_height = calculate_total_text_size(player_lines, font_small, line_height_small)[1]

        # Расчёт общего размера фона
        total_text_height = header_height + player_height + footer_height + 70  # 20 пикселей сверху, 50 пикселей снизу
        total_text_width = max(calculate_text_width(line, font_large) for line in header_lines) + \
                           max(calculate_text_width(line, font_small) for line in player_lines) + \
                           max(calculate_text_width(line, font_large) for line in footer_lines) + 100

        # Определяем координаты фона
        padding_x = 20
        padding_y = 20
        text_box_x = (base_image.width - total_text_width) // 2
        text_box_y = 20  # Начало фона с 20 пикселей сверху
        text_box_width = total_text_width
        text_box_height = total_text_height

        # Создаем изображение для фона
        background = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
        background_draw = ImageDraw.Draw(background)
        background_draw.rectangle(
            [(text_box_x, text_box_y), (text_box_x + text_box_width, text_box_y + text_box_height)],
            fill=(0, 0, 0, 128)
        )

        # Рисуем фон на изображении
        base_image.paste(background, (0, 0), background)

        # Рисуем текст на изображении
        draw = ImageDraw.Draw(base_image)  # Перерисовываем для текста
        y = text_box_y + 30  # Сдвигаем текст на 30 пикселей вниз
        y = draw_text_block(y, header_lines, draw, font_large, line_height_large)
        y += 10  # Отступ между header и players
        y = draw_text_block(y, player_lines, draw, font_small, line_height_small)
        y += 10  # Отступ между players и footer
        draw_text_block(y, footer_lines, draw, font_large, line_height_large)

        # Сохраняем изображение
        base_image.save(output_image)


    def format_text(self, text):
        txt = ''
        for i in text['extra']:
            if 'color' in i:
                tag = '&' + self.colors[i['color']] + i['text']
            else:
                tag = '&f' + i['text']
            if 'bold' in text:
                tag = '&l' + tag
            if 'strikethrough' in text:
                tag = '&m' + tag
            if 'underline' in text:
                tag = "&n" + tag
            if 'italic' in text:
                tag = '&o' + tag
            if '\n' in i['text']:
                tag = tag + '&n' 
            txt = txt + tag
        return txt + text['text']

    def format_nick(self, players):
        nicks = []
        for player in players:
            for player_data in players[player]['displayName']['json']:
                if player_data == 'extra':
                    nick = ''
                    for stat in players[player]['displayName']['json'][player_data]:
                        tag = ''
                        if "color" in stat:
                            tag = '&' + self.colors[stat['color']] + stat['text']
                        else:
                            tag = '&f' + stat['text']
                        if 'bold' in stat:
                            if stat['bold'] == True:
                                tag = '&l'+tag
                        if 'strikethrough' in stat:
                            if stat['strikethrough'] == True:
                                tag = '&m' + tag
                        if 'underline' in stat:
                            if stat['underline'] == True:
                                tag = "&n" + tag
                        if 'italic' in stat:
                            if stat['italic'] == True:
                                tag = '&o' + tag

                        if '\n' in stat['text']:
                            tag = tag
                        nick = nick + tag
                    nicks.append(nick)
        return nicks