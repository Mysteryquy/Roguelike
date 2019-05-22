#3rd party modules#3rd party modules
import pygame
import tcod as libtcodpy





#gamefiles
import constants

#WENN DAS GRÜN IST HAT ES GEKLAPPT

#     _______.___________..______       __    __    ______ .___________.
#    /       |           ||   _  \     |  |  |  |  /      ||           |
#   |   (----`---|  |----`|  |_)  |    |  |  |  | |  ,----'`---|  |----`
#    \   \       |  |     |      /     |  |  |  | |  |         |  |     
#.----)   |      |  |     |  |\  \----.|  `--'  | |  `----.    |  |     
#|_______/       |__|     | _| `._____| \______/   \______|    |__|   

class struc_Tile:
	def __init__(self, block_path):
		self.block_path = block_path
		self.explored = False






#  ______   .______          __   _______   ______ .___________.    _______.
# /  __  \  |   _  \        |  | |   ____| /      ||           |   /       |
#|  |  |  | |  |_)  |       |  | |  |__   |  ,----'`---|  |----`  |   (----`
#|  |  |  | |   _  <  .--.  |  | |   __|  |  |         |  |        \   \    
#|  `--'  | |  |_)  | |  `--'  | |  |____ |  `----.    |  |    .----)   |   
# \______/  |______/   \______/  |_______| \______|    |__|    |_______/  


class obj_Actor:
	def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
		self.x = x
		self.y = y
		self.sprite = sprite

		self.creature = creature
		if creature: 
			creature.owner = self

		self.ai = ai	
		if ai:
			ai.owner = self

	
	def draw(self):
		is_visible = libtcodpy.map_is_in_fov(FOV_MAP, self.x, self.y)

		if is_visible:
			SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))






#                                                         __          
#  ____  ____   _____ ______   ____   ____   ____   _____/  |_  ______
#_/ ___\/  _ \ /     \\____ \ /  _ \ /    \_/ __ \ /    \   __\/  ___/
#\  \__(  <_> )  Y Y  \  |_> >  <_> )   |  \  ___/|   |  \  |  \___ \ 
# \___  >____/|__|_|  /   __/ \____/|___|  /\___  >___|  /__| /____  >
#     \/            \/|__|               \/     \/     \/          \/ 


class com_Creature:

	def __init__(self, name_instance, hp = 10, death_function = None):
		self.name_instance = name_instance
		self.maxhp = hp
		self.hp = hp
		self.death_function = death_function

	def move(self, dx, dy):

		tile_is_wall = (GAME_MAP[self.owner.x + dx][self.owner.y + dy].block_path == True)

		target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

		if target:
			#im Tuturial ist das print unten rot aber anscheined geht es trotzdem
			self.attack(target, 3)

		if not tile_is_wall and target is None:
			self.owner.x += dx
			self.owner.y += dy		

	def attack(self, target, damage):
		print (self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) +" damage!")

		target.creature.take_damage(damage)
			

	def take_damage(self, damage):
		self.hp -= damage
		print (self.name_instance + "`s health is " + str(self.hp) + "/" + str(self.maxhp))

		if self.hp <= 0:

			if self.death_function is not None:
				self.death_function(self.owner)

#TODO class com_item:

#TODO class com_container:


#   _____  .___ 
#  /  _  \ |   |
# /  /_\  \|   |
#/    |    \   |
#\____|__  /___|
#        \/ 

class ai_Test:

	def take_turn(self):
		self.owner.creature.move(libtcodpy.random_get_int(None,-1,1), libtcodpy.random_get_int(None,-1,1))

def death_monster(monster):
	#On death, most monsters stop moving tho
	print (monster.creature.name_instance + " is slaughtered into ugly bits of flesh!")

	monster.creature = None
	monster.ai = None		
		




#.___  ___.      ___      .______   
#|   \/   |     /   \     |   _  \  
#|  \  /  |    /  ^  \    |  |_)  | 
#|  |\/|  |   /  /_\  \   |   ___/  
#|  |  |  |  /  _____  \  |  |      
#|__|  |__| /__/     \__\ | _|

def map_create():
	new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]


	new_map[10][10].block_path = True
	new_map[10][15].block_path = True

	for x in range(constants.MAP_WIDTH):
		new_map[x][0].block_path = True
		new_map[x][constants.MAP_HEIGHT-1].block_path = True

	for y in range(constants.MAP_HEIGHT):
		new_map[0][y].block_path = True
		new_map[constants.MAP_WIDTH-1][y].block_path = True	

	map_make_fov(new_map)	

	return new_map

