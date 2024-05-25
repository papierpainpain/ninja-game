import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Ninja game")
        self.screen = pygame.display.set_mode((640, 480))
        
        self.clock = pygame.time.Clock()

        self.images = pygame.image.load("data/images/clouds/cloud_1.png")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60) # 60 FPS


if __name__ == "__main__":
    Game().run()
