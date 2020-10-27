import socket
import sys
import time
import pygame
from pygame import gfxdraw


WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
TEXTCOLOR = (  0,   0,  0)
(width, height) = (600, 600)

running = True

def main():
    global running, screen

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(WHITE)
    pygame.display.update()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('localhost', 8080)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    connection, client_address = sock.accept()

    last = time.time()
    accum_dt = 0
    pos = [0, 5]

    while running:
        w, h = pygame.display.get_surface().get_size()
        ev = pygame.event.get()

        for event in ev:

            if event.type == pygame.QUIT:
                running = False
        
        time.sleep(1/60)
        cur = time.time()
        dt = cur - last
        last = cur

        accum_dt += dt
        if accum_dt > 1/30:
          connection.sendall(str(accum_dt).encode())
          pos = [float(n) for n in connection.recv(100).decode().split(",")]
          accum_dt = 0
        
        screen.fill(WHITE)
        draw_circle(screen, BLUE, w//2 + int(30*pos[0]), h - 60 - int(30*pos[1]), 60)
        pygame.display.update()

    connection.close()

def draw_circle(surface, color, x, y, radius):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

if __name__ == '__main__':
    main()