import pygame
from sys import exit
import random


class Player(pygame.sprite.Sprite):

    _player_walk_1 = pygame.image.load('Images/mario_still.png')
    _player_walk_2 = pygame.image.load('Images/mario_moving.png')
    _player_jump = pygame.image.load('Images/mario_still.png')

    def __init__(self):

        super().__init__()

        self.player_frame = [Player._player_walk_1, Player._player_walk_2]
        self.player_index = 0

        self.image = self.player_frame[self.player_index]
        self.rect = self.image.get_rect(midbottom=(258, 630))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Images/Mario-jump-sound.mp3')
        self.jump_sound.set_volume(0.05)
        self.xpos = 630

    def player_input(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.xpos:
            self.gravity = -22
            self.jump_sound.play()

    def jump(self):

        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.xpos:
            self.rect.bottom = self.xpos

    def animate(self):
        if self.rect.bottom < self.xpos:
            self.image = Player._player_jump
        else:
            self.player_index += 0.10
            if self.player_index >= len(self.player_frame):
                self.player_index = 0
            self.image = self.player_frame[int(self.player_index)]

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def reset_position(self):

        self.rect = self.image.get_rect(midbottom=(258, 630))

    def update(self):

        self.player_input()
        self.jump()
        self.animate()


class Ball(pygame.sprite.Sprite):

    _frame_1 = pygame.image.load('Images/fireball/MFRemake_10 (4).png')
    _frame_2 = pygame.image.load('Images/fireball/MFRemake_10 (3).png')
    _frame_3 = pygame.image.load('Images/fireball/MFRemake_10 (2).png')
    _frame_4 = pygame.image.load('Images/fireball/MFRemake_10 (1).png')

    def __init__(self):
        super().__init__()

        self.frames = [Ball._frame_1, Ball._frame_2, Ball._frame_3, Ball._frame_4]
        self.ball_index = 0
        self.image = self.frames[self.ball_index]
        self.gravity = 0
        self.damage = 0
        self.position = None

    def bounce(self):

        if self.rect.bottom == 630:
            self.gravity = -15

    def animate(self):

        self.ball_index += 0.4
        if self.ball_index >= len(self.frames):
            self.ball_index = 0
        self.image = self.frames[int(self.ball_index)]

    def apply_gravity(self):

        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 630:
            self.rect.bottom = 630

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def update(self):

        self.animate()
        self.rect.x += 2
        self.bounce()
        self.apply_gravity()


class Fireball(Ball):

    _fireball_frame_1 = pygame.image.load('Images/fireball/MFRemake_10 (4).png')
    _fireball_frame_2 = pygame.image.load('Images/fireball/MFRemake_10 (3).png')
    _fireball_frame_3 = pygame.image.load('Images/fireball/MFRemake_10 (2).png')
    _fireball_frame_4 = pygame.image.load('Images/fireball/MFRemake_10 (1).png')

    def __init__(self, position):
        super().__init__()

        self.frames = [Fireball._fireball_frame_1, Fireball._fireball_frame_2,
                       Fireball._fireball_frame_3, Fireball._fireball_frame_4]
        self.damage = 1
        self.position = position
        self.rect = self.image.get_rect(midleft=position)


class Iceball(Ball):

    _iceball_frame_1 = pygame.image.load('Images/iceball/1.png')
    _iceball_frame_2 = pygame.image.load('Images/iceball/2.png')
    _iceball_frame_3 = pygame.image.load('Images/iceball/3.png')
    _iceball_frame_4 = pygame.image.load('Images/iceball/4.png')

    def __init__(self, position):
        super().__init__()

        self.frames = [Iceball._iceball_frame_1, Iceball._iceball_frame_2,
                       Iceball._iceball_frame_3, Iceball._iceball_frame_4]

        self.position = position
        self.rect = self.image.get_rect(midleft=position)
        self.damage = 2

    def bounce(self):

        if self.rect.bottom == 630:
            self.gravity = -15


class Enemy(pygame.sprite.Sprite):

    _dummy_frame_1 = pygame.image.load('Images/frame_2_delay-0.2s.png')
    _dummy_frame_2 = pygame.image.load('Images/frame_2_delay-0.2s.png')

    def __init__(self):
        super().__init__()

        self.frames = [Enemy._dummy_frame_1, Enemy._dummy_frame_2]
        self.y_pos = 632
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(0, 0))
        self.speed = 0

    def animate(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def move(self):

        self.rect.x -= self.speed

    def collide(self, list_1, list_2):

        pass

    def update(self):

        self.animate()
        self.move()


class Coin(pygame.sprite.Sprite):

    _coin_0 = pygame.image.load('Images/gold/0.png')
    _coin_1 = pygame.image.load('Images/gold/1.png')
    _coin_2 = pygame.image.load('Images/gold/2.png')
    _coin_3 = pygame.image.load('Images/gold/3.png')

    def __init__(self):
        super().__init__()

        self.coin_frames = [Coin._coin_0, Coin._coin_1, Coin._coin_2, Coin._coin_3]
        self.coin_index = 0
        self.y_pos = 532
        self.image = self.coin_frames[self.coin_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(1300, 1800), self.y_pos))
        self.collecting_coin = pygame.mixer.Sound('Images/Mario-coin-sound.mp3')
        self.collecting_coin.set_volume(0.5)

    def animate(self):

        self.coin_index += 0.3
        if self.coin_index >= len(self.coin_frames):
            self.coin_index = 0
        self.image = self.coin_frames[int(self.coin_index)]

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def update(self):

        self.animate()
        self.rect.x -= 6


