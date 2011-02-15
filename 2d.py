import os, random, time
import pygame, pygame.image, pygame.key
from pygame.locals import *

generations_per_second = 3
fade_time = 15.0
size = width, height = 1280, 720
black = (0,0,0)
blit_size = 1
board_width = width
board_height = height

# a new cell will appear if the number of neighbors (Sum)
# is equal or more than r[0] and equal or less than r[1]
# a cell will die if the Sum is more than r[2] or less than r[3]
R = (3, 3, 3, 2)

class Cell:
    def __init__(self, alive = False):
        self.alive = alive
        self.future_state = alive
        self.time_since_death = fade_time

    def apply_future(self):
        self.alive = self.future_state
        if not self.alive:
            self.time_since_death += 1

    def draw(self, surface, x, y):
        if self.alive:
            surface.fill((255, 255, 255), pygame.Rect(x*blit_size, y*blit_size, blit_size, blit_size) )
        else:
            saturation = 200 * self.time_since_death/fade_time
            if saturation > 100:
                saturation = 100

            value = (1.5 * fade_time - self.time_since_death)/fade_time * 100

            if value < 0:
                value = 0

            if value > 100:
                value = 100

            c = Color(0,0,0,0)
            c.hsva = (195, saturation, value, 100)
            
            surface.fill(c, pygame.Rect(x*blit_size, y*blit_size, blit_size, blit_size) )

    def die(self):
        self.future_state = False
        if self.alive:
            self.time_since_death = 0

    def live(self):
        self.future_state = True


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.board = [ [Cell() for _ in range(board_height)] for _ in range(board_width)]
        random.seed(time.time())

        self.gen = 0

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self.step()
            time.sleep(0.01)

    def random_seed(self):
        choices = [False, True, False]
        
        for i in range(board_width):
            if random.choice(choices):
                self.board[i][0].live()
            else:
                self.board[i][0].die()
                
            if random.choice(choices):
                self.board[i][board_height-1].live()
            else:
                self.board[i][board_height-1].die()

        
        for i in range(board_height):       
            if random.choice(choices):
                self.board[0][i].live()
            else:
                self.board[0][i].die()
                
            if random.choice(choices):
                self.board[board_width-1][i].live()
            else:
                self.board[board_width-1][i].die()


    def step(self):
        self.screen.fill(black)

        for i in range(board_width):
            #print " "
            for j in range(board_height):
                self.board[i][j].apply_future()
                self.board[i][j].draw(self.screen, i, j)

                #if self.board[i][j].alive:
                #    print "x",
                #else:
                #    print "0",

        for i in range(board_width):
            for j in range(board_height):

                sum = 0

                for x in [i-1, i, (i+1) % board_width]:
                    for y in [j-1, j, (j+1) % board_height]:
                        if self.board[x][y].alive:
                            sum += 1

                if self.board[i][j].alive:
                    sum -= 1

                if sum >= R[0] and sum <= R[1]:
                    self.board[i][j].live()
                if sum > R[2] or sum < R[3]:
                    self.board[i][j].die()

        

        self.random_seed()
        pygame.display.flip()

        pygame.image.save(self.screen, "life%000d.png" % self.gen)
        self.gen += 1

            



if __name__ == '__main__':
    game = Game()
    game.run()
