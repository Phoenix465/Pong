# Library Imports
import pygame
from math import sin, cos, pi, asin
from random import randint


class PongHandler:
    def __init__(self):
        # Initialising Components
        pygame.init()

        pygame.display.set_caption('Pong')
        WindowIcon = pygame.image.load("PingPong.jpg")
        (self.screenWidth, self.screenHeight) = (1200, 700)
        self.background_colour = (50, 50, 50)

        # Initial Settings - DON'T TOUCH
        self.windowScreen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.windowScreen.fill(self.background_colour)

        pygame.display.set_icon(WindowIcon)
        pygame.display.flip()

        self.setting = None
        self.leftscore = 0
        self.rightscore = 0
        self.gamesetttings()

        if self.setting == ["MP"]:
            self.P1 = self.HumanPaddle(self.screenHeight, self.screenWidth, True, pygame.K_w, pygame.K_s)
            self.P2 = self.HumanPaddle(self.screenHeight, self.screenWidth, False, pygame.K_UP, pygame.K_DOWN)

        elif self.setting[0] == "SP":
            self.P1 = self.HumanPaddle(self.screenHeight, self.screenWidth, True, pygame.K_w, pygame.K_s)
            self.Computer = self.ComputerPaddle(self.screenHeight, self.screenWidth)

            self.Computer.setspeed(5)

        self.BallObj = self.Ball(self.screenHeight, self.screenWidth)

    def drawroundrect(self, colour, rect, circleR=0, thicknessOut=True):
        #  colour = (R, G, B)
        #  rect = (x, y, width, height)
        #  rect coordinates describe the middle rectangle
        #  circleR = radius of thickness

        if not thicknessOut:
            rect = (rect[0] + circleR, rect[1] + circleR, rect[2] - (2 * circleR), rect[3] - (2 * circleR))

        pygame.draw.circle(self.windowScreen, colour, (rect[0], rect[1]), circleR)
        pygame.draw.circle(self.windowScreen, colour, (rect[0] + rect[2], rect[1]), circleR)
        pygame.draw.circle(self.windowScreen, colour, (rect[0], rect[1] + rect[3]), circleR)
        pygame.draw.circle(self.windowScreen, colour, (rect[0] + rect[2], rect[1] + rect[3]), circleR)

        pygame.draw.rect(self.windowScreen, colour, rect)

        pygame.draw.rect(self.windowScreen, colour, (rect[0] + rect[2], rect[1], circleR, rect[3]))
        pygame.draw.rect(self.windowScreen, colour, (rect[0] - circleR, rect[1], circleR, rect[3]))

        pygame.draw.rect(self.windowScreen, colour, (rect[0], rect[1] - circleR, rect[2], circleR))
        pygame.draw.rect(self.windowScreen, colour, (rect[0], rect[1] + rect[3], rect[2], circleR))

        return [rect[0] - circleR, rect[0] + rect[2] + circleR, rect[1] - circleR, rect[1] + rect[3] + circleR]

    def gamesetttings(self):
        mode = None
        level = {0: "EASY", 1: "MEDIUM", 2: "HARD", 3: "IMPOSSIBLE?"}

        while self.setting is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.windowScreen.fill(self.background_colour)

            mouseCoord = pygame.mouse.get_pos()
            leftC, _, _ = pygame.mouse.get_pressed()

            textSettings = pygame.font.Font('freesansbold.ttf', 50)

            Text = textSettings.render("Pong", True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.center = (self.screenWidth // 2, 50)
            self.windowScreen.blit(Text, TextRect)

            if mode is None:
                textSettings = pygame.font.Font('freesansbold.ttf', 39)
                sButton = (self.screenWidth // 2 - 140, self.screenWidth // 2 + 140, 200, 250)
                self.drawroundrect((255, 255, 255), (sButton[0], sButton[2], sButton[1] - sButton[0], sButton[3] - sButton[2]), 20, False)
                Text = textSettings.render("Single Player", True, (0, 0, 0))
                TextRect = Text.get_rect()
                TextRect.center = (self.screenWidth // 2, 225)
                self.windowScreen.blit(Text, TextRect)

                textSettings = pygame.font.Font('freesansbold.ttf', 39)
                mButton = (self.screenWidth // 2 - 140, self.screenWidth // 2 + 140, 300, 350)
                self.drawroundrect((255, 255, 255), (mButton[0], mButton[2], mButton[1] - mButton[0], mButton[3] - mButton[2]), 20, False)
                Text = textSettings.render("Two Player", True, (0, 0, 0))
                TextRect = Text.get_rect()
                TextRect.center = (self.screenWidth // 2, 325)
                self.windowScreen.blit(Text, TextRect)

                if sButton[0] < mouseCoord[0] < sButton[1] and sButton[2] < mouseCoord[1] < sButton[3] and leftC and mode is None:
                    mode = "SP"

                if mButton[0] < mouseCoord[0] < mButton[1] and mButton[2] < mouseCoord[1] < mButton[3] and leftC and mode is None:
                    mode = "MP"

            if mode == "SP":
                for hardness in range(4):
                    textSettings = pygame.font.Font('freesansbold.ttf', 39)
                    location = (self.screenWidth // 2 - 140, self.screenWidth // 2 + 140, 250 + (100 * hardness), 300 + (100 * hardness))
                    self.drawroundrect((255, 255, 255), (location[0], location[2], location[1] - location[0], location[3] - location[2]), 20, False)

                    Text = textSettings.render(level[hardness], True, (0, 0, 0))
                    TextRect = Text.get_rect()
                    TextRect.center = (self.screenWidth // 2, location[2] + 25)
                    self.windowScreen.blit(Text, TextRect)

                    if location[0] < mouseCoord[0] < location[1] and location[2] < mouseCoord[1] < location[3] and leftC:
                        mode = "SP2"
                        levelchosen = level[hardness]

            if mode == "SP2":
                textSettings = pygame.font.Font('freesansbold.ttf', 39)

                location = (self.screenWidth // 2 - 300, self.screenWidth // 2 + 300, 250, 300)
                location2 = (self.screenWidth // 2 - 50, self.screenWidth // 2 + 50, 600, 650)

                self.drawroundrect((255, 255, 255), (location[0], location[2], location[1] - location[0], location[3] - location[2]), 20, False)
                self.drawroundrect((255, 255, 255), (location2[0], location2[2], location2[1] - location2[0], location2[3] - location2[2]), 20, False)

                Text = textSettings.render("Player LEFT Uses 'W' & 'S'", True, (0, 0, 0))
                TextRect = Text.get_rect()
                TextRect.center = (self.screenWidth // 2, location[2] + 25)
                self.windowScreen.blit(Text, TextRect)

                Text = textSettings.render("OK", True, (0, 0, 0))
                TextRect = Text.get_rect()
                TextRect.center = (self.screenWidth // 2, location2[2] + 25)
                self.windowScreen.blit(Text, TextRect)

                if location2[0] < mouseCoord[0] < location2[1] and location2[2] < mouseCoord[1] < location2[3] and leftC:
                    self.setting = ["SP", levelchosen]

            if mode == "MP":
                textSettings = pygame.font.Font('freesansbold.ttf', 39)
                location = (self.screenWidth // 2 - 300, self.screenWidth // 2 + 300, 250, 300)
                location2 = (self.screenWidth // 2 - 500, self.screenWidth // 2 + 500, 350, 400)
                location3 = (self.screenWidth // 2 - 50, self.screenWidth // 2 + 50, 550, 600)

                self.drawroundrect((255, 255, 255), (location[0], location[2], location[1] - location[0], location[3] - location[2]), 20, False)
                self.drawroundrect((255, 255, 255), (location2[0], location2[2], location2[1] - location2[0], location2[3] - location2[2]), 20, False)
                self.drawroundrect((255, 255, 255), (location3[0], location3[2], location3[1] - location3[0], location3[3] - location3[2]), 20, False)

                Text = textSettings.render("Player LEFT Uses 'W' & 'S'", True, (0, 0, 0))
                TextRect = Text.get_rect()
                TextRect.center = (self.screenWidth // 2, location[2] + 25)
                self.windowScreen.blit(Text, TextRect)

                Text = textSettings.render("Player RIGHT Uses 'UP ARROW' & 'DOWN ARROW'", True, (0, 0, 0))
                TextRect = Text.get_rect()
                TextRect.center = (self.screenWidth // 2, location2[2] + 25)
                self.windowScreen.blit(Text, TextRect)

                Text = textSettings.render("OK", True, (0, 0, 0))
                TextRect = Text.get_rect()
                TextRect.center = (self.screenWidth // 2, location3[2] + 25)
                self.windowScreen.blit(Text, TextRect)

                if location3[0] < mouseCoord[0] < location3[1] and location3[2] < mouseCoord[1] < location3[3] and leftC:
                    self.setting = ["MP"]

            pygame.display.update()

    def update(self):
        running = True
        self.BallObj.update(True)
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.windowScreen.fill(self.background_colour)

            for x in range(13):
                pygame.draw.rect(self.windowScreen, (255, 255, 255), (((self.screenWidth // 2) - 3), 55 * x, 6, 20))

            textSettings = pygame.font.Font('freesansbold.ttf', 50)

            Text = textSettings.render(str(self.leftscore), True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.x = self.screenWidth // 2 - 30 - TextRect.width
            TextRect.y = 30
            self.windowScreen.blit(Text, TextRect)

            Text = textSettings.render(str(self.rightscore), True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.x = self.screenWidth // 2 + 30
            TextRect.y = 30
            self.windowScreen.blit(Text, TextRect)

            #self.P1.position[1] = self.BallObj.position[1] - (self.P1.height//2)
            #self.P2.position[1] = self.BallObj.position[1] - (self.P2.height//2)

            Ball = pygame.draw.rect(self.windowScreen, (255, 255, 255), [self.BallObj.position[0] - self.BallObj.radius, self.BallObj.position[1] - self.BallObj.radius, self.BallObj.radius, self.BallObj.radius], )
            P1Paddle = pygame.draw.rect(self.windowScreen, (255, 255, 255), self.P1.position)

            if P1Paddle.colliderect(Ball):
                self.BallObj.vx = -self.BallObj.vx
                self.BallObj.position[0] = P1Paddle.x + P1Paddle.width + self.BallObj.radius + 5
                self.BallObj.angle += randint(-20, 20)
                self.BallObj.updatevelo()

            self.P1.update()

            self.BallObj.update(None)

            if self.setting == ["MP"]:
                P2Paddle = pygame.draw.rect(self.windowScreen, (255, 255, 255), self.P2.position)

                if P2Paddle.colliderect(Ball):
                    self.BallObj.vx = -self.BallObj.vx
                    self.BallObj.position[0] = P2Paddle.x - self.BallObj.radius - 5
                    self.BallObj.angle += randint(-20, 20)
                    self.BallObj.updatevelo()

                self.P2.update()

            if self.setting[0] == "SP":
                tempLoc = self.Computer.position.copy()
                tempLoc[1] -= self.Computer.height // 2
                ComputerPaddle = pygame.draw.rect(self.windowScreen, (255, 255, 255), tempLoc)

                if ComputerPaddle.colliderect(Ball):
                    self.BallObj.vx = -self.BallObj.vx
                    self.BallObj.position[0] = ComputerPaddle.x - self.BallObj.radius - 5
                    self.BallObj.angle += randint(-20, 20)
                    self.BallObj.updatevelo()

                self.Computer.update(self.BallObj.position[0], self.BallObj.position[1], self.setting[1])


            if self.BallObj.position[0] - self.BallObj.radius <= 0:
                self.rightscore += 1
                self.BallObj.update(startleft=False)

            elif self.BallObj.position[0] + self.BallObj.radius >= self.screenWidth:
                self.leftscore += 1
                self.BallObj.update(startleft=True)

            if self.rightscore >= 5:
                running = False

                textSettings = pygame.font.Font('freesansbold.ttf', 75)

                Text = textSettings.render("PLAYER ON THE RIGHT WINS", True, (255, 255, 255))
                TextRect = Text.get_rect()
                TextRect.x = self.screenWidth // 2 - (TextRect.width//2)
                TextRect.y = self.screenHeight // 2
                self.windowScreen.blit(Text, TextRect)

            if self.leftscore >= 5:
                running = False

                textSettings = pygame.font.Font('freesansbold.ttf', 75 )

                Text = textSettings.render("PLAYER ON THE LEFT WINS", True, (255, 255, 255))
                TextRect = Text.get_rect()
                TextRect.x = self.screenWidth // 2 - (TextRect.width//2)
                TextRect.y = self.screenHeight // 2
                self.windowScreen.blit(Text, TextRect)

            pygame.display.update()

            clock.tick(60)

        pygame.display.update()

        pygame.time.wait(5000)
        self.__init__()
        self.update()

    class Ball:
        def __init__(self, screenheight, screenwidth):
            self.screenheight = screenheight
            self.screenwidth = screenwidth

            self.angle = randint(-79, 79)
            self.position = [self.screenwidth // 2, self.screenheight // 2]
            self.radius = 10

            self.maxdist = 5
            self.vy = sin(self.angle * pi / 180) * self.maxdist
            self.vx = cos(self.angle * pi / 180) * self.maxdist

            self.frame = 0

        def updatevelo(self):
            if self.vy > 0:
                self.vy = sin(self.angle * pi / 180) * self.maxdist
            else:
                self.vy = -(sin(self.angle * pi / 180) * self.maxdist)

            if self.vx > 0:
                self.vx = cos(self.angle * pi / 180) * self.maxdist
            else:
                self.vx = -(cos(self.angle * pi / 180) * self.maxdist)

        def update(self, startleft=None):
            if self.frame % 300 == 0:
                self.maxdist += 1
                self.updatevelo()

            if startleft is None:
                if self.angle > 80:
                    self.angle = 70
                    self.updatevelo()
                elif self.angle < 10:
                    self.angle = 20
                    self.updatevelo()

                if self.position[0] + self.radius > self.screenwidth or self.position[0] - self.radius < 0:
                    self.vx = -self.vx

                if self.position[1] + self.radius > self.screenheight:
                    self.vy = -self.vy
                    self.position[1] = self.screenheight - self.radius

                if self.position[1] - self.radius < 0:
                    self.vy = -self.vy
                    self.position[1] = self.radius

                self.position[0] += int(self.vx)
                self.position[1] += int(self.vy)

                self.frame += 1

            elif startleft:
                self.angle = randint(-79, 79)
                self.position = [self.screenwidth // 2, self.screenheight // 2]

                self.vy = sin(self.angle * pi / 180) * self.maxdist
                self.vx = -(cos(self.angle * pi / 180) * self.maxdist)

                self.maxdist = 5
                self.updatevelo()

            elif not startleft:
                self.angle = randint(-79, 79)
                self.position = [self.screenwidth // 2, self.screenheight // 2]

                self.vy = sin(self.angle * pi / 180) * self.maxdist
                self.vx = cos(self.angle * pi / 180) * self.maxdist

                self.maxdist = 5
                self.updatevelo()

    class HumanPaddle:
        def __init__(self, screenheight, screenwidth, left=True, up=pygame.K_UP, down=pygame.K_DOWN):
            self.screenheight = screenheight
            self.screenwidth = screenwidth

            self.upkey = up
            self.downkey = down

            self.width = 10
            self.height = 70

            self.speed = 10

            self.frame = 0

            if left:
                self.position = [30, self.screenheight // 2 - self.height // 2, self.width, self.height]
            else:
                self.position = [self.screenwidth - self.width - 30, self.screenheight // 2 - self.height // 2, self.width, self.height]

        def update(self):
            InputKey = pygame.key.get_pressed()

            if InputKey[self.upkey] and self.position[1] >= 0:
                self.position[1] -= self.speed

            elif InputKey[self.downkey] and self.position[1] + self.position[3] <= self.screenheight:
                self.position[1] += self.speed

    class ComputerPaddle:
        def __init__(self, windowHeight, windowWidth):
            self.screenheight = windowHeight
            self.screenwidth = windowWidth

            self.width = 10
            self.height = 70

            self.speed = 10
            self.frame = 0

            self.position = [self.screenwidth - self.width - 30, self.screenheight // 2 - self.height // 2, self.width, self.height]

        def setspeed(self, speed):
            self.speed = speed

        def update(self, ballX, ballY, level):
            # level = {0: "EASY", 1: "MEDIUM", 2: "HARD", 3: "IMPOSSIBLE?"
            if level != "EASY":
                if level == "MEDIUM":
                    if self.frame % 1200 == 0:
                        self.speed += 1
                elif level == "HARD":
                    if self.frame % 600 == 0:
                        self.speed += 1

            if level == "IMPOSSIBLE?":
                self.position[1] = ballY

            if level != "IMPOSSIBLE?":
                if ballY > self.position[1]:
                    self.position[1] += self.speed
                else:
                    self.position[1] -= self.speed

            self.frame += 1


if __name__ == "__main__":
    Pong = PongHandler()
    Pong.update()