class Koopa(Enemy):

    _koopa_1 = pygame.image.load('Images/koopa_0.png')
    _koopa_2 = pygame.image.load('Images/koopa_1.png')

    def __init__(self):
        super().__init__()

        self.frames = [Koopa._koopa_1, Koopa._koopa_2]
        self.y_pos = 655
        self.rect = self.image.get_rect(midbottom=(random.randint(1280, 1450), self.y_pos))
        self.speed = 5
        self.health = 2

    def collide(self, list_fireball, list_iceball):

        for fireball in list_fireball:

            if pygame.sprite.collide_rect(fireball, self):

                list_fireball.remove(fireball)
                self.health -= fireball.damage

        for iceball in list_iceball:

            if pygame.sprite.collide_rect(iceball, self):

                list_iceball.remove(iceball)
                self.health -= iceball.damage

    def die(self, list_koopa):

        koopas = list_koopa

        if self.health <= 0:

            koopas.remove(self)


class Goomba(Enemy):

    _goomba_1 = pygame.image.load('Images/goomba_0.png')
    _goomba_2 = pygame.image.load('Images/goomba_1.png')

    def __init__(self):
        super().__init__()

        self.frames = [Goomba._goomba_1, Goomba._goomba_2]
        self.y_pos = 670
        self.rect = self.image.get_rect(midbottom=(random.randint(1280, 1450), self.y_pos))
        self.speed = 5.5

    def collide(self, list_fireball, list_goomba):

        goombas = list_goomba
        for fireball in list_fireball:

            if pygame.sprite.collide_rect(fireball, self):

                list_fireball.remove(fireball)
                goombas.remove(self)


