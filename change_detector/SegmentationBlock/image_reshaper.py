import cv2

class ImageReshaper:

    def split(self, image, size):
        try:
            if size < 1:
                raise Exception("block size can not be less than one.")
            if size > image.shape[0]:
                raise Exception("block size can not be greater than image size.")
            blocks_number = int((10980 * 10980) / (size * size))
            blocks_row = int(10980 / size)
            x = 0
            y = 0
            blocks = []
            for c in range(int(blocks_number)):
                i = y * size
                j = x * size
                blocks.append(image[i:(i + size), j:(j + size)])
                x += 1
                if x == blocks_row:
                    x = 0
                    y += 1

            return blocks
        except Exception:
            return None

    def merge(self, blocks):
        try:
            if blocks == None:
                raise Exception("blocks can not be None value.")
            size = blocks[0].shape[0]
            if (10980 * 10980) / (size * size) != len(blocks):
                raise Exception("invalid blocks array.")
            image_raw = []
            blocks_number = int((10980 * 10980) / (size * size))
            blocks_row = int(10980 / size)
            for c in range(0, int(blocks_number), blocks_row):
                image_raw.append(blocks[c : (c + blocks_row)])
            image = self.concat_vh(image_raw)
            return image
        except Exception:
            return None
    
    def concat_vh(self, list_2d):
        return cv2.vconcat([cv2.hconcat(list_h) 
                            for list_h in list_2d])