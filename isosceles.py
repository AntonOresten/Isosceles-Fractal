import math
import cmath

import pygame
from pygame import gfxdraw


tuplify = lambda zs: [(z.real, z.imag) for z in zs]
complify = lambda ts: [complex(*t) for t in ts]


pygame.font.init()
font = pygame.font.SysFont('Consolas', 12)

line_func = pygame.draw.line
line_width = 1

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

background_color = '#181820'
empty = pygame.Color(0,0,0,0)
draw_surf = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()


def third_point(point1: complex, point2: complex, theta: float):
    base_vector = point2-point1
    base_length = abs(base_vector)
    leg_length = base_length/(2*math.cos(theta))
    scaling_factor = leg_length / base_length
    leg_vector = base_vector * (math.cos(theta) + 1j*math.sin(theta)) * scaling_factor
    return point1 + leg_vector


def draw_triangle(surf, point1: complex, point2: complex, theta, n):
    point3 = third_point(point1, point2, theta)
    pos1, pos2, pos3 = tuplify([point1, point2, point3])
    
    if n < iterations_drawn:
        if draw_base:
            line_func(surf, '#bbbbbb', pos1, pos2, line_width)
        line_func(surf, '#bbbbbb', pos1, pos3, line_width)
        line_func(surf, '#bbbbbb', pos2, pos3, line_width)

    if n > 0:
        if inward:
            theta = -theta
        draw_triangle(surf, point1, point3, theta, n-1)
        draw_triangle(surf, point3, point2, theta, n-1)
    

def draw_figure():
    point1, point2 = complify([point1_rect.center, point2_rect.center])
    draw_surf.fill(empty)
    
    # I think point1 and point2 need to be flipped because of pygames coordinate system (with the origin in the top left)
    draw_triangle(draw_surf, point2, point1, math.radians(angle), iterations)
    gfxdraw.aacircle(draw_surf, *point1_rect.center, 4, pygame.Color('#dd2222'))
    gfxdraw.filled_circle(draw_surf, *point1_rect.center, 4, pygame.Color('#dd2222'))
    gfxdraw.aacircle(draw_surf, *point2_rect.center, 4, pygame.Color('#2266cc'))
    gfxdraw.filled_circle(draw_surf, *point2_rect.center, 4, pygame.Color('#2266cc'))

point1_rect = pygame.Rect((0,0), (20,20))
point1_rect.center = (100, height+360)
point2_rect = pygame.Rect((0,0), (20,20))
point2_rect.center = (width-100, height+360)

angle = 45.0
iterations = 15
iterations_drawn = 1
inward = False
draw_base = False

draw_figure()

clicked = False
moving1 = False
moving2 = False
run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                run = False

            # Increment angle
            elif event.key == pygame.K_m:
                angle += 0.2
            elif event.key == pygame.K_k:
                angle += 1
            elif event.key == pygame.K_n:
                angle -= 0.2
            elif event.key == pygame.K_j:
                angle -= 1
            
            # Change number of iterations
            elif event.key == pygame.K_x:
                iterations = max(0, iterations+1)
            elif event.key == pygame.K_z:
                iterations = max(0, iterations-1)
            
            # Invert
            elif event.key == pygame.K_i:
                inward = not inward

            elif event.key == pygame.K_c:
                if line_func == pygame.draw.aaline:
                    line_func = pygame.draw.line
                elif line_func == pygame.draw.line:
                    line_func = pygame.draw.aaline
            
            elif event.key == pygame.K_q:
                line_width = max(1, line_width-1)
            elif event.key == pygame.K_w:
                line_width = max(1, line_width+1)
            
            elif event.key == pygame.K_y:
                iterations_drawn = min(iterations, max(1, iterations_drawn+1))
            elif event.key == pygame.K_u:
                iterations_drawn = max(1, iterations_drawn-1)

            elif event.key == pygame.K_b:
                draw_base = not draw_base

            angle = max(0, angle)

            draw_figure()

        elif event.type == pygame.MOUSEWHEEL:
            angle += event.y * 0.5
            angle = max(0, angle)

            draw_figure()
            
    mouse_state = pygame.mouse.get_pressed()
    if mouse_state[0]:
        clicked = True
        mouse_position = pygame.mouse.get_pos()
        if (point1_rect.collidepoint(*mouse_position) or moving1) and not moving2:
            moving1 = True
            point1_rect.center = mouse_position
            draw_figure()
                
        elif (point2_rect.collidepoint(*mouse_position) or moving2) and not moving1:
            moving2 = True
            point2_rect.center = mouse_position
            draw_figure()
            
    elif clicked and not mouse_state[0]:
        clicked = False
        moving1 = False
        moving2 = False

    screen.fill(background_color)
    screen.blit(draw_surf, (0,0))
    screen.blit(font.render(
        f'iterations = {round(iterations)}, '
        f'angle = {round(angle,1)}, '
        f'dimension = {round(1/(1+math.log2(math.cos(math.radians(angle)))),3)}, '
        f'width = {line_width}, '
        f'iterations_drawn = {iterations_drawn}',
        True, (225, 230, 240)), (40, height-30))

    pygame.display.update()


pygame.image.save(screen, f"koch{iterations}.png")

pygame.quit()
