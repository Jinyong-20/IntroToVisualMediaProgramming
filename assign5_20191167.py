# Free Sound: https://pgtd.tistory.com/110
# assignment: meet CEO and talk to him.
# assignment: play sound when bounce up

import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 30   # frames per second

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T 
    pygame.draw.polygon(screen, color=color, points=Ptransformed, width=3)
    return
#

def main():
    pygame.init() # initialize the engine

    sound = pygame.mixer.Sound("diyong.mp3")
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 150
    h = 40
    wh = w/4
    hh = h/4
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    XH = np.array([ [0,0], [wh, 0], [wh, hh], [0, hh]])
    position = [WINDOW_WIDTH/2-w/2, WINDOW_HEIGHT-100]

    angle = 0
    grab = False
    gangle = 0

    done = False
    while not done:
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grab = not grab


        #joint control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] :
            if angle > -70 :
                angle -= 1
        elif key[pygame.K_RIGHT] :
            if angle < 70 :
                angle += 1

        #grab Func
        if grab :
            if gangle < 30:
                gangle+=1
        elif grab == False :
            if gangle > 0:
                gangle-=1

        screen.fill( (200, 254, 219) )

        H0 = Tmat(position[0], position[1])
        
        draw(X, H0, screen, (0,0,0))
        H1 = H0 @ Tmat(w/2, 0) @ Rmat(angle-90) @ Tmat(0,-h/2)
        draw(X, H1, screen, (100,200,200))
        H2 = H1 @ Tmat(w, h/2) @ Rmat(angle*1.1) @ Tmat(0,-h/2)
        draw(X, H2, screen, (100,200,100))
        
        H3 = H2 @ Tmat(w, h/2) @ Rmat(angle*1.2) @ Tmat(0,-h/2)
        draw(X, H3, screen, (100,200,100))
        H4 = H3 @ Tmat(w, h/2) @ Rmat(angle*1.3) @ Tmat(0,-h/2)
        draw(X, H4, screen, (100,200,100))

        #hand
        hand0 = H4 @ Tmat(w, h/2) @Rmat(0) @Tmat(0, -hh/2)
        draw(XH, hand0, screen, (0,0,0))
        hand1 = hand0 @ Tmat(wh,hh/2) @ Rmat(90) @ Tmat(-wh/2, -hh/2)
        draw(XH, hand1, screen, (0,0,0))
        hand1L = hand1 @ Rmat(-90+gangle) @ Tmat(0, -hh/2)
        hand1R = hand1 @ Tmat(wh,0) @ Rmat(-90-gangle) @ Tmat(0, -hh/2)
        
        draw(XH, hand1L, screen, (0,0,0))
        draw(XH, hand1R, screen, (0,0,0))
        
        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()