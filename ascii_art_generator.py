from PIL import Image
import sys

class Ascii_Art_Generator:
    ASCII_LIST = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
    PIXEL_RANGE = 25

    def __init__(self, image_path):
        self.image = None
        try:
            self.image = Image.open(image_path)
        except IOError:
            print "can't open the image file{image_path}".format(image_path = image_path)
            exit(-1)


    def __del__(self):
        self.image.close()

    def convert_to_ascii(self):
        # convert to grayscale
        new_image = self.image.convert(mode = 'L')

        # resize the image
        (original_width, original_height) = new_image.size
        new_width = 100
        new_height = new_width * original_height / original_width
        new_image = new_image.resize((new_width, new_height))

        # map pixels to ascii chars
        pixels = list(new_image.getdata())
        pixels_to_chars = [self.ASCII_LIST[pixel / self.PIXEL_RANGE] for pixel in pixels]
        result = "".join(pixels_to_chars)

        # save result
        with open('result.txt', mode='a') as fhand:
            for i in range(0, len(result), new_width):
                fhand.write(result[i : i + new_width])
                fhand.write('\n')



if __name__ == '__main__':
    generator = Ascii_Art_Generator(sys.argv[1])
    generator.convert_to_ascii()
