from PIL import Image


_WRITE = Image.open("BLANK.png")
_WRITE_PIXELS = _WRITE.load()

_IMAGE = Image.open("image.png")
_FILE = open("coord.txt", "a")
_PASSED = []
_STARTING = True

RANGE = 8 + 1

START = (447, 251)

RIGHT = "RIGHT"
LEFT = "LEFT"
UP = "UP"
DOWN = "DOWN"


def writeCoord(a):
    if a is not None:
        _FILE.write("{x},{y},0,\n".format(x=str(a[0]), y=str(a[1])))


def writeRedPixel(x, y):
    _WRITE_PIXELS[x, y] = (255, 0, 0)


def writeBluePixel(x, y):
    _WRITE_PIXELS[x, y] = (0, 0, 255)


def markCoordinates(x, y):
    global _PASSED
    _PASSED.append((x, y))


def getRangePoints(p, direction):
    global _PASSED
    coordinates = []
    if direction == LEFT:
        a = p[1] - RANGE
        b = p[1] + RANGE
        c = p[0]
        for i in range(a, b):
            for j in range(c, c - RANGE, -1):
                if _IMAGE.getpixel((j, i))[0] < 50 and (j, i) not in _PASSED:
                    markCoordinates(j, i)
                    coordinates.append((j, i))
                    writeRedPixel(j, i)
    elif direction == RIGHT:
        a = p[1] - RANGE
        b = p[1] + RANGE
        c = p[0]
        for i in range(a, b):
            for j in range(c, c + RANGE):
                if _IMAGE.getpixel((j, i))[0] < 50 and (j, i) not in _PASSED:
                    markCoordinates(j, i)
                    coordinates.append((j, i))
                    writeRedPixel(j, i)
    elif direction == UP:
        a = p[0] - RANGE
        b = p[0] + RANGE
        c = p[1]
        for i in range(a, b):
            for j in range(c, c - RANGE, -1):
                if _IMAGE.getpixel((i, j))[0] < 50 and (i, j) not in _PASSED:
                    markCoordinates(i, j)
                    coordinates.append((i, j))
                    writeRedPixel(i, j)
    elif direction == DOWN:
        a = p[0] - RANGE
        b = p[0] + RANGE
        c = p[1]
        for i in range(a, b):
            for j in range(c, c + RANGE):
                if _IMAGE.getpixel((i, j))[0] < 50 and (i, j) not in _PASSED:
                    markCoordinates(i, j)
                    coordinates.append((i, j))
                    writeRedPixel(i, j)
    return coordinates


def getNextPoint(point, direction):
    nexts = getRangePoints(point, direction)
    if START in nexts and not _STARTING:
        return START
    if len(nexts) == 0:
        return None
    return nexts[-1]


writeCoord(START)
TEMP = START


temp = getNextPoint(START, RIGHT)
_PASSED.remove(START)
_WRITE_PIXELS[temp[0], temp[1]] = (0, 0, 255)

DIRECTION = RIGHT
while True:
    if DIRECTION is RIGHT and temp is None:
        DIRECTION = DOWN
    elif DIRECTION is DOWN and temp is None:
        DIRECTION = LEFT
    elif DIRECTION is LEFT and temp is None:
        DIRECTION = UP
    elif DIRECTION is UP and temp is None:
        DIRECTION = RIGHT
    if temp is None:
        if last == START and not _STARTING:
            break
        temp = getNextPoint(last, DIRECTION)
        continue
    last = temp
    temp = getNextPoint(temp, DIRECTION)

    if temp is not None:
        _WRITE_PIXELS[temp[0], temp[1]] = (0, 0, 255)
        writeBluePixel(temp[0], temp[1])
        writeCoord(temp)
        writeCoord(temp)

    _STARTING = False


_IMAGE.close()
_WRITE.save("OUTPUT.png")
_WRITE.close()
_FILE.close()
