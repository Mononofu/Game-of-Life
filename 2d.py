import os, random, time
import pygame, pygame.image, pygame.key, pygame.draw
from pygame.locals import *
import cProfile

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

    def apply_future(self, surf, (x, y)):
        if ( self.alive != self.future_state ) or ( not self.alive and self.time_since_death < fade_time ):
            self.alive = self.future_state
            self.draw(surf, x, y)
        else:
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
            
            surface.set_at((x,y), c )

    def die(self):
        self.future_state = False
        if self.alive:
            self.time_since_death = 0

    def live(self):
        self.future_state = True

    def set_state(self, state):
        if state:
            self.live()
        else:
            self.die()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.board = {}
        random.seed(time.time())

        self.gen = 0

    def run(self):
        counter = 0
        while 1:
            if counter > 10:
                return
            start = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self.step()
            time_used = time.time() - start
            print "%f s or %f FPS" % (time_used, 1/time_used)
            counter += 1

    def set_cell(self, pos, state):
        if pos not in self.board:
            self.board[pos] = Cell()

        self.board[pos].set_state(state)

    def random_seed(self):
        choices = [False, True, False]
        
        for i in range(board_width):
            self.set_cell( (i,0), random.choice(choices) )
            self.set_cell( (i,board_height-1), random.choice(choices) )
  
        for i in range(board_height):
            self.set_cell( (0,i), random.choice(choices) )
            self.set_cell( (board_width-1,i), random.choice(choices) )

    def step(self):
        self.screen.fill(black)

        self.screen.lock()

        for pos, cell in self.board.iteritems():
            cell.apply_future(self.screen, pos)

        self.screen.unlock()


        for pos, cell in self.board.iteritems():
            sum = 0

            neighbors = [ (pos[0]-1,pos[1]),
                          (pos[0]-1,pos[1]-1),
                          (pos[0],pos[1]-1),
                          ((pos[0]+1) % board_width,pos[1]-1),
                          ((pos[0]+1) % board_width,pos[1]),
                          ((pos[0]+1) % board_width,(pos[1]+1) % board_height),
                          (pos[0],(pos[1]+1) % board_height),
                          (pos[0]-1,(pos[1]+1) % board_height) ]

            for n in neighbors:
                if n in self.board and self.board[n].alive:
                    sum += 1

            if cell.alive:
                sum -= 1

            if sum >= R[0] and sum <= R[1]:
                cell.live()
            if sum > R[2] or sum < R[3]:
                cell.die()

        

        self.random_seed()
        pygame.display.flip()

        pygame.image.save(self.screen, "life%000d.png" % self.gen)
        self.gen += 1

            



if __name__ == '__main__':
    game = Game()
    cProfile.run('game.run()', 'gol_prof')
    #game.run()
