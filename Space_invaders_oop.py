from hmac import new
import pygame
import random
import math
from pygame import mixer

class Player:
    def __init__(self):
        self.playerImage = pygame.image.load('data/spaceship.png')
        self.player_X = 370
        self.player_Y = 523
        self.player_Xchange = 0

        self.bulletImage = pygame.image.load('data/bullet.png')
        self.bullet_X = 0
        self.bullet_Y = 500
        self.bullet_Xchange = 0
        self.bullet_Ychange = 100
        self.bullet_state = "rest"
        self.bullet_sound = None

class Invader:
    def __init__(self):
        self.invaderImage = []
        self.invader_X = []
        self.invader_Y = []
        self.invader_Xchange = []
        self.invader_Ychange = []
        self.no_of_invaders = 5
        self.player = Player()

        for num in range(self.no_of_invaders):
            self.invaderImage.append(pygame.image.load('data/alien.png'))
            self.invader_X.append(random.randint(64, 737))
            self.invader_Y.append(random.randint(30, 180))
            #velocidade vertical do invader
            self.invader_Xchange.append(0.2)
            #velocidade horizontal do invader
            self.invader_Ychange.append(10)


class Game:
    def __init__(self):
        # initializing pygame
        pygame.init()
        self.createScreen()
        self.playerInstance = Player()
        self.invaderInstance = Invader()
        self.needRun = True
        self.phase = 0
        self.background_image = "data/bg_1.png"
        self.runGame()

    def setPhase(self, phase):
        if phase == 0:
            print("Faz nada")
        elif phase == 1:
            self.background_image = "data/bg_2.png"
        elif phase == 2:
            print("Fase 3")
            self.background_image = "data/bg_3.png"
        elif phase == 3:
            print("Fase 4")
            self.background_image = "data/bg_4.png"
        elif phase == 4:
            print("Parabéns, você salvou a galáxia Anima")

    def createScreen(self):
        # creating screen
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # caption and icon
        pygame.display.set_caption("UNIBH Space Invaders")

        # Score
        self.score_val = 0
        self.scoreX = 5
        self.scoreY = 5
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        # Background Sound
        mixer.music.load('data/background.wav')
        mixer.music.play()

        # Game Over
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)

    def show_score(self, x, y):
        self.score = self.font.render("Points: " + str(self.score_val), True, (255, 255, 255))
        self.screen.blit(self.score, (x, y))

    def game_over(self):
        self.game_over_text = self.game_over_font.render("GAME OVER", True, (255, 255, 255)) 
        self.screen.blit(self.game_over_text, (190, 250))

    def win_game(self):
        self.invaderInstance.no_of_invaders = 0
        mixer.music.stop()
        self.win_text_font = pygame.font.Font('freesansbold.ttf', 32)
        self.win_text = self.win_text_font.render("Parabéns, você salvou a galáxia Anima", True, (255, 255, 255)) 
        self.screen.blit(self.win_text, (100, 250))
        self.playerInstance.player_X = 1000
        self.playerInstance.player_Y = 1000
        self.playerInstance.bullet_state = "rest"
        
    def isCollision(self, x1, x2, y1, y2):
        self.distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
        if self.distance <= 50:
            return True
        else:
            return False

    def player(self, x, y):
        self.screen.blit(self.playerInstance.playerImage, (x - 16, y + 10))

    def invader(self, x, y, i):
        self.screen.blit(self.invaderInstance.invaderImage[i], (x, y))

    def bullet(self, x, y):
        self.screen.blit(self.playerInstance.bulletImage, (x, y))
        self.playerInstance.bullet_state = "fire"

    def runGame(self):
        self.running = True
        self.clock = pygame.time.Clock()
        while self.running:
            self.clock.tick(150)
            
            # RGB
            self.screen.fill((0, 0, 0))

            bg = pygame.image.load(self.background_image).convert()
            #INSIDE OF THE GAME LOOP
            self.screen.blit(bg, (0, 0))
            
            if self.score_val <= 25: 
                self.setPhase(0)
            
            if self.score_val >= 26 and self.score_val <= 80:
                self.setPhase(1)
                self.bg = "data/bg_2.png"
                self.invaderImage.append(pygame.image.load('data/alien1.png'))
            
            if self.score_val >= 81 and self.score_val <= 150:
                self.setPhase(2)
                self.bg = "data/bg_3.png"
            
            if self.score_val >= 151 and self.score_val <= 199:
                self.setPhase(3)
                self.bg = "data/bg_4.png"


            elif self.score_val >= 200 :
                self.phase = 4
                self.setPhase(1)
                self.win_game()

            
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Controlling the player movement
                # from the arrow keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.playerInstance.player_Xchange = -1.7

                    if event.key == pygame.K_RIGHT:
                        self.playerInstance.player_Xchange = 1.7

                    if event.key == pygame.K_SPACE:

                        # Fixing the change of direction of bullet
                        if self.playerInstance.bullet_state == "rest" and self.phase != 5:
                            self.playerInstance.bullet_X = self.playerInstance.player_X
                            self.bullet(self.playerInstance.bullet_X, self.playerInstance.bullet_Y)
                            self.playerInstance.bullet_sound = mixer.Sound('data/bullet.wav')
                            self.playerInstance.bullet_sound.play()
                if event.type == pygame.KEYUP:
                    self.playerInstance.player_Xchange = 0

            # adding the change in the player position
            self.playerInstance.player_X += self.playerInstance.player_Xchange
            for i in range(self.invaderInstance.no_of_invaders):
                self.invaderInstance.invader_X[i] += self.invaderInstance.invader_Xchange[i]

            # bullet movement
            if self.playerInstance.bullet_Y <= 0:
                self.playerInstance.bullet_Y = 600
                self.playerInstance.bullet_state = "rest"
            if self.playerInstance.bullet_state == "fire":
                self.bullet(self.playerInstance.bullet_X, self.playerInstance.bullet_Y)
                self.playerInstance.bullet_Y -= self.playerInstance.bullet_Ychange

            # movement of the invader
            for i in range(self.invaderInstance.no_of_invaders):

                if self.invaderInstance.invader_Y[i] >= 450:
                    if abs(self.playerInstance.player_X - self.invaderInstance.invader_X[i]) < 80:
                        for j in range(self.invaderInstance.no_of_invaders):
                            self.invaderInstance.invader_Y[j] = 2000
                            self.explosion_sound = mixer.Sound('data/explosion.wav')
                            self.explosion_sound.play()
                        self.game_over()
                        break

                if self.invaderInstance.invader_X[i] >= 735 or self.invaderInstance.invader_X[i] <= 0:
                    self.invaderInstance.invader_Xchange[i] *= -1
                    self.invaderInstance.invader_Y[i] += self.invaderInstance.invader_Ychange[i]
                # Collision
                self.collision = self.isCollision(self.playerInstance.bullet_X, self.invaderInstance.invader_X[i],
                                        self.playerInstance.bullet_Y, self.invaderInstance.invader_Y[i])
                if self.collision:
                    self.score_val += 10
                    self.playerInstance.bullet_Y = 600
                    self.playerInstance.bullet_state = "rest"
                    self.invaderInstance.invader_X[i] = random.randint(64, 736)
                    self.invaderInstance.invader_Y[i] = random.randint(30, 200)
                    self.invaderInstance.invader_Xchange[i] *= -1

                self.invader(self.invaderInstance.invader_X[i], self.invaderInstance.invader_Y[i], self.phase)

            # restricting the spaceship so that
            # it doesn't go out of screen
            if self.playerInstance.player_X <= 16:
                self.playerInstance.player_X = 16;
            elif self.playerInstance.player_X >= 750:
                self.playerInstance.player_X = 750



            self.player(self.playerInstance.player_X, self.playerInstance.player_Y)
            self.show_score(self.scoreX, self.scoreY)
            pygame.display.update()

Game()