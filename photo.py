import random
from PIL import Image


class Photo:

    def __init__(self, image, patch_size):
        self.image = image
        self.patch_size = patch_size
        self.inequal = -1

    def split_image(self):
        tiles = []
        if self.patch_size % 2 == 0:
            for i in range(1,3):
                j = 1
                while j <= self.patch_size // 2:
                    tiles.append(self.crop_image(i, (self.image.height // (self.patch_size // 2))*j, (self.image.height // (self.patch_size // 2))*(j-1)))
                    j += 1
        else:
            if self.inequal == -1:
                for i in range(1,3):
                    j = 1
                    while j <= (self.patch_size-1) // 2:
                        tiles.append(self.crop_image(i, (self.image.height // ((self.patch_size+1) // 2))*j, (self.image.height // ((self.patch_size+1) // 2))*(j-1)))
                        j += 1
                tiles.append(self.crop_image(3, self.image.height, self.image.height - self.image.height // ((self.patch_size+1)// 2)))
                self.inequal = (self.patch_size + 1) // 2
            else:
                for i in range(1, 3):
                    j = 1
                    while j <= (self.patch_size - 1) // 2:
                        if j != self.inequal:
                            tiles.append(self.crop_image(i, (self.image.height // ((self.patch_size + 1) // 2)) * j,
                                                         (self.image.height // ((self.patch_size + 1) // 2)) * (j - 1)))
                        j += 1
                tiles.append(self.crop_image(3, (self.image.height // ((self.patch_size + 1) // 2)) * self.inequal,
                                             (self.image.height // ((self.patch_size + 1) // 2)) * (self.inequal - 1)))
        return tiles

    def crop_image(self, half, bottom, top):
        if half == 1:
            return self.image.crop((0, top, self.image.width/2, bottom)).convert('L')
        elif half == 2:
            return self.image.crop((self.image.width/2, top, self.image.width, bottom)).convert('L')
        elif half == 3:
            return self.image.crop((0, top, self.image.width, bottom)).convert('L')
        else:
            return None

    def paste_image(self, half, top, board,image):
        if half == 1:
            board.paste(image, (0, top))
        elif half==2:
            board.paste(image, (self.image.width // 2, top))
        elif half == 3:
            board.paste(image, (0, top))

    def combine_images(self, tiles, image):
        if len(tiles) % 2 == 0:
            for i in range(0, len(tiles)//2):
                self.paste_image(1, (self.image.height // (len(tiles) // 2))*i, image, tiles[i])
            for i in range(len(tiles) // 2, len(tiles)):
                self.paste_image(2, (self.image.height // (len(tiles) // 2))*(i - len(tiles) // 2), image, tiles[i])
        else:
            inequal_index = 0
            for i in range(0, len(tiles)):
                if tiles[i].width == self.image.width:
                    inequal_index = i
            row_count = (len(tiles) + 1) // 2
            if inequal_index > row_count:
                inequal_row = (inequal_index + 1) % row_count
            elif inequal_index == row_count and inequal_index != len(tiles) - 1:
                inequal_row = 0
            elif inequal_index == row_count and inequal_index == len(tiles) - 1:
                inequal_row = 1
            else:
                inequal_row = inequal_index
            self.paste_image(3, (self.image.height // ((len(tiles) + 1) // 2)) * inequal_row, image, tiles[inequal_index])
            inequal_height = (self.image.height // ((len(tiles) + 1) // 2)) * inequal_row
            self.inequal = inequal_row
            j = 0
            counter = 0
            for i in range(0, (len(tiles) + 1) // 2):
                height = (self.image.height // ((len(tiles) + 1) // 2))*j
                if height == inequal_height and i == inequal_index:
                    j += 1
                    counter += 1
                elif height == inequal_height:
                    height = (self.image.height // ((len(tiles) + 1) // 2)) * (j+1)
                    self.paste_image(1, height, image, tiles[i])
                    j += 2
                    counter += 2
                else:
                    self.paste_image(1,  height, image, tiles[i])
                    j += 1
            if counter >= ((len(tiles) - 1) // 2) - 1:
                start = (len(tiles) - 1) // 2
            else:
                start = (len(tiles) + 1) // 2
            j = (len(tiles) - 1) // 2
            for i in range(start, len(tiles)):
                height = (self.image.height // ((len(tiles) + 1) // 2))*(j - (len(tiles) - 1) // 2)
                if height == inequal_height and i == inequal_index:
                    j += 1
                elif height == inequal_height:
                    height = (self.image.height // ((len(tiles) + 1) // 2))*(j+1 - (len(tiles) - 1) // 2)
                    self.paste_image(2, height, image, tiles[i])
                    j += 2
                else:
                    self.paste_image(2, height, image, tiles[i])
                    j += 1
        return image

    def shuffle_image(self):
        tiles = self.split_image()
        random.shuffle(tiles)
        image = Image.new("L", self.image.size)
        return Photo(self.combine_images(tiles, image), self.patch_size)

    def compare(self, image):
        original_photo = Photo(self.combine_images(self.split_image(), Image.new('L', self.image.size)), self.patch_size)
        if self.patch_size % 2 == 0:
            patches = self.patch_size
        else:
            patches = self.patch_size + 1
        similar_parts = 0
        for i in range(1, 3):
            j = 1
            while j <= patches // 2:
                original_part = original_photo.crop_image(i, (original_photo.image.height // (patches // 2)) * j
                                                , (original_photo.image.height // (patches // 2)) * (j - 1))
                shuffled_part = image.crop_image(i, (image.image.height // (patches // 2)) * j
                                                                , (image.image.height // (patches // 2)) * (j - 1))
                if list(original_part.getdata()) == list(shuffled_part.getdata()):
                    similar_parts += 1
                j += 1
        percentage = (similar_parts / patches) * 100
        return percentage














