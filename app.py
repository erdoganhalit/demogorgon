import pgzrun
from random import randint, choice
from pygame.rect import Rect
from pgzero.actor import Actor

WIDTH = 800
HEIGHT = 608
EDGE_OFFSET = 32
COIN_OFFSET = 32
TILE_SIZE = 16

# Game States
game_state = "menu"  # "menu", "playing", "game_over"

# Hero class inherits from Actor
class Hero(Actor):
    def __init__(self, pos):
        image = "hero_down_0"
        super().__init__(image, pos)  # Call Actor's constructor
        self.animations = {
            "right": ["hero_right_0", "hero_right_1", "hero_right_2", "hero_right_3"],
            "left": ["hero_left_0", "hero_left_1", "hero_left_2", "hero_left_3"],
            "up": ["hero_up_0", "hero_up_1", "hero_up_2", "hero_up_3"],
            "down": ["hero_down_0", "hero_down_1", "hero_down_2", "hero_down_3"],
        }
        self.animation_index = 0
        self.is_moving = False
        self.direction = "down"
        self.velocity = {"x": 0, "y": 0}
        

    def update_animation(self, frame_speed, direction):
        self.animation_index = (self.animation_index + frame_speed) % len(self.animations[direction])
        self.image = self.animations[direction][int(self.animation_index)]

    def get_rect(self):
        return Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

# Enemy class inherits from Actor
class Enemy(Actor):
    def __init__(self, pos, direction, velocity):
        image = "demon_walk_down_0"
        super().__init__(image, pos)  # Call Actor's constructor
        self.animations = {
            "right": ["demon_walk_right_0", "demon_walk_right_1", "demon_walk_right_2", "demon_walk_right_3"],
            "left": ["demon_walk_left_0", "demon_walk_left_1", "demon_walk_left_2", "demon_walk_left_3"],
            "up": ["demon_walk_up_0", "demon_walk_up_1", "demon_walk_up_2", "demon_walk_up_3"],
            "down": ["demon_walk_down_0", "demon_walk_down_1", "demon_walk_down_2", "demon_walk_down_3"],
        }
        self.animation_index = 0
        self.direction = direction
        self.velocity = velocity

    def update_animation(self, frame_speed):
        self.animation_index = (self.animation_index + frame_speed) % len(self.animations[self.direction])
        self.image = self.animations[self.direction][int(self.animation_index)]

    def get_rect(self):
        return Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    

class Coin:
    def __init__(self, pos):
        self.x, self.y = pos
        self.width, self.height = 16, 16
        self.animation_frames = [f"coin_{i}" for i in range(15)]
        self.animation_index = 0
        self.image = self.animation_frames[0]
        self.is_moving = False

    def draw(self):
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))

    def update_animation(self):
        self.animation_index = (self.animation_index + 0.2) % len(self.animation_frames)
        self.image = self.animation_frames[int(self.animation_index)]

    def get_rect(self):
        return Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
    
class Portal:
    def __init__(self):
        self.x, self.y = WIDTH // 2 , HEIGHT // 2
        self.width, self.height = 64, 64
        self.animation_frames = [f"portal_{i}" for i in range(7)]
        self.animation_index = 0
        self.image = self.animation_frames[0]

    def draw(self):
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))

    def update_animation(self):
        self.animation_index = (self.animation_index + 0.2) % len(self.animation_frames)
        self.image = self.animation_frames[int(self.animation_index)]

    def get_rect(self):
        return Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
    