def map_check_for_creature(x, y, exclude_object = None):
	
	target = None

	if exclude_object:
		#ceck objectlist to find creature at that location that isnt excluded
		for object in GAME_OBJECTS:
			if (object is not exclude_object and 
				object.x == x and 
				object.y == y and 
				object.creature):

				target = object
				

			if target:
				return target	

	else: 
		#ceck objectlist to find any creature at that location 
		for object in GAME_OBJECTS:
			if (object.x == x and 
				object.y == y and 
				object.creature):

				target = object
				

			if target:
				return target				

def map_make_fov(incoming_map):
	global FOV_MAP

	FOV_MAP = libtcodpy.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

	for y in range(constants.MAP_HEIGHT):
		for x in range(constants.MAP_WIDTH):
			libtcodpy.map_set_properties(FOV_MAP, x, y,not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)



def map_calculate_fov():
	global FOV_CALCULATE	

	if FOV_CALCULATE:
		FOV_CALCULATE = False
		libtcodpy.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
			constants.FOV_ALGO)



# _______  .______          ___   ____    __    ____  __  .__   __.   _______ 
#|       \ |   _  \        /   \  \   \  /  \  /   / |  | |  \ |  |  /  _____|
#|  .--.  ||  |_)  |      /  ^  \  \   \/    \/   /  |  | |   \|  | |  |  __  
#|  |  |  ||      /      /  /_\  \  \            /   |  | |  . `  | |  | |_ | 
#|  '--'  ||  |\  \----./  _____  \  \    /\    /    |  | |  |\   | |  |__| |  
#|_______/ | _| `._____/__/     \__\  \__/  \__/     |__| |__| \__|  \______|

def draw_game():

	global SURFACE_MAIN

	#clear the surface
	SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)


	#draw the map
	draw_map(GAME_MAP)

	
	for obj in GAME_OBJECTS:
		obj.draw()
	
	draw_debug()	

	#update the display
	pygame.display.flip()

def draw_map(map_to_draw):

	for x in range(0, constants.MAP_WIDTH):
		for y in range(0, constants.MAP_HEIGHT):

			is_visible = libtcodpy.map_is_in_fov(FOV_MAP, x, y)

			if is_visible:

				map_to_draw[x][y].explored = True

				if map_to_draw[x][y].block_path == True:

					SURFACE_MAIN.blit(constants.S_WALL, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT) )
				else:
					SURFACE_MAIN.blit(constants.S_FLOOR, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT) ) 

			elif map_to_draw[x][y].explored:

				if map_to_draw[x][y].block_path == True:

					SURFACE_MAIN.blit(constants.S_WALLEXPLORED, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT) )
				else:
					SURFACE_MAIN.blit(constants.S_FLOOREXPLORED, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT) ) 

def draw_debug():

	draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), (0,0), constants.COLOR_RED)

def draw_text(display_surface, text_to_display, T_coords, text_color):
	#This function takes in some text and displays it on the refered surface

	text_surf, text_rect = helper_text_objects(text_to_display, text_color)

	text_rect.topleft = T_coords

	display_surface.blit(text_surf, text_rect)



#          _______  _        _______  _______  _______  _______ 
#|\     /|(  ____ \( \      (  ____ )(  ____ \(  ____ )(  ____ \
#| )   ( || (    \/| (      | (    )|| (    \/| (    )|| (    \/
#| (___) || (__    | |      | (____)|| (__    | (____)|| (_____ 
#|  ___  ||  __)   | |      |  _____)|  __)   |     __)(_____  )
#| (   ) || (      | |      | (      | (      | (\ (         ) |
#| )   ( || (____/\| (____/\| )      | (____/\| ) \ \__/\____) |
#|/     \|(_______/(_______/|/       (_______/|/   \__/\_______)

def helper_text_objects(incoming_text, incoming_color):

	Text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

	return Text_surface, Text_surface.get_rect()









                                                                                        

#  _______      ___      .___  ___.  _______ 
# /  _____|    /   \     |   \/   | |   ____|
#|  |  __     /  ^  \    |  \  /  | |  |__   
#|  | |_ |   /  /_\  \   |  |\/|  | |   __|  
#|  |__| |  /  _____  \  |  |  |  | |  |____ 
# \______| /__/     \__\ |__|  |__| |_______|
                                            
