import pygame, random

pygame.init()

# 색 초기화
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (155, 155,0)

COLORS = (BLUE, GREEN, RED, YELLOW)

#스크린 사이즈 정해놓기
size = [400, 500]
screen = pygame.display.set_mode(size)
BOXSIZE = 20
XMARGIN = 75
TOPMARGIN = 10
BLANK = '.'


pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()

rot = 0

lead_x = 75
lead_y = 10

#모양 정의
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                      '.....',
                      '..OO.',
                      '.OO..',
                      '.....'],

                     ['.....',
                      '..O..',
                      '..OO.',
                      '...O.',
                      '.....']]



Z_SHAPE_TEMPLATE = [['.....',
                       '.....',
                       '.OO..',
                       '..OO.',
                       '.....'],

                      ['.....',
                       '..O..',
                      '.OO..',
                      '.O...',
                      '.....']]



I_SHAPE_TEMPLATE = [['..O..',
                      '..O..',
                      '..O..',
                      '..O..',
                      '.....'],

                     ['.....',
                      '.....',
                      'OOOO.',
                      '.....',
                      '.....']]



O_SHAPE_TEMPLATE = [['.....',
                      '.....',
                      '.OO..',
                      '.OO..',
                      '.....']]



J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                      '.OOO.',
                      '.....',
                      '.....'],

                     ['.....',
                      '..OO.',
                      '..O..',
                      '..O..',
                      '.....'],

                     ['.....',
                      '.....',
                      '.OOO.',
                      '...O.',
                      '.....'],

                     ['.....',
                      '..O..',
                      '..O..',
                      '.OO..',
                      '.....']]



L_SHAPE_TEMPLATE = [['.....',
                      '...O.',
                      '.OOO.',
                      '.....',
                      '.....'],

                     ['.....',
                      '..O..',
                      '..O..',
                      '..OO.',
                      '.....'],

                     ['.....',
                      '.....',
                      '.OOO.',
                      '.O...',
                      '.....'],

                     ['.....',
                      '.OO..',
                      '..O..',
                      '..O..',
                      '.....']]



T_SHAPE_TEMPLATE = [['.....',
                      '..O..',
                      '.OOO.',
                      '.....',
                      '.....'],

                     ['.....',
                      '..O..',
                      '..OO.',
                      '..O..',
                      '.....'],

                     ['.....',
                      '.....',
                      '.OOO.',
                      '..O..',
                      '.....'],

                     ['.....',
                      '..O..',
                      '.OO..',
                      '..O..',
                      '.....']]



SHAPES = {'S': S_SHAPE_TEMPLATE,
           'Z': Z_SHAPE_TEMPLATE,
           'J': J_SHAPE_TEMPLATE,
           'L': L_SHAPE_TEMPLATE,
           'I': I_SHAPE_TEMPLATE,
           'O': O_SHAPE_TEMPLATE,
           'T': T_SHAPE_TEMPLATE}

#모양 정의 끝

grid = [[1]*10 for n in range(20)]

#그리드 만들기
def draw_grid():
    x = 75
    y = 10
    for row in grid:
        for col in row:
            pygame.draw.rect(screen, WHITE, [x,y,20,20], 2)
            x = x + 20
        x = 75
        y = y + 20

#새 조각 생성하기
#piece를 반환한다.
#dictionary 형태로 piece 정보를 묘사한다.
# 정보:
# shape(블럭 모양), rotation(얼마나 회전하는지),
# x(보드 내에서 가로 좌표), y(보드 내에서 세로 좌표), color(블럭 색)
def getNewPiece():
    #'S', 'Z', 'J', 'L' , 'I' , 'O', 'T' 중 하나
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {
        'shape': shape,
        'rotation': random.randint(0, len(SHAPES[shape])-1),
        'x' : int(10 / 2) - int (5/2),
        'y' : 0,
        'color': random.randint(0, len(COLORS)-1)
    }
    return newPiece

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None :
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(screen, COLORS[color], (pixelx +1, pixely +1, BOXSIZE -1, BOXSIZE -1))

def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawPiece(piece, pixelx= None, pixely = None):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

'''
조각이 board내에 있는지 확인하는 함수
# (삐져나오면 안되지)
'''
def isOnBoard(x,y):
    return (x >= 0 ) and x < 10 and y < 20

def isValidPosition(piece, adjX = 0, adjY = 0):
    shapeToCheck = SHAPES[piece['shape']][piece['rotation']]

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            print("aaaa", x, piece['x'], adjX)
            if shapeToCheck[y][x] != BLANK and not isOnBoard(x + piece['x'] + adjX,y +piece['y'] + adjY):
                return False
    return True

'''
조각이 board 내에 있는지 확인하는 함수 끝
'''

fallingPiece = getNewPiece()

while not done:
    clock.tick(10)

    # Main Event Loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            continue
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT) and isValidPosition(fallingPiece, 1,0):
                fallingPiece['x'] +=1
                #lead_x += 20
            elif (event.key == pygame.K_LEFT) and isValidPosition(fallingPiece, -1,0):
                fallingPiece['x'] -= 1
                #lead_x -= 20
            elif (event.key == pygame.K_DOWN) and isValidPosition(fallingPiece, 0,1):
                fallingPiece['y'] += 1
                #lead_y += 20
            elif (event.key == pygame.K_UP) and isValidPosition(fallingPiece, 0 , -1):
                fallingPiece['y'] -= 1
                #lead_y -= 20
            elif event.key == pygame.K_s:
                fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
                #rot = (rot + 90) % 360


    screen.fill(BLACK)
    # Draw a rectangle outline
    pygame.draw.rect(screen, WHITE, [75, 10, 200, 400], 2)
    draw_grid()

    drawPiece(fallingPiece)

    # tetrimino = pygame.Surface((60,20))
    # tetrimino.set_colorkey(WHITE)
    # tetrimino.fill(RED)
    # new_tetrimino = pygame.transform.rotate(tetrimino, rot)
    #
    # screen.blit(new_tetrimino, (lead_x, lead_y))

    #obj = pygame.draw.rect(screen, RED, [lead_x, lead_y, 60, 20])

    # Draw a solid rectangle
    #pygame.draw.rect(screen, RED, [150, 10, 50, 20])

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()


# Be IDLE friendly
pygame.quit()
