import pygame
import sys


class Plate:
    """
    定义托盘
    """
    def __init__(self, surface, width, height):
        self.surface = surface
        self.width = width
        self.rect = pygame.Rect(width / 3, height - 10, width / 4, 10)
        self.colorIdx = 0
        self.colorList = []
        self.colorList.append(pygame.Color(0, 200, 0))
        self.colorList.append(pygame.Color(200, 0, 0))
        self.colorList.append(pygame.Color(0, 0, 200))
        self.color = self.colorList[self.colorIdx]
        self.speed = 10
        self.dir = 0

    def left(self):
        if self.dir != 0:
            self.dir = 0
            self.speed = -10
        else:
            self.speed -= 5
        if self.speed < -30:
            self.speed = -30
        if self.rect.left < -self.speed:
            self.rect.left = 0
            return
        self.rect = self.rect.move(self.speed, 0)

    def right(self):
        if self.dir != 1:
            self.dir = 1
            self.speed = 10
        else:
            self.speed += 5
        if self.speed > 30:
            self.speed = 30
        if self.rect.right >= self.width - self.speed:
            self.rect.right = self.width
            return
        self.rect = self.rect.move(self.speed, 0)

    def update(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def hit_ball(self, ball):
        self.colorIdx += 1
        if self.colorIdx > 2:
            self.colorIdx = 0
        self.color = self.colorList[self.colorIdx]
        ball.speed[0] += int(self.speed / 4)


class CircleBall:
    """
    定义小球
    """
    def __init__(self, surface, width, height):
        self.surface = surface
        self.rect = pygame.Rect(width / 2, height - 15, 4, 4)
        self.colorIdx = 0
        self.colorList = []
        self.colorList.append(pygame.Color(0, 200, 0))
        self.colorList.append(pygame.Color(200, 0, 0))
        self.colorList.append(pygame.Color(0, 0, 200))
        self.color = self.colorList[self.colorIdx]
        self.speed = [4, -4]
        self.lunched = False
        self.lives = 3

    def move(self):
        self.rect = self.rect.move(self.speed)

    def move_in_window(self, width, height):
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0:
            self.speed[1] = -self.speed[1]
        if self.rect.bottom > height - 10:
            # self.rect = pygame.Rect(width / 2, height - 15, 4, 4)
            self.colorIdx = 0
            self.speed = [4, -4]
            self.lunched = False
            if self.lives:
                self.lives -= 1
            return
        self.move()

    def move_with_plate(self, onplate):
        self.rect.x = onplate.rect.midtop[0] - 5
        self.rect.y = onplate.rect.midtop[1] - 10

    def ball_move(self, width, height, onplate):
        if self.lunched:
            self.move_in_window(width, height)
        else:
            self.move_with_plate(onplate)

    def update(self):
        pygame.draw.circle(self.surface, self.color, (self.rect.x + 4, self.rect.y + 4), 4)

    def hit_plate(self):
        self.colorIdx += 1
        if self.colorIdx > 2:
            self.colorIdx = 0
        self.color = self.colorList[self.colorIdx]
        self.speed[1] = -self.speed[1]
        self.rect = self.rect.move(self.speed)


class Brick:
    """
    定义砖块
    """
    def __init__(self, surface, x, y, brickWidth, brickHeight):
        self.brickHeight = brickHeight
        self.brickWidth = brickWidth
        self.surface = surface
        self.x, self.y = x, y
        self.color = pygame.Color(100, 30, 90)
        self.rect = pygame.Rect(x, y, brickWidth, brickHeight)

    def update(self):
        pygame.draw.rect(self.surface, self.color, self.rect)


class BrickMap:
    """
    生成砖块
    """
    def __init__(self, surface, width, height):
        xnum = 15
        ynum = 15
        xoffset = int(width / xnum)
        brick_width = xoffset - 7
        yoffset = int((height / 2) / ynum)
        brick_height = yoffset - 7
        self.bricks = []
        for i in range(xnum - 1):
            for j in range(ynum - 1):
                self.bricks.append(
                    Brick(surface, xoffset / 2 + xoffset * i, yoffset / 2 + yoffset * (j + 1), brick_width,
                          brick_height))


pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
black = 0, 0, 0
plate = Plate(screen, width, height)
pygame.key.set_repeat(50)
ball = CircleBall(screen, width, height)
brickMap = BrickMap(screen, width, height)
font = pygame.font.SysFont('Arial', 28)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                plate.left()
            elif key[pygame.K_d]:
                plate.right()
            elif key[pygame.K_SPACE]:
                ball.lunched = True
                if ball.lives == 0:
                    brickMap = BrickMap(screen, width, height)
                    ball.lives = 3
                if len(brickMap.bricks) == 0:
                    brickMap = BrickMap(screen, width, height)
            else:
                plate.speed = 0
                plate.dir = 2
        else:
            plate.speed = 0
            plate.dir = 2
    # 移动小球
    ball.ball_move(width, height, plate)
    # 检测托盘
    if ball.rect.colliderect(plate.rect):
        plate.hit_ball(ball)
        ball.hit_plate()
    # 检测砖块碰撞
    for b in brickMap.bricks:
        if ball.rect.colliderect(b):
            brickMap.bricks.remove(b)
            if b.rect.collidepoint(ball.rect.midleft[0], ball.rect.midleft[1]):
                ball.speed[0] = -ball.speed[0]
            elif b.rect.collidepoint(ball.rect.midright[0], ball.rect.midright[1]):
                ball.speed[0] = -ball.speed[0]
            elif b.rect.collidepoint(ball.rect.midtop[0], ball.rect.midtop[1]):
                ball.speed[1] = -ball.speed[1]
            elif b.rect.collidepoint(ball.rect.midbottom[0], ball.rect.midbottom[1]):
                ball.speed[1] = -ball.speed[1]
    # 重绘显示区域
    screen.fill(black)
    s = font.render("life: " + str(ball.lives), True, [100, 100, 100])
    srect = s.get_rect()
    srect.x = width - srect.width - 20
    srect.y = height - srect.height - 5
    screen.blit(s, srect)
    plate.update()
    ball.update()
    # 显示提示信息
    if ball.lives == 0 or not ball.lunched:
        s2 = font.render("Press Space to Play!", True, [100, 100, 100])
        srect = s2.get_rect()
        srect.x = (width - srect.width) / 2
        srect.y = height / 2
        screen.blit(s2, srect)
    if len(brickMap.bricks) == 0:
        s3 = font.render("Good Job!", True, [100, 100, 100])
        srect = s3.get_rect()
        srect.x = (width - srect.width) / 2
        srect.y = height / 2
        screen.blit(s3, srect)
        ball.lunched = False
    for b in brickMap.bricks:
        b.update()
    pygame.display.flip()
    clock.tick(60)