class Map:
    def __init__(self, obstacles):
        self.tile_size = 16
        self.obstacle_image = "map_1_2.png"
        self.default_image = "map_0_0.png"
        self.obstacles = obstacles
        self.grid = self.get_grid()

    def get_grid(self):
        grid_edges = {}
        for i, obs in enumerate(self.obstacles):
            x0, y0, x1, y1 = obs.left , obs.top , obs.left + obs.width , obs.top + obs.height
            grid_edges[i] = {
                "x0":x0 // self.tile_size, 
                "y0":y0 // self.tile_size, 
                "x1":x1 // self.tile_size, 
                "y1":y1 // self.tile_size
            }

        #print(grid_edges)

        map_grid = []
        for i in range(WIDTH // self.tile_size):
            row_grid = []
            for j in range(HEIGHT // self.tile_size):
                if (
                    (i in range(grid_edges[0]["x0"] , grid_edges[0]["x1"]) or i in range(grid_edges[1]["x0"] , grid_edges[1]["x1"]))
                    and (j in range(grid_edges[0]["y0"] , grid_edges[0]["y1"]) or j in range(grid_edges[2]["y0"] , grid_edges[2]["y1"]))
                ):
                    row_grid.append(1)
                else:
                    row_grid.append(0)
            map_grid.append(row_grid)
        return map_grid
    
    def draw(self):
        for i, row in enumerate(self.grid):
            for j, tile in enumerate(row):
                if tile == 1:
                    screen.blit(self.obstacle_image, (i*self.tile_size , j*self.tile_size))
                else:
                    screen.blit(self.default_image, (i*self.tile_size , j*self.tile_size))

# Obstacles
obstacles = [
    Rect(96, 96, 256, 160), # (6,6,16,10)
    Rect(448, 96, 256, 160), # (28,6,16,10)
    Rect(96, 352, 256, 160), # (6,22,16,10)
    Rect(448, 352, 256, 160) # (28,22,16,10)
]

map = Map(obstacles=obstacles)
portal = Portal()

"""coins = [
    Coin((250, 550)),
    Coin((290, 550)),
    Coin((330, 450)),
]"""
def create_coins():
    coins_storage = []
    for j in [COIN_OFFSET, WIDTH // 2, WIDTH - COIN_OFFSET]:
        for i in range(COIN_OFFSET,HEIGHT,COIN_OFFSET):
            coins_storage.append(
                Coin((j,i))
            )
    for j in [COIN_OFFSET, HEIGHT//2, HEIGHT-COIN_OFFSET]:
        for i in range(COIN_OFFSET,WIDTH,COIN_OFFSET):
            coins_storage.append(
                Coin((i,j))
            )
    coins_storage = list(set(coins_storage))
    return coins_storage

coins = create_coins()
#coins = deepcopy(coins_storage)
hero = Hero((50, HEIGHT - 50))

# Sprites
# hero = Actor("hero_down_0", (50, HEIGHT - 50))

enemy1 = Enemy(pos=(50, 50), direction="right", velocity={"x": 3, "y": 0})
enemy2 = Enemy(pos=(750, 50), direction="down", velocity={"x": 0, "y": 3})
enemy3 = Enemy(pos=(750, 550), direction="left", velocity={"x": -3, "y": 0})

#enemy1 = Actor("demon_walk_down_0", (50, 50))
#enemy2 = Actor("demon_walk_down_0", (750, 50))
#enemy3 = Actor("demon_walk_down_0", (750, 550))

# Enemy Setup
enemies = [enemy1, enemy2, enemy3]

# Menu Buttons
menu_buttons = [
    {"text": "Start Game", "rect": Rect(WIDTH // 2 - 100, 200, 200, 50)},
    {"text": "Toggle Sound", "rect": Rect(WIDTH // 2 - 100, 270, 200, 50)},
    {"text": "Exit", "rect": Rect(WIDTH // 2 - 100, 340, 200, 50)},
]

game_over_buttons = [
    {"text": "Restart", "rect": Rect(WIDTH // 2 - 100, 200, 200, 50)},
    {"text": "Quit", "rect": Rect(WIDTH // 2 - 100, 270, 200, 50)},
]

congrats_buttons = [
    {"text": "Play Again", "rect": Rect(WIDTH // 2 - 100, 200, 200, 50)},
    {"text": "Quit", "rect": Rect(WIDTH // 2 - 100, 270, 200, 50)},
]

# Flags and Movement Variables
sound_enabled = True
background_music = "background_music"
key_priority = None

# Functions for Animations
def update_animation(actor, animation_frames, frame_speed):
    actor.animation_index = (actor.animation_index + frame_speed) % len(animation_frames)
    actor.image = animation_frames[int(actor.animation_index)]

# Drawing Functions
def draw_menu():
    screen.clear()
    screen.fill("black")
    screen.draw.text("MAIN MENU", center=(WIDTH // 2, 100), fontsize=50, color="white")
    for button in menu_buttons:
        screen.draw.filled_rect(button["rect"], "blue")
        screen.draw.text(button["text"], center=button["rect"].center, color="white", fontsize=30)

def draw_game():
    screen.clear()
    #screen.fill("skyblue")
    for obstacle in obstacles:
        screen.draw.filled_rect(obstacle, "brown")
    map.draw()
    hero.draw()
    for enemy in enemies:
        enemy.draw()
    for coin in coins:
        coin.draw()
    if not coins:
        portal.draw()

def draw_game_over():
    screen.clear()
    screen.fill("black")
    screen.draw.text("GAME OVER", center=(WIDTH // 2, 100), fontsize=50, color="red")
    for button in game_over_buttons:
        screen.draw.filled_rect(button["rect"], "blue")
        screen.draw.text(button["text"], center=button["rect"].center, color="white", fontsize=30)

def draw_congrats():
    screen.clear()
    screen.fill("black")
    screen.draw.text("CONGRATULATIONS!", center=(WIDTH // 2, 100), fontsize=50, color="red")
    for button in congrats_buttons:
        screen.draw.filled_rect(button["rect"], "blue")
        screen.draw.text(button["text"], center=button["rect"].center, color="white", fontsize=30)

# Main Draw Function
def draw():
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "congrats":
        draw_congrats()

# Update Functions
def update_game():
    global game_state

    previous_position = hero.x, hero.y

    # Hero Movement
    hero.x += hero.velocity["x"]
    hero.y += hero.velocity["y"]

    # hero_rect = hero.get_rect() Rect(hero.x - hero.width // 2, hero.y - hero.height // 2, hero.width, hero.height)
    if any(hero.get_rect().colliderect(obstacle) for obstacle in obstacles):
        # Revert to the previous position if a collision occurs
        hero.x, hero.y = previous_position

    # Keep Hero on Screen
    hero.x = max(hero.width // 2, min(WIDTH - hero.width // 2, hero.x))
    hero.y = max(hero.height // 2, min(HEIGHT - hero.height // 2, hero.y))

    # Update Hero Animation
    if hero.is_moving:
        # update_animation(hero, hero.animations[hero.direction], 0.2)
        hero.update_animation(direction=hero.direction, frame_speed=0.2)

    else:
        # update_animation(hero, hero.animations["down"], 0.2)
        hero.update_animation(direction="down", frame_speed=0.2)

    for coin in coins:
        coin.update_animation()
        if hero.colliderect(coin.get_rect()):  # Check if hero collects the coin
            coins.remove(coin)
            sounds.coin.play()

    if len(coins)==0:
        portal.update_animation()

    # Enemy Movement
    for enemy in enemies:
        velocity = enemy.velocity

        # Randomly change direction
        if randint(0, 100) < 5:
            if (
                not any([enemy.colliderect(obstacle) for obstacle in obstacles])
            ):
                #print("random change")
                if enemy.direction in ["right", "left"]:
                    velocity["x"] = 0
                    if enemy.y < EDGE_OFFSET:
                        velocity["y"] = 3
                    elif enemy.y > HEIGHT-EDGE_OFFSET:
                        velocity["y"] = -3
                    else:
                        velocity["y"] = choice([-3, 3])
                    
                    if velocity["y"] == 3:
                        enemy.direction = "down"
                    else:
                        enemy.direction = "up"
                
                elif enemy.direction in ["up", "down"]:
                    velocity["y"] = 0
                    if enemy.x < EDGE_OFFSET:
                        velocity["x"] = 3
                    elif enemy.x > WIDTH - EDGE_OFFSET:
                        velocity["x"] = -3
                    else:
                        velocity["x"] = choice([-3, 3])
                    
                    if velocity["x"] == 3:
                        enemy.direction = "right"
                    else:
                        enemy.direction = "left"

        # Update position
        enemy.x += velocity["x"]
        enemy.y += velocity["y"]

        # Check screen boundaries
        if enemy.x < enemy.width // 2 or enemy.x > WIDTH - enemy.width // 2:
            velocity["x"] *= -1
        if enemy.y < enemy.height // 2 or enemy.y > HEIGHT - enemy.height // 2:
            velocity["y"] *= -1

        # Check obstacle collisions
        for obstacle in obstacles:
            if enemy.colliderect(obstacle):
                if enemy.direction in ["right", "left"]:
                    if velocity["x"] < 0:
                        enemy.x += 5
                    else:
                        enemy.x -= 5
                    velocity["x"] *= -1
                elif enemy.direction in ["up", "down"]:
                    if velocity["y"] < 0: # GOING UP
                        enemy.y += 5
                    else: # GOING DOWN
                        enemy.y -= 5
                    velocity["y"] *= -1

        # Update animation
        enemy.direction = "right" if velocity["x"] > 0 else "left" if velocity["x"] < 0 else \
                    "down" if velocity["y"] > 0 else "up"
        #update_animation(actor, actor.animations[direction], 0.1)
        enemy.update_animation(frame_speed=0.1)

        # Check collision with hero
        if enemy.colliderect(hero):
            game_state = "game_over"

        if (
            len(coins)==0
            and hero.x in range(portal.x-16 , portal.x+16)
            and hero.y in range(portal.y-16 , portal.y+16)
        ):
            game_state = "congrats"

# Main Update Function
def update():
    if game_state == "menu":
        pass
    elif game_state == "playing":
        update_game()

# Handling Input
def on_key_down(key):
    global key_priority
    if game_state == "playing" and not key_priority:
        key_priority = key
        if key == keys.LEFT:
            hero.velocity["x"] = -5
            hero.direction = "left"
            hero.is_moving = True
        elif key == keys.RIGHT:
            hero.velocity["x"] = 5
            hero.direction = "right"
            hero.is_moving = True
        elif key == keys.UP:
            hero.velocity["y"] = -5
            hero.direction = "up"
            hero.is_moving = True
        elif key == keys.DOWN:
            hero.velocity["y"] = 5
            hero.direction = "down"
            hero.is_moving = True

def on_key_up(key):
    global key_priority
    if key_priority == key:
        key_priority = None
        hero.velocity["x"] = hero.velocity["y"] = 0
        hero.is_moving = False

def on_mouse_down(pos):
    global game_state
    global sound_enabled
    global coins
    if game_state == "menu":
        for button in menu_buttons:
            if sound_enabled:
                music.play(background_music)
            if button["rect"].collidepoint(pos):
                if button["text"] == "Start Game":
                    game_state = "playing"
                    #if sound_enabled:
                    #    music.play(background_music)
                elif button["text"] == "Toggle Sound":
                    sound_enabled = not sound_enabled
                    if not sound_enabled:
                        music.stop()
                elif button["text"] == "Exit":
                    exit()
    elif game_state == "game_over":
        for button in game_over_buttons:
            if button["rect"].collidepoint(pos):
                if button["text"] == "Restart":
                    game_state = "playing"
                    hero.pos = (50, HEIGHT - 50)
                    enemies[0].pos = (50, 50)
                    enemies[1].pos = (750, 50)
                    enemies[2].pos = (750, 550)
                    coins = create_coins()
                elif button["text"] == "Quit":
                    exit()
    elif game_state == "congrats":
        for button in congrats_buttons:
            if button["rect"].collidepoint(pos):
                if button["text"] == "Play Again":
                    game_state = "playing"
                    hero.pos = (50, HEIGHT - 50)
                    enemies[0].pos = (50, 50)
                    enemies[1].pos = (750, 50)
                    enemies[2].pos = (750, 550)
                    coins = create_coins()
                elif button["text"] == "Quit":
                    exit()

pgzrun.go()
