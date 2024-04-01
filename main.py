import pygame
import math
import pymunk
import pymunk.pygame_util

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 678
BOTTOM_PANEL = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
pygame.display.set_caption("Pool")

space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

clock = pygame.time.Clock()
FPS = 120

lives = 3
diameter = 36
pocket_diameter = 66
force = 0
max_force = 10000
force_direction = 1
game_running = True
cue_ball_potted = False
taking_shot = True
powering_up = False
potted_balls = []

BG = (50, 50, 50)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Lato", 30)
large_font = pygame.font.SysFont("Lato", 60)

cue_image = pygame.image.load("images/cue.png")
table_image = pygame.image.load("images/cue.png")
ball_images = []
for i in range(1, 17):
    image = pygame.image.load(f"images/ball_{1}.png")
    ball_images.append(image)


def draw_text(text, font, text_color, x, y):
    writing = font.render(text, True, text_color)
    screen.blit(writing, (x, y))


def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 1000

    space.add(body, shape, pivot)
    return shape


balls = []
rows = 5
for col in range(5):
    for row in range(rows):
        pos = (250 + (col * (diameter + 1)), 267 + (row * (diameter + 1)) + (col * diameter / 2))
        new_ball = create_ball(diameter / 2, pos)
        balls.append(new_ball)
    rows -= 1

pos = (888, SCREEN_HEIGHT / 2)
cue_ball = create_ball(diameter / 2, pos)
balls.append(cue_ball)

pockets = [
    (55, 63),
    (592, 48),
    (1134, 64),
    (55, 616),
    (592, 629),
    (1134, 616)
]

cushions = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]


def create_cushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0, 0))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.8
    space.add(body, shape)


for i in cushions:
    create_cushion(i)


class Cue:
    def __init__(self, pos):
        self.original_image = cue_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, angle):
        self.angle = angle

    def draw(self, screen):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        screen.blit(self.image,
                    (self.rect.centerx - self.image.get_width() / 2,
                     self.rect.centery - self.image.get_height() / 2))
