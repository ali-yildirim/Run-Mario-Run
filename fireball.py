import pygame
from sys import exit

pygame.init()


class Fireball(pygame.sprite.Sprite):

    counter = 0

    def __init__(self):
        super().__init__()

        fireball_frame_1 = pygame.image.load('Images/fireball/MFRemake_10 (4).png').convert_alpha()
        fireball_frame_2 = pygame.image.load('Images/fireball/MFRemake_10 (3).png').convert_alpha()
        fireball_frame_3 = pygame.image.load('Images/fireball/MFRemake_10 (2).png').convert_alpha()
        fireball_frame_4 = pygame.image.load('Images/fireball/MFRemake_10 (1).png').convert_alpha()

        self.fireball_frames = [fireball_frame_1, fireball_frame_2, fireball_frame_3, fireball_frame_4]

        self.fireball_index = 0

        self.image = self.fireball_frames[self.fireball_index]
        self.rect = self.image.get_rect(midbottom=(400, 200))

        self.gravity = 0

        Fireball.counter += 1

    def kill_itself(self):

        if self.rect.x < 100:

            del self

    def print_instances(self):

        print(Fireball.counter)

    def bounce(self):

        if self.rect.bottom == 300:
            self.gravity = -15

    def animation(self):

        self.fireball_index += 0.4
        if self.fireball_index >= len(self.fireball_frames):
            self.fireball_index = 0
        self.image = self.fireball_frames[int(self.fireball_index)]

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def keep_fireball_visible(self):

        if self.rect.x > 800:
            self.rect.x = 0

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def update(self):

        self.animation()
        self.rect.x += 2
        self.bounce()
        self.apply_gravity()
        self.keep_fireball_visible()
        self.kill_itself()


class Game:

    _window_width, _window_height = (800, 400)
    _window_size = (_window_width, _window_height)
    _black = (0, 0, 0)
    _screen = pygame.display.set_mode(_window_size)

    def __init__(self):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.fireball_list = []

    def delete_off_screen(self):

        for fireball in self.fireball_list:

            if fireball.rect.x < 100:

                del fireball

    def create_fireball(self):

        new_fireball = Fireball()
        self.fireball_list.append(new_fireball)

    def is_collide(self):

        for fireball in self.fireball_list:

            if pygame.Rect.colliderect(fireball.rect, fireball.rect):

                self.fireball_list.remove(fireball)

    def play(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.create_fireball()

            Game._screen.fill('black')
            self.delete_off_screen()

            for fireball in self.fireball_list:

                fireball.draw(Game._screen)
                fireball.update()
                print(len(self.fireball_list))

            pygame.display.update()
            self.clock.tick(60)


pygame.init()

game = Game()
game.play()

pygame.quit()
