# -*- encoding:utf8 -*-
import random
import string
from PIL import Image, ImageDraw, ImageFont


# Image:画布   ImageDraw:画笔  ImageFont:画笔的字体
# print(list(string.ascii_letters))
class Captcha(object):
    number = 4  # 生成几位数的验证码
    size = (110, 43)  # 验证码图片的宽度和高度
    fontsize = 35  # 验证码字体大小
    line_number = 2  # 加入干扰线的条数
    SOURCE = list(string.ascii_letters + "123456789")  # 构建一个验证码源文本,包括大小写数字

    # classmethod 修饰符对应的函数不需要实例化，不需要 self 参数，
    # 但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等。
    @classmethod
    def __gene_line(cls, draw, width, height):
        # 开始点 X,Y
        begin = (random.randint(0, width), random.randint(0, height))
        # 结束点
        end = (random.randint(0, width), random.randint(0, height))
        # 画线条，开始 结束点  线条颜色  线条宽度
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        # 大小限制
        chance = min(50, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())

    # 生成随机的颜色
    @classmethod
    # 起始颜色 最终颜色
    def __gene_random_color(cls, start=0, end=255):
        # 初始化随机数
        random.seed()
        # 按范围生成随机输R  G  B
        return random.randint(start, end), random.randint(start, end), random.randint(start, end)

    # 随机选择一个字体
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            "STZHONGS.TTF",
            "STXIHEI.TTF",
            "COOPBL.TTF",
            "lucon.ttf"
        ]
        # 随机选一个 字体
        font = random.choice(fonts)
        return font

    # 用来随机生成一个字符串(包括英文和数字)
    @classmethod
    def gene_text(cls, number):
        # cls.SOURCE生成list A-Z a-z 0-9  number是生成验证码的位数
        return ''.join(random.sample(cls.SOURCE, number))

    # 生成验证码
    @classmethod
    def gene_graph_captcha(cls):
        # 验证码图片的宽和高
        width, height = cls.size
        # 创建图片
        # R：Red（红色）0-255  G：G（绿色）0-255   B：B（蓝色）0-255    A：Alpha（透明度）,添加了A，则就只能生成png图片
        image = Image.new('RGB', (width, height), cls.__gene_random_color(0, 100))
        # 验证码的字体  随机产生字体 字体大小
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 随机生成4为字符串
        text = cls.gene_text(cls.number)
        # 获取字体的尺寸
        font_width, font_height = font.getsize(text)
        # 填充字符串 x y坐标 文本 字体 字体颜色
        draw.text(((width - font_width) / 2, (height - font_height) / 2),
                  text, font=font, fill=cls.__gene_random_color(150, 255))
        # 绘制干扰线 绘制多少条干扰线

        for x in range(0, cls.line_number):
            cls.__gene_line(draw, width, height)
            # 绘制噪点
            cls.__gene_points(draw, 10, width, height)
        return text, image
