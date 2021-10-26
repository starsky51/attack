# import libraries
import pygame
from pygame.surfarray import array2d

class Tile:
    image: pygame.Surface
    width: int
    height: int

    def __init__(self, image_file: str, width: int = 0, height: int = 0) -> None:
        original_image : pygame.Surface = pygame.image.load(image_file).convert_alpha()
        self.width = width if width > 0 else original_image.get_width()
        self.height = height if height > 0 else original_image.get_height()
        self.image = pygame.transform.scale(original_image, (width, height))
        return None

    def get_image(self, flip_x: bool = False, flip_y: bool = False) -> pygame.Surface:
        if flip_x | flip_y:
            return pygame.transform.flip(self.image, flip_y, flip_x)
        return self.image

class TileMap:
    width: int
    height: int
    filename: str = ""
    __array: array2d
    player_starts = {}

    def __init__(self, *args) -> None:
        # check args for width/height or filename_str
        if len(args) == 2 and type(args[0]) == int and type(args[1]) == int:
            # width/length arguments
            self.width = args[0]
            self.height = args[1]
            self.__array = [ [0] * self.width for _ in range(self.height)]
        elif len(args) == 1 and type(args[0]) == str:
            # filename argument
            self.filename = args[0]
            file1 = open(self.filename, 'r')
            file_lines = file1.readlines()
            map_array = []

            for line in file_lines:
                map_array.append(line.replace('\n', '').split(','))

            if len(map_array) == 0 or len(map_array[0]) == 0:
                return None

            self.height = len(map_array)
            self.width = len(map_array[0])
            self.__array = [ [0] * self.height for _ in range(self.width)]

            for j in range(0, self.height):
                for i in range(0, self.width):
                    # map_array is stored in y, x order (ie. each line of the file is on y-axis)
                    if map_array[j][i] == '0':
                        continue
                    elif map_array[j][i].isnumeric():
                        self.setvalue(i, j, int(map_array[j][i]))
                    elif map_array[j][i] == 'A':
                        self.player_starts['1'] = (i, j)
                        self.player_starts['2'] = (i+2, j)
                        self.player_starts['3'] = (i+4, j)
                        self.player_starts['4'] = (i+6, j)
                    else:
                        raise(Exception("File '" + self.filename + "' contains an invalid value at position " + str(i) + "," + str(j) + " ('" + map_array[i][j] + "')"))

        return None

    def getvalue(self, x: int, y: int) -> int:
        return self.__array[x][y]

    def setvalue(self, x: int, y: int, value: int) -> bool:
        self.__array[x][y] = value
        return True
    
    def __str__(self) -> str:
        map_str: str = ""

        for j in range(0, self.height):
            str_ints = [str(int) for int in self.__array[j]] 
            map_str += ','.join(str_ints) + '\n'
        
        return map_str