def game_main_loop():

	game_quit = False

	player_action = "no-action"
	
	while not game_quit:



		player_action = game_handle_keys()

		map_calculate_fov()

		if player_action == "QUIT":
			game_quit = True

		elif player_action != "no-action":
			for obj in GAME_OBJECTS:
				if obj.ai:
					obj.ai.take_turn()

		

		#draw the game
		draw_game()

		CLOCK.tick(constants.GAME_FPS)

	#quit the game
	pygame.quit()
	exit()



def game_initialize():

	'''Das hier startet Pygame und das Hauptfenster'''	

	global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS, FOV_CALCULATE, CLOCK

	#initialize Pygame
	pygame.init()

	CLOCK = pygame.time.Clock()

	SURFACE_MAIN = pygame.display.set_mode( (constants.MAP_WIDTH*constants.CELL_WIDTH, constants.MAP_HEIGHT*constants.CELL_HEIGHT) )


	GAME_MAP = map_create()

	FOV_CALCULATE = True

	creature_com1 = com_Creature("greg")
	PLAYER = obj_Actor(1, 1, "python", constants.S_PLAYER, creature = creature_com1)

	creature_com2 = com_Creature("crabby", death_function = death_monster)
	ai_com = ai_Test()
	ENEMY = obj_Actor(20, 15, "crab", constants.S_ENEMY, creature = creature_com2, ai = ai_com)

	GAME_OBJECTS = [PLAYER, ENEMY]

def game_handle_keys():
	global FOV_CALCULATE

	#get player input
	events_list = pygame.event.get()

	#process input
	for event in events_list:
		if event.type == pygame.QUIT:
			return "QUIT"

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
					PLAYER.creature.move(0, -1)
					FOV_CALCULATE = True
					return "player moved"

			if event.key == pygame.K_DOWN:
					PLAYER.creature.move(0, 1)
					FOV_CALCULATE = True	
					return "player moved"

			if event.key == pygame.K_LEFT:
					PLAYER.creature.move(-1, 0)
					FOV_CALCULATE = True
					return "player moved"

			if event.key == pygame.K_RIGHT:
					PLAYER.creature.move(1, 0)
					FOV_CALCULATE = True
					return "player moved"

			if event.key == pygame.K_KP1:
					PLAYER.creature.move(-1, 1)
					FOV_CALCULATE = True
					return "player moved"

			if event.key == pygame.K_KP2:
					PLAYER.creature.move(0, 1)
					FOV_CALCULATE = True
					return "player moved"		
							
			if event.key == pygame.K_KP3:
					PLAYER.creature.move(1, 1)
					FOV_CALCULATE = True
					return "player moved"

			if event.key == pygame.K_KP4:
					PLAYER.creature.move(-1, 0)
					FOV_CALCULATE = True
					return "player moved"

			if event.key == pygame.K_KP5:
					PLAYER.creature.move(0, 0)
					FOV_CALCULATE = True
					return "player moved"				

			if event.key == pygame.K_KP6:
					PLAYER.creature.move(1, 0)
					FOV_CALCULATE = True
					return "player moved"		

			if event.key == pygame.K_KP7:
					PLAYER.creature.move(-1, -1)
					FOV_CALCULATE = True
					return "player moved"		

			if event.key == pygame.K_KP8:
					PLAYER.creature.move(0, -1)
					FOV_CALCULATE = True
					return "player moved"		

			if event.key == pygame.K_KP9:
					PLAYER.creature.move(1, -1)
					FOV_CALCULATE = True
					return "player moved"			

	return "no-action"			




if __name__ == '__main__':
	game_initialize()
	game_main_loop ()


#              .7
#            .'/
#           / /
#          / /
#         / /
#        / /
#       / /
#      / /
#     / /         
#    / /          
#  __|/
#,-\__\
#|f-"Y\|
#\()7L/
# cgD                            __ _
# |\(                          .'  Y '>,
#  \ \                        / _   _   \
#   \\\                       )(_) (_)(|}
#    \\\                      {  4A   } /
#     \\\                      \uLuJJ/\l
#      \\\                     |3    p)/
#       \\\___ __________      /nnm_n//
#       c7___-__,__-)\,__)(".  \_>-<_/D
#                  //V     \_"-._.__G G_c__.-__<"/ ( \
#                         <"-._>__-,G_.___)\   \7\
#                        ("-.__.| \"<.__.-" )   \ \
#                        |"-.__"\  |"-.__.-".\   \ \
#                        ("-.__"". \"-.__.-".|    \_\
#                        \"-.__""|!|"-.__.-".)     \ \
#                         "-.__""\_|"-.__.-"./      \ l
#                          ".__""">G>-.__.-">       .--,_
#                              ""  G

