class BackGroundItems(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.y_pos = 632
        self.image = pygame.image.load('Images/tree_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(1280, self.y_pos))
        self.speed = 3

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def update(self):

        self.rect.x -= self.speed


class Tree(BackGroundItems):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('Images/tree_1.png').convert_alpha()
        self.y_pos = 628
        self.rect = self.image.get_rect(midbottom=(1300, self.y_pos))


class Fence(BackGroundItems):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('Images/fence_1.png').convert_alpha()
        self.y_pos = 628
        self.rect = self.image.get_rect(midbottom=(1485, self.y_pos))


class Cloud(BackGroundItems):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('Images/cloud_1.png').convert_alpha()
        self.y_pos = random.choice((150, 212, 275))
        self.rect = self.image.get_rect(midbottom=(1350, self.y_pos))


class Game:

    # screen and its properties
    _window_width, _window_height = (1280, 720)
    _window_size = (_window_width, _window_height)
    _black = (0, 0, 0)
    _screen = pygame.display.set_mode(_window_size)

    def __init__(self):

        # game name, game icon and the font
        pygame.display.set_caption('Run Mario Run')
        self.pygame_icon = pygame.image.load('Images/Mario.png')
        pygame.display.set_icon(self.pygame_icon)
        self.test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

        # some variables of the game
        self.game_active = False
        self.start_time = 0
        self.score = 0
        self.counter = 0
        self._clock = pygame.time.Clock()
        self.coin_sound = pygame.mixer.Sound('Images/Mario-coin-sound.mp3')

        # player instance
        self.player = Player()

        # lists of the assets
        self.fireball_list = []
        self.iceball_list = []
        self.tree_list = []
        self.fence_list = []
        self.cloud_list = []
        self.goombas_list = []
        self.koopas_list = []
        self.coin_list = []

        # uploading the background image
        self.background = pygame.image.load('Images/background.jpg').convert()

        # Intro screen
        self.game_cover = pygame.image.load('Images/mario_cover.png').convert_alpha()
        self.game_cover = pygame.transform.rotozoom(self.game_cover, 0, 2)
        self.game_cover_rect = self.game_cover.get_rect(center=(640, 360))

        self.game_name = self.test_font.render('Run Mario Run', True, 'Black')
        self.game_name_rect = self.game_name.get_rect(center=(400, 80))

        self.game_message = self.test_font.render('Press space to run!', True, 'Black')
        self.game_message_rect = self.game_message.get_rect(center=(640, 580))

        # Game Over Screen
        self.score_message = self.test_font.render(f'Your score: {self.score}', True, 'Black')
        self.score_message_rect = self.score_message.get_rect(center=(630, 150))
        self.death_message = self.test_font.render('Game Over! Press space to restart!', True, 'Black')
        self.death_message_rect = self.score_message.get_rect(center=(490, 550))

        # Timer
        self.goomba_timer = pygame.USEREVENT + 2
        self.koopa_timer = pygame.USEREVENT + 3
        self.coin_timer = pygame.USEREVENT + 3
        self.background_timer = pygame.USEREVENT + 1

        pygame.time.set_timer(self.goomba_timer, 2200)
        pygame.time.set_timer(self.koopa_timer, 2350)
        pygame.time.set_timer(self.coin_timer, 1800)
        pygame.time.set_timer(self.background_timer, 2000)

    def draw_basics(self):

        Game._screen.blit(self.background, (0, 0))
        self.score = self.display_score()
        self.display_coin_number()

    def bring_score_screen(self):

        self.score_message = self.test_font.render(f'Your score: {self.score}', True, 'Black')
        Game._screen.blit(self.death_message, self.death_message_rect)
        Game._screen.blit(self.score_message, self.score_message_rect)

    def bring_game_over_screen(self):

        Game._screen.fill('Red')
        Game._screen.blit(self.game_cover, self.game_cover_rect)
        self.counter = 0
        self.player.reset_position()

    def create_fireball(self):

        position = self.player.rect.midright
        new_fireball = Fireball((position[0], position[1] + 2))
        self.fireball_list.append(new_fireball)

    def create_iceball(self):

        position = self.player.rect.midright
        new_iceball = Iceball((position[0], position[1] + 2))
        self.iceball_list.append(new_iceball)

    def create_background(self):

        new_tree = Tree()
        self.tree_list.append(new_tree)
        new_fence = Fence()
        self.fence_list.append(new_fence)
        new_cloud = Cloud()
        self.cloud_list.append(new_cloud)

    def create_goomba(self):

        new_goomba = Goomba()
        self.goombas_list.append(new_goomba)

    def create_koopa(self):

        new_koopa = Koopa()
        self.koopas_list.append(new_koopa)

    def create_coin(self):

        new_coin_1 = Coin()
        new_coin_2 = Coin()
        new_coin_3 = Coin()
        new_coin_4 = Coin()
        coins = [new_coin_1, new_coin_2, new_coin_3, new_coin_4]

        for c in coins:
            self.coin_list.append(c)

    def display_coin_number(self):

        coin_display = self.test_font.render(f'Coins: {self.counter}', False, 'White')
        coin_number_rect = coin_display.get_rect(center=(880, 50))
        Game._screen.blit(coin_display, coin_number_rect)

    def display_score(self):

        current_time = int(pygame.time.get_ticks() / 100) - self.start_time
        score_game = self.test_font.render(f'Score: {current_time}', False, 'White')
        score_rect = score_game.get_rect(center=(400, 50))
        Game._screen.blit(score_game, score_rect)
        return current_time

    def game_over_collision(self):

        for goomba in self.goombas_list:

            if pygame.sprite.collide_rect(self.player, goomba):

                self.game_active = 0
                self.goombas_list.clear()
                self.koopas_list.clear()
                self.coin_list.clear()
                self.tree_list.clear()
                self.fence_list.clear()
                self.cloud_list.clear()
                self.fireball_list.clear()
                self.iceball_list.clear()

        for koopa in self.koopas_list:

            if pygame.sprite.collide_rect(self.player, koopa):

                self.game_active = 0
                self.goombas_list.clear()
                self.koopas_list.clear()
                self.coin_list.clear()
                self.tree_list.clear()
                self.fence_list.clear()
                self.cloud_list.clear()
                self.fireball_list.clear()
                self.iceball_list.clear()

    def coin_collect(self):

        for coin in self.coin_list:

            if pygame.sprite.collide_rect(self.player, coin):

                self.coin_list.remove(coin)
                self.counter += 1
                self.coin_sound.set_volume(0.05)
                self.coin_sound.play()

    def delete_off_screen(self):

        for goomba in self.goombas_list:

            if goomba.rect.midleft[0] < -2:

                self.goombas_list.remove(goomba)

        for koopa in self.koopas_list:

            if koopa.rect.midleft[0] < -2:

                self.koopas_list.remove(koopa)

    def play(self):

        while True:

            # draw all our elements
            # update everything
            # looping through all the events

            for event in pygame.event.get():

                # click X to close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # press escape to end the game and go to the menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        self.game_active = 0
                        self.goombas_list.clear()
                        self.koopas_list.clear()
                        self.coin_list.clear()
                        self.tree_list.clear()
                        self.fence_list.clear()
                        self.cloud_list.clear()
                        self.fireball_list.clear()
                        self.iceball_list.clear()

                if self.game_active:

                    # create instances of background items
                    if event.type == self.background_timer:

                        self.create_background()

                    # create instances of enemies
                    if event.type == self.goomba_timer:

                        self.create_goomba()

                    if event.type == self.koopa_timer:

                        self.create_koopa()

                    # create instances of coins (4 at a time)
                    if event.type == self.coin_timer:

                        self.create_coin()

                    # Takes player input to create instances of fireball. It costs 5 coins to throw a fireball.
                    # Player can't throw a fireball if coin number < 5.
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:

                            if not self.counter < 3:

                                self.counter -= 3
                                self.create_fireball()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_o:

                            if not self.counter < 3:

                                self.counter -= 3
                                self.create_iceball()

                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:

                            pygame.time.delay(300)
                            self.game_active = True
                            self.start_time = int(pygame.time.get_ticks() / 100)

            if self.game_active:

                # draw the background, display score and the coin number
                self.draw_basics()

                # enrich the background
                for tree in self.tree_list:

                    tree.draw(Game._screen)
                    tree.update()

                for fence in self.fence_list:

                    fence.draw(Game._screen)
                    fence.update()

                for cloud in self.cloud_list:

                    cloud.draw(Game._screen)
                    cloud.update()

                # draw the coins
                for coin in self.coin_list:

                    coin.draw(Game._screen)
                    coin.update()

                # draw the Player
                self.player.draw(Game._screen)
                self.player.update()

                # Game Over if player collides with an enemy
                self.game_over_collision()

                # draw the fireball(s) or iceball(s)
                for fireball in self.fireball_list:

                    fireball.draw(Game._screen)
                    fireball.update()

                for iceball in self.iceball_list:

                    iceball.draw(Game._screen)
                    iceball.update()

                # draw the enemies
                for goomba in self.goombas_list:

                    goomba.draw(Game._screen)
                    goomba.collide(self.fireball_list, self.goombas_list)
                    goomba.update()

                for koopa in self.koopas_list:

                    koopa.draw(Game._screen)
                    koopa.collide(self.fireball_list, self.iceball_list)
                    koopa.die(self.koopas_list)
                    koopa.update()

                # collect coin, give coin-collecting sound and update self.count = number of coins collected
                self.coin_collect()

                # items off-screen will be removed from the list
                self.delete_off_screen()

            else:

                # bring the Game Over screen.

                self.bring_game_over_screen()

                if self.score == 0:
                    Game._screen.blit(self.game_message, self.game_message_rect)
                else:

                    self.bring_score_screen()

            pygame.display.update()
            self._clock.tick(60)


if __name__ == '__main__':

    pygame.init()

    game = Game()
    game.play()

    pygame.quit()
