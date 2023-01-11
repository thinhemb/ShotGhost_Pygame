import pygame

from world import World, load_level
from player import Player
from enemies import Ghost
from projectiles import Bullet, Grenade
from button import Button
from texts import Text, Message, BlinkingText, MessageBox
import time

pygame.init()







WIDTH, HEIGHT = 640, 384
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
TILE_SIZE = 16
Full_Sound = 0.2
score = 0
clock = pygame.time.Clock()
FPS = 60

# IMAGES **********************************************************************

BG1 = pygame.transform.scale(pygame.image.load('assets/BG1.png'), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load('assets/BG2.png'), (WIDTH, HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load('assets/BG3.png'), (WIDTH, HEIGHT))
MOON = pygame.transform.scale(pygame.image.load('assets/moon.png'), (300, 220))

# FONTS ***********************************************************************

title_font = "Fonts/NotoSerif-Regular.ttf"
instructions_font = 'Fonts/NotoSerif-Regular.ttf'
winner_font = "Fonts/Bungee-Regular.ttf"


ghostbusters = Message(WIDTH//2 + 5, HEIGHT//2 - 90, 50, "Ghost Shot", winner_font, (255, 255, 255), win)
left_key = Message(WIDTH//2 + 30, HEIGHT//2 - 120, 16, "Nhấn mũi tên trái hoặc A để đi sang trái", instructions_font, (255, 255, 255), win)
right_key = Message(WIDTH//2 + 30, HEIGHT//2 - 90, 16, "Nhấn mũi tên phải hoặc D để đi sang phải", instructions_font, (255, 255, 255), win)
up_key = Message(WIDTH//2 + 30, HEIGHT//2 - 60, 16, "Nhấn mũi tên lên hoặc W để nhảy", instructions_font, (255, 255, 255), win)
space_key = Message(WIDTH//2 + 30, HEIGHT//2 - 30, 16, "Nhấn space để bắn", instructions_font, (255, 255, 255), win)
g_key = Message(WIDTH//2 + 30, HEIGHT//2 + 0, 16, "Nhấn G để ném bom", instructions_font, (255, 255, 255), win)
menu_key = Message(WIDTH//2 + 30, HEIGHT//2 + 30, 16, "Nhấn q để tạm dừng", instructions_font, (255, 255, 255), win)
exit_key = Message(WIDTH//2 + 30, HEIGHT//2 + 60, 16, "Nhấn esc để thoát khỏi game", instructions_font, (255, 255, 255), win)
game_won_msg = Message(WIDTH//2 + 10, HEIGHT//2 - 50, 50, "WINNER", winner_font, (255, 255, 255), win)
lose_msg = Message(WIDTH//2 + 10, HEIGHT//2 -50, 50, "Thua cuộc", winner_font, (255, 255, 255), win)
pause_msg = Message(WIDTH//2 + 10, HEIGHT//2 -50, 50, "Tạm dừng", winner_font, (255, 255, 255), win)


t = Text(instructions_font, 12)
font_color = (12, 12, 12)
play = t.render('Chơi Mới', font_color)
play_next = t.render('Chơi tiếp', font_color)
level=t.render('Level', font_color)
controls = t.render('Hướng dẫn', font_color)
exit = t.render('Thoát', font_color)
main_menu = t.render('Menu', font_color)

soud_menu = t.render('Âm lượng', font_color)
onSounds = t.render('Bật', font_color)
offSounds = t.render("Tắt", font_color)
remuses = t.render("Tiếp tục", font_color)
replays = t.render("Chơi lại", font_color)
level_1 = t.render('Level 1', font_color)
level_2 = t.render('Level 2', font_color)
level_3 = t.render('Level 3', font_color)
level_4 = t.render('Level 4', font_color)
level_5 = t.render('Level 5', font_color)
# BUTTONS *********************************************************************

ButtonBG = pygame.image.load('Assets/ButtonBG.png')
bwidth = ButtonBG.get_width()

play_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2, ButtonBG, 0.5, play, 10)

play_next= Button(WIDTH//2 - bwidth//4, HEIGHT//2 +30, ButtonBG, 0.5, play_next,10)

Level= Button(WIDTH//2 - bwidth//4, HEIGHT//2 +60, ButtonBG, 0.5, level,10)

controls_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 90, ButtonBG, 0.5, controls, 10)
sounds_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 120, ButtonBG, 0.5, soud_menu, 10)
exit_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 158, ButtonBG, 0.5, exit, 10)

# main_play_next= Button(WIDTH//2 - bwidth//4, HEIGHT//2 +120, ButtonBG, 0.5, play_next,10)

main_menu_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 150, ButtonBG, 0.5, main_menu, 20)
on_sound_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2, ButtonBG, 0.5, onSounds, 10)
off_sound_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 30, ButtonBG, 0.5, offSounds, 10)
main_menu_btn_remuse = Button(WIDTH//2 - bwidth//4 - 80, HEIGHT//2 + 120, ButtonBG, 0.5, main_menu, 20)
continue_btn_remuse = Button(WIDTH//2 - bwidth//4 + 80, HEIGHT//2 + 120, ButtonBG, 0.5, remuses, 10)
replay_btn_remuse = Button(WIDTH//2 - bwidth//4 + 80, HEIGHT//2 + 120, ButtonBG, 0.5, replays, 10)

level_1_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2, ButtonBG, 0.5,level_1, 10)
level_2_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2+40, ButtonBG, 0.5,level_2, 10)
level_3_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2+80, ButtonBG, 0.5,level_3, 10)
level_4_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2+120, ButtonBG, 0.5,level_4, 10)
level_5_btn = Button(120+WIDTH//2 - bwidth//4, HEIGHT//2, ButtonBG, 0.5,level_5, 10)
# MUSIC ***********************************************************************


pygame.mixer.music.load('Sounds/mixkit-complex-desire-1093.mp3')
pygame.mixer.music.play(loops=-1)


diamond_fx = pygame.mixer.Sound('Sounds/point.mp3')

bullet_fx = pygame.mixer.Sound('Sounds/bullet.wav')
jump_fx = pygame.mixer.Sound('Sounds/jump.mp3')
health_fx = pygame.mixer.Sound('Sounds/health.wav')
menu_click_fx = pygame.mixer.Sound('Sounds/menu.mp3')
next_level_fx = pygame.mixer.Sound('Sounds/level.mp3')
grenade_throw_fx = pygame.mixer.Sound('Sounds/grenade throw.wav')


# GROUPS **********************************************************************


bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

objects_group = [water_group, diamond_group, potion_group, enemy_group, exit_group]

p_image = pygame.transform.scale(pygame.image.load('Assets/Player/Idle/0.png'), (32,32))
p_rect = p_image.get_rect(center=(470, 200))
p_dy = 1
p_ctr = 1


# LEVEL VARIABLES **************************************************************

ROWS = 24
COLS = 40
SCROLL_THRES = 200


level_sim = 1
chose_level=1
level_length = 0
screen_scroll = 0
bg_scroll = 0
dx = 0
tmp_score = 0
# RESET ***********************************************************************

def reset_level(level):
	
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	enemy_group.empty()
	water_group.empty()
	diamond_group.empty()
	potion_group.empty()
	exit_group.empty()

	# LOAD LEVEL WORLD

	world_data, level_length = load_level(level)
	w = World(objects_group)
	w.generate_world(world_data, win)

	return world_data, level_length, w

def reset_player():
	p = Player(20, 60)
	moving_left = False
	moving_right = False

	return p, moving_left, moving_right
def score_player(my_score):
	return Message(WIDTH - 40, 20, 20, f'{my_score}', winner_font, (255, 255, 255), win)
def my_score_player(my_score):
	return Message(WIDTH//2 + 10, HEIGHT//2 , 30, f'Score: {my_score}', winner_font, (255, 255, 255), win)
# MAIN GAME *******************************************************************

main_menu = True
sounds_page = False
Level_page = False
play_level =  False
controls_page = False
exit_page = False
game_start = False
remuse_page = False
replay_page = False
game_won = True
running = True
while running:
   	
	Grenade.sound_nade(Full_Sound)
	Ghost.volume(Full_Sound)
	pygame.mixer.music.set_volume(Full_Sound)
	diamond_fx.set_volume(Full_Sound)
	bullet_fx.set_volume(Full_Sound)
	jump_fx.set_volume(Full_Sound)
	health_fx.set_volume(Full_Sound)
	menu_click_fx.set_volume(Full_Sound)
	next_level_fx.set_volume(Full_Sound)
	grenade_throw_fx.set_volume(Full_Sound)
	win.fill((0,0,0))
	for x in range(5):
		win.blit(BG1, ((x*WIDTH) - bg_scroll * 0.6, 0))
		win.blit(BG2, ((x*WIDTH) - bg_scroll * 0.7, 0))
		win.blit(BG3, ((x*WIDTH) - bg_scroll * 0.8, 0))
	
	if not game_start:
		win.blit(MOON, (-60, 150))

	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: 
			
				running = False
			if event.key == pygame.K_q:
				remuse_page = True
				game_start = False
				

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or \
				event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_RIGHT or \
				event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_UP or \
				event.key == pygame.K_w:
				if not p.jump:
					p.jump = True
					jump_fx.play()
			if event.key == pygame.K_SPACE:
				x, y = p.rect.center
				direction = p.direction
				bullet = Bullet(x, y, direction, (240, 240, 240), 1, win)
				bullet_group.add(bullet)
				bullet_fx.play()
				p.attack = True
    
			if event.key == pygame.K_g:
				if p.grenades:
					p.grenades -= 1
					grenade = Grenade(p.rect.centerx, p.rect.centery, p.direction, win)
					grenade_group.add(grenade)
					grenade_throw_fx.play()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or \
				event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_RIGHT or \
				event.key == pygame.K_d:
				moving_right = False
		

	if main_menu:
		ghostbusters.update()
		
		win.blit(p_image, p_rect)
		p_rect.y += p_dy
		p_ctr += p_dy
		if p_ctr > 35 or p_ctr < -35:
			p_dy *= -1
		


		if play_btn.draw(win):
			menu_click_fx.play()
			time.sleep(0.08)
			
			world_data, level_length, w = reset_level("1")
			p, moving_left, moving_right = reset_player()

			game_start = True
			main_menu = False
			game_won = False
   
		if play_next.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			f_level = open('level.txt', 'r+')
			level_next= f_level.read()
			level_sim = level_next
			f_level.close()
			world_data, level_length, w = reset_level(level_next)
			p, moving_left, moving_right = reset_player()

			game_start = True
			main_menu = False
			game_won = False
		# if main_play_next.draw(win):
		
		if Level.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			Level_page=True
			main_menu = False
   
		if sounds_btn.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			sounds_page = True
			main_menu = False

		if controls_btn.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			controls_page = True
			main_menu = False

		if exit_btn.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			running = False
   
	elif sounds_page:
		
		if main_menu_btn.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			sounds_page = False
			main_menu = True
		
		if on_sound_btn.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			Full_Sound = 0.2
			 
			 
			
		if off_sound_btn.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			Full_Sound = 0
			 
			 
   
	elif Level_page:
		f_level = open('save_level_max.txt', 'r+')
		max_level_save=int( f_level.read())
		
		
		
		if main_menu_btn.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			Level_page = False
			main_menu = True
		if max_level_save>=4:
			if level_5_btn.draw(win):
				menu_click_fx.play() 
				time.sleep(0.08)
				chose_level=5
				Level_page = False
				play_level = True
		if max_level_save>=3:
			if level_4_btn.draw(win):
				menu_click_fx.play() 
				time.sleep(0.08)
				chose_level=4
				Level_page = False
				play_level = True
		if max_level_save>=2:
			if level_3_btn.draw(win):
				menu_click_fx.play() 
				time.sleep(0.08)
				chose_level=3
				Level_page = False
				play_level = True
    
		if max_level_save>=1:
			if level_2_btn.draw(win):
				
				menu_click_fx.play() 
				time.sleep(0.08)
				chose_level=2
				Level_page = False
				play_level = True
   
		
		if level_1_btn.draw(win):
			Level_page = False
			chose_level=1
			play_level = True
		f_level.write(str(chose_level))
		

	elif play_level:	
			
			world_data, level_length, w = reset_level(str(chose_level))
			p, moving_left, moving_right = reset_player()
			
			# chose_level=1
			play_level = False
			game_start = True
			game_won=False
			
		
	elif controls_page:
		left_key.update()
		right_key.update()
		up_key.update()
		space_key.update()
		g_key.update()
		menu_key.update()
		exit_key.update()
		

		if main_menu_btn.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			controls_page = False
			main_menu = True
	elif remuse_page:
		pause_msg.update()
		my_score_play = my_score_player(score).update()
		if main_menu_btn_remuse.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			remuse_page = False
			main_menu = True
			score = 0
		if continue_btn_remuse.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			remuse_page = False
			game_start = True
			
	elif replay_page:
		lose_msg.update()
		my_score_play = my_score_player(tmp_score).update()
		if main_menu_btn_remuse.draw(win):
			menu_click_fx.play()
			time.sleep(0.08)
			replay_page = False
			main_menu = True
		if replay_btn_remuse.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			replay_page = False
			game_start = True	
	elif exit_page:
		pass

	elif game_won:
		game_won_msg.update()
		my_score_play = my_score_player(score).update()
		f_level = open('level.txt', 'r+')
		if main_menu_btn.draw(win):
			menu_click_fx.play()
			time.sleep(0.08)
			controls_page = False
			main_menu = True
		if play_next.draw(win):
			menu_click_fx.play() 
			time.sleep(0.08)
			if level_sim==3:
				world_data, level_length, w = reset_level("3")
			else: 
				world_data, level_length, w = reset_level(str(level_sim))
			p, moving_left, moving_right = reset_player()

			game_start = True
			# main_menu = False
			game_won = False
	
	elif game_start:
		
		score_msg = score_player(score).update()
		win.blit(MOON, (-60, -10))
		w.draw_world(win, screen_scroll)

		# Updating Objects ********************************************************

		bullet_group.update(screen_scroll, w)
		grenade_group.draw(win)
		grenade_group.update(screen_scroll, p, enemy_group, explosion_group, w)
		explosion_group.draw(win)
		explosion_group.update(screen_scroll)

		water_group.update(screen_scroll)
		water_group.draw(win)
		diamond_group.update(screen_scroll)
		diamond_group.draw(win)
		potion_group.update(screen_scroll)
		potion_group.draw(win)
		exit_group.update(screen_scroll)
		exit_group.draw(win)
		

		enemy_group.update(screen_scroll, bullet_group, p)
		enemy_group.draw(win)

		

		screen_scroll = 0
		p.update(moving_left, moving_right, w)
		p.draw(win)

		if (p.rect.right >= WIDTH - SCROLL_THRES and bg_scroll < (level_length*TILE_SIZE) - WIDTH) \
			or (p.rect.left <= SCROLL_THRES and bg_scroll > abs(dx)):
			dx = p.dx
			p.rect.x -= dx
			screen_scroll = -dx
			bg_scroll -= screen_scroll


		# Collision Detetction ****************************************************

		if p.rect.bottom > HEIGHT:
			p.health = 0

		if pygame.sprite.spritecollide(p, water_group, False):
			p.health = 0
			level = 1

		if pygame.sprite.spritecollide(p, diamond_group, True):
			diamond_fx.play()
			score += 100
			# score_msg = score_player(score).update()
			pass

		if pygame.sprite.spritecollide(p, exit_group, False):
			next_level_fx.play()
			level_sim += 1
			if level_sim>=3:
				level_sim =3
			game_won = True


		potion = pygame.sprite.spritecollide(p, potion_group, False)
		if potion:
			if p.health < 100:
				potion[0].kill()
				p.health += 15
				health_fx.play()
				if p.health > 100:
					p.health = 100


		for bullet in bullet_group:
			enemy =  pygame.sprite.spritecollide(bullet, enemy_group, False)
			if enemy and bullet.type == 1:
				if not enemy[0].hit:
					enemy[0].hit = True
					enemy[0].health -= 50
					if(enemy[0].health == 0):
						score += 50
						# score_msg = score_player(score).update()
				bullet.kill()
			
			if bullet.rect.colliderect(p):
				if bullet.type == 2:
					if not p.hit:
						p.hit = True
						p.health -= 20
						print(p.health)
					bullet.kill()
				# score += 50
		
		# drawing variables *******************************************************

		if p.alive:
			color = (0, 255, 0)
			if p.health <= 40:
				# p.health+=60
				color = (255, 0, 0)
			pygame.draw.rect(win, color, (6, 8, p.health, 20), border_radius=10)
		pygame.draw.rect(win, (255, 255, 255), (6, 8, 100, 20), 2, border_radius=10)

		for i in range(p.grenades):
			pygame.draw.circle(win, (200, 200, 200), (20 + 15*i, 40), 5)
			pygame.draw.circle(win, (255, 50, 50), (20 + 15*i, 40), 4)
			pygame.draw.circle(win, (0, 0, 0), (20 + 15*i, 40), 1)
		
		if p.health <= 0:
			f = open("level.txt", "w")
			f.write(str(chose_level))
			f.close()
			world_data, level_length, w = reset_level(chose_level)
			p, moving_left, moving_right = reset_player() 

			screen_scroll = 0
			bg_scroll = 0
			tmp_score = score
			score = 0

			main_menu = False
			sounds_page = False
			controls_page = False
			game_start = False
			replay_page = True

	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 4, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()