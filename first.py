import pygame
from sys import exit
from random import randint,choice
import pickle

#File I/O

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('Project1\Graphics\player\player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Project1\Graphics\player\player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_jump = pygame.image.load('Project1\Graphics\player\jump.png').convert_alpha()
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom =(200,300))
        self.gravity=0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom ==300:
            self.gravity = -9
    def apply_gravity(self):
        self.gravity+=0.3
        self.rect.y+= self.gravity
        self.rect.left += 3
        if self.rect.bottom >=300:
            self.rect.bottom =300
    def update(self):
        if self.rect.right > 850: self.rect.left = -40
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.4
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = player_walk[int(self.player_index)]

    def resetgame(self):
        self.rect.midbottom = (200,300)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def displayscore():
    curr_time = pygame.time.get_ticks() - start_time
    global gscore
    gscore = int(curr_time/900)
    score_surf = test_font.render(f'{gscore}',False,(64,64,64))
    score_rect = score_surf.get_rect(center =(180,50))
    screen.blit(score_surf,score_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -=5
            if obstacle_rect.bottom ==300: screen.blit(snail_surface,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.4
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
        return 0

pygame.init()
width=800
height = 400
game_active = True
start_time= 0
snail_speed =4
screen= pygame.display.set_mode((width,height))
pygame.display.set_caption('FirstGame')
clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()


test_font=pygame.font.Font('Pixeltype.ttf',50)
game_score= pygame.font.Font('Pixeltype.ttf',50)
sky_surface = pygame.image.load('Project1\Graphics\Sky.png').convert()
gnd_surface = pygame.image.load('Project1\Graphics\ground.png').convert()
text_surface= test_font.render('FirstGame',False, 'Black')

#texts
score_surface = test_font.render('Score:',False, (64,64,64))
score_rect = score_surface.get_rect(center = (100,50))
hscore_surface = test_font.render('High Score:',False, (64,64,64))
hscore_rect =  score_surface.get_rect(center = (600,50))

welcome_surface = test_font.render('Welcome',False, (139,207,186))
welcome_surface_scaled=pygame.transform.scale2x(welcome_surface)
welcome_rect = welcome_surface_scaled.get_rect(center = (400,50))

space_surface = test_font.render('Press Space to Continue',False, (139,207,186))
space_surface_scaled=pygame.transform.scale2x(space_surface)
space_rect = space_surface_scaled.get_rect(center = (400,340))

score_surface = test_font.render('Score:',False, (64,64,64))
score_rect = score_surface.get_rect(center = (100,50))

#obstacles
snail_frame1 = pygame.image.load('Project1/graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('Project1/graphics/snail/snail2.png').convert_alpha()
snail_frames= [snail_frame1,snail_frame2]
snail_index = 0
snail_surface= snail_frames[snail_index]

fly_frame1 = pygame.image.load('Project1\graphics\Fly\Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('Project1\graphics\Fly\Fly2.png').convert_alpha()
fly_frames = [fly_frame1,fly_frame2]
fly_index = 0
fly_surf = fly_frames[fly_index]

obstacles_list = []


#intro screen
player_stand = pygame.image.load('Project1/graphics/Player/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand_scaled.get_rect(center=(400,200))
player_gravity = 0

#player
player_walk1 = pygame.image.load('Project1\Graphics\player\player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('Project1\Graphics\player\player_walk_2.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_jump = pygame.image.load('Project1\Graphics\player\jump.png').convert_alpha()
player_index = 0

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,250))
#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1400)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,500)

fly_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_timer,400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if (event.type == pygame.MOUSEBUTTONDOWN ):
                player_gravity = -9
            # if event.type == pygame.MOUSEMOTION:
            #     # print(event.pos)
            #     if player_rect.collidepoint(event.pos): print ('col')
            if (event.type == pygame.KEYDOWN and player_rect.bottom == 300):
                if event.key == pygame.K_SPACE:
                    player_gravity=-10
            if event.type == obstacle_timer:
                if randint(0,1):
                    obstacles_list.append(snail_surface.get_rect(midbottom = (randint(1000,1200),300)))
                else:
                    obstacles_list.append(fly_surf.get_rect(midbottom=(randint(1000, 1200), 100)))
            if event.type ==snail_timer:
                if snail_index ==0 : snail_index =1
                else: snail_index = 0
                snail_surface = snail_frames[snail_index]
            if event.type ==fly_timer:
                if fly_index ==0 : fly_index =1
                else: fly_index = 0
                fly_surf = fly_frames[fly_index]

        else:
            if (event.type ==pygame.KEYDOWN and event.key == pygame.K_SPACE):
                game_active= True
                player_rect.left=0
    if game_active:
        #print(pickle.load(open("highscore.dat","rb")))

        screen.blit(sky_surface,(0,0))
        screen.blit(gnd_surface,(0,300))
        screen.blit(text_surface,(320,30))
        displayscore()
        #pygame.draw.rect(screen,'#c0e8ec',score_rect)
        #pygame.draw.line(screen,'Red',(0,0),pygame.mouse.get_pos(),1)

        #display score and highscore
        screen.blit(score_surface,score_rect)
        screen.blit(hscore_surface, hscore_rect)

        hscore_s = test_font.render(f'{pickle.load(open("highscore.dat","rb"))}', False, (64, 64, 64))
        hscore_r = hscore_s.get_rect(center=(740, 50))
        screen.blit(hscore_s, hscore_r)
        # snail_rect.x-=snail_speed
        # screen.blit(snail_surface,snail_rect)
        # if snail_rect.right < 0: snail_rect.left = 800

        player_gravity+=0.3
        player_rect.bottom+=player_gravity
        player_rect.left +=3

        #obs movement
        obstacles_list = obstacle_movement(obstacles_list)

        if player_rect.bottom >= 300: player_rect.bottom =300
        #print(player_rect.left)
        if player_rect.right > 850: player_rect.left = -40

        # if abs(player_rect.centerx - snail_rect.centerx) < 4  : print('i made it work but dont know what to do')
        player_animation()
        screen.blit(player_surface,player_rect)

        # player.draw(screen)
        # player.update()
        # obstacle_group.draw(screen)
        # obstacle_group.update()

        #collisions
        game_active = collisions(player_rect, obstacles_list)
    else:
        highscore = gscore
        if(highscore>pickle.load(open("highscore.dat","rb"))):
            pickle.dump(gscore,open("highscore.dat","wb"))
        screen.fill((94,109,162))
        start_time = pygame.time.get_ticks()
        screen.blit(player_stand_scaled,player_stand_rect)
        screen.blit(welcome_surface_scaled,welcome_rect)
        screen.blit(space_surface_scaled, space_rect)
        #reset
        obstacles_list.clear()
        player_rect.midbottom=(80,300)
        player_gravity = 0
        player.update()

    pygame.display.update()
    clock.tick(60)