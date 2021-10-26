from tile import TileMap

def open_map(map_file: str) -> TileMap:
    file1 = open('maps/map1.map', 'r')
    file_lines = file1.readlines()
    map_array = []

    for line in file_lines:
        map_array.append(line.replace('\n', '').split(','))

    if len(map_array) == 0 or len(map_array[0]) == 0:
        return None

    map_height = len(map_array)
    map_width = len(map_array[0])

    tilemap = TileMap(map_width, map_height)

    for i in range(0, map_height):
        for j in range(0, map_width):
            if map_array[i][j] == '0':
                continue
            if map_array[i][j].isnumeric():
                tilemap.setvalue(i, j, int(map_array[i][j]))
            else:
                raise(Exception("File '" + map_file + "' contains an invalid value at position " + str(i) + "," + str(j) + " ('" + map_array[i][j] + "')"))

    return tilemap

tilemap = open_map('maps/map1.map')
print(str(tilemap))