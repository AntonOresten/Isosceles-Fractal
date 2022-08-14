import math
import pygame
from pygame import gfxdraw

pygame.font.init()
font = pygame.font.SysFont('Consolas', 12)

line_func = pygame.draw.aaline
line_width = -1

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

background_color = '#202030'
empty = pygame.Color(0,0,0,0)
draw_surf = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()

# Flawed algorithm/function that uses slopes and only utilizes the tan function
# A better function would use sin and cos (would probably be simpler as well.. idk)
def draw_triangle(surf, point1, point2, theta, n):
    sgn = 1
    if point2[1] < point1[1]:
        sgn = -1
    try:
        slope = (point1[1]-point2[1])/(point1[0]-point2[0])
        slope_normal = -1/slope
    except ZeroDivisionError:
        return False
    distance = ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5
    middle_point = (point1[0]+point2[0])/2, (point1[1]+point2[1])/2
    height = math.tan(math.radians(theta))*distance/2
    
    delta_x = (height**2/(slope_normal**2+1))**0.5*sgn
    delta_y = slope_normal*delta_x

    point3 = middle_point[0]+delta_x, middle_point[1]+delta_y
    
    line_func(surf, '#bbbbbb', point1, point2, line_width)
    line_func(surf, '#bbbbbb', point1, point3, line_width)
    line_func(surf, '#bbbbbb', point2, point3, line_width)

    if n > 0:
        if inward:
            draw_triangle(surf, point3, point1, theta, n-1)
            draw_triangle(surf, point2, point3, theta, n-1)
        else:
            draw_triangle(surf, point1, point3, theta, n-1)
            draw_triangle(surf, point3, point2, theta, n-1)
            
    return True

#def draw_triangle(surf, point1, point2, theta, n):
#    distance = ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5
#    leg_length = distance/(2*math.cos(math.radians(theta)))
    

def draw_figure():
    draw_surf.fill(empty)
    draw_triangle(draw_surf, point1_rect.center, point2_rect.center, angle, iterations)
    gfxdraw.aacircle(draw_surf, *point1_rect.center, 4, pygame.Color('#dd2222'))
    gfxdraw.filled_circle(draw_surf, *point1_rect.center, 4, pygame.Color('#dd2222'))
    gfxdraw.aacircle(draw_surf, *point2_rect.center, 4, pygame.Color('#2266cc'))
    gfxdraw.filled_circle(draw_surf, *point2_rect.center, 4, pygame.Color('#2266cc'))

point1_rect = pygame.Rect((0,0), (20,20))
point1_rect.center = (200, 300)
point2_rect = pygame.Rect((0,0), (20,20))
point2_rect.center = (600, 400)

angle = 40.0
iterations = 7
inward = False

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

            # Increment angle
            if event.key == pygame.K_m:
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
        f'width = {line_width}',
        True, (225, 230, 240)), (40, height-30))

    pygame.display.update()

pygame.quit()
