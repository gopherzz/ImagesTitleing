from PIL import Image, ImageDraw, ImageFont
from sys import platform
import os
import csv


class Main:

    def __init__(self):
        self.CSVFILENAME = input('Csv File Dir: ').strip()
        self.INPUTDIR = input('Dir with source images name: ').strip()
        self.OUTPUTDIR = input('Output dir name: ').strip()
        self.FONTSIZE = 32
        self.BFCOLOR = 'white'
        self.PADDING = 30

        if platform == "linux":
            self.FONT = ImageFont.truetype(font=f'{"/usr/share/fonts/truetype/freefont/FreeSerif.ttf"}',
                                           size=self.FONTSIZE)
        else:
            self.FONT = ImageFont.truetype(font=f'arial.ttf',
                                           size=self.FONTSIZE)

        self.FONTCOLOR = 'black'

    # Return Size of Multiline String
    def get_size(self, text, font):
        l_text = text.split('\n')
        max_l = ''

        for i in l_text:
            if len(i) > len(max_l):
                max_l = i
        line_spacing = round(self.FONTSIZE * 0.25)

        text_width, text_height = font.getsize(max_l)
        return text_width, text_height*len(l_text)+(line_spacing*(len(l_text)-1))

    # ohh that debug fun, don't touch it
    @staticmethod
    def print_row(row):
        print(row[0].strip(), '',
              row[1].strip(), '',
              row[2].strip())

    # Match Position types
    # text: str, imageSize: str, pos: tuple -> tuple, tuple
    def match_pos(self, text, image_size, pos):
        imagew, imageh = image_size
        textw, texth = self.get_size(text, self.FONT)

        if pos == 'TL':
            text_pos = (0 + self.PADDING,
                        0 + self.PADDING)
            return (text_pos,
                    (0, 0, textw + self.PADDING * 2, texth + self.PADDING * 2))

        if pos == 'TR':
            text_pos = (imagew - textw - self.PADDING,
                        0 + self.PADDING)
            textx, texty = text_pos
            return (text_pos, (textx - self.PADDING, 0,
                               imagew, texty + texth + self.PADDING))
        if pos == 'BL':
            text_pos = (0 + self.PADDING,
                        imageh - texth - self.PADDING)

            return (text_pos, (0, imageh,
                               textw + self.PADDING * 2, imageh - texth - self.PADDING * 2))
        if pos == 'BR':
            text_pos = (imagew - textw - self.PADDING,
                        imageh - texth - self.PADDING)
            textx, texty = text_pos
            return (text_pos, (textx - self.PADDING, texty - self.PADDING,
                               imagew, imageh))
        if pos == 'CT':
            text_pos = (imagew // 2 - textw // 2,
                        imageh // 2 - texth // 2)
            textx, texty = text_pos

            return (text_pos, (textx - self.PADDING, texty - self.PADDING,
                               textx + textw + self.PADDING, texty + texth + self.PADDING))

    # ImageName: str, Text: str, pos: tuple -> save image to OUTPUTDIR
    def process_image(self, imagename, text, pos):
        image = Image.open(f'{self.INPUTDIR}' + os.path.sep + f'{imagename}')
        idraw = ImageDraw.Draw(image)

        text_pos, bg_pos = self.match_pos(text, image.size, pos)

        idraw.rectangle(bg_pos, fill=self.BFCOLOR)
        idraw.text(text_pos, text, font=self.FONT, fill=self.FONTCOLOR)

        image.save(f'{self.OUTPUTDIR}{os.path.sep}{imagename}')

    # None -> None
    def start(self):
        # Start Processing Image
        if not os.path.exists(self.OUTPUTDIR):
            os.mkdir(self.OUTPUTDIR)

        # Read Csv File
        with open(self.CSVFILENAME, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)
            # Iter All Fields in .csv File and Process Images
            # Images Writed in .csv File in Last Column
            for row in reader:
                self.process_image(row[-1].strip(), row[1].strip(), row[0].strip())


if __name__ == '__main__':
    app = Main()
    app.start()
