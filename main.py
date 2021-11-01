import os
import sys
import time
import subprocess
import serial
from serial.tools import list_ports

import math
import pygame as pg
from pygame.math import Vector2


class Wheelchair(pg.sprite.Sprite):

  def __init__(self, pos=(420, 420)):
    super(Wheelchair, self).__init__()
    self.image = pg.transform.scale(pg.image.load('wheelchair.png')\
                                        .convert_alpha(), (128, 128))
    self.original_image = self.image
    self.rect = self.image.get_rect(center=pos)
    self.position = Vector2(pos)
    self.direction = Vector2(1, 0)  # A unit vector pointing rightward.
    # self.speed = 2
    self.speed = 0
    self.angle = 0
    self.angle_speed = 0

  def update(self, WIDTH, HEIGHT):
    if self.angle_speed != 0:
      # Rotate the direction vector and then the image.
      self.direction.rotate_ip(self.angle_speed)
      self.angle += self.angle_speed
      self.image = pg.transform.rotate(self.original_image, -self.angle)
      self.rect = self.image.get_rect(center=self.rect.center)
    # Update the position vector and the rect.
    self.position += self.direction * self.speed
    wrap_around = False
    if self.position[0] <  0 :
      # off screen left
      self.rect.move_ip(WIDTH, 0)
      wrap_around = True

    if self.position[0]  + self.image.get_width() > WIDTH:
      # off screen right
      self.rect.move_ip(-WIDTH, 0)
      wrap_around = True

    if self.position[1]  < 0:
      # off screen top
      self.rect.move_ip(0, HEIGHT) 
      wrap_around = True

    if self.position[1] + self.image.get_height() > HEIGHT:
      # off screen bottom
      self.rect.move_ip(0, -HEIGHT) 
      wrap_around = True

    if wrap_around:
      self.rect.center = self.position

    self.position[0] %= WIDTH
    self.position[1] %= HEIGHT  
    self.rect.center = self.position


def main():
  connected_serial = None
  for port in list_ports.comports():
    if "Nano 33 BLE" in port.description: 
      connected_serial = port.device
  
  if not connected_serial:
    print('Serial port not found')
    return 1

  retry = 3
  port = None
  
  for i in range(retry):
    try:
      port = serial.Serial(connected_serial, baudrate=9600, timeout=5.0)
      break
    except:
      print('Serial port "{}" is busy, trying again in a second [{}/{}]...'.format(connected_serial, (i+1), retry))
      time.sleep(1)
  
  if not port:
    print('Serial port "{}" is busy'.format(connected_serial))
    return 1

  pg.init()
  WIDTH = 1280
  HEIGHT = 720
  screen = pg.display.set_mode((WIDTH, HEIGHT))
  
  wheelchair = Wheelchair((420, 420))
  wheelchairsprite = pg.sprite.RenderPlain((wheelchair))
  clock = pg.time.Clock()

  retry = 2000
  wheelchair_states = ["FORWARD", "FORWARD_LEFT", "FORWARD_RIGHT", 
                      "BACKWARD", "BACKWARD_LEFT", "BACKWARD_RIGHT", 
                      "IDLE", "ROTATE_LEFT", "ROTATE_RIGHT"]

  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        return

    clock.tick(60)
    try:
      curr_state = port.readline().decode("utf-8").strip()
      curr_state, ax, ay, az = curr_state.split("\t")
      if curr_state in wheelchair_states:
        if curr_state == "FORWARD":
          wheelchair.speed = 4
          wheelchair.angle_speed = 0
        elif curr_state == "BACKWARD":
          wheelchair.speed = -4
          wheelchair.angle_speed = 0
        elif curr_state == "ROTATE_LEFT":
          wheelchair.speed = 0
          wheelchair.angle_speed = -2
        elif curr_state == "ROTATE_RIGHT":
          wheelchair.speed = 0
          wheelchair.angle_speed = 2
        elif curr_state == "FORWARD_LEFT":
          wheelchair.speed = 4
          wheelchair.angle_speed = -2
        elif curr_state == "FORWARD_RIGHT":
          wheelchair.speed = 4
          wheelchair.angle_speed = 2
        elif curr_state == "BACKWARD_LEFT":
          wheelchair.speed = -4
          wheelchair.angle_speed = 2
        elif curr_state == "BACKWARD_RIGHT":
          wheelchair.speed = -4
          wheelchair.angle_speed = -2
        elif curr_state == "IDLE":
          wheelchair.speed = 0
          wheelchair.angle_speed = 0
        
        wheelchairsprite.update(WIDTH, HEIGHT)
        screen.fill((255, 255, 255))
        wheelchairsprite.draw(screen)

        font = pg.font.Font(pg.font.get_default_font(), 36)
        text_surface = font.render(curr_state, True, (127, 127, 127))
        screen.blit(text_surface, dest=(20,20))
        
        font = pg.font.Font(pg.font.get_default_font(), 24)
        text_surface = font.render("AX: {}".format(ax), True, (127, 127, 127))
        screen.blit(text_surface, dest=(20,70))
        text_surface = font.render("AY: {}".format(ay), True, (127, 127, 127))
        screen.blit(text_surface, dest=(20,100))
        text_surface = font.render("AZ: {}".format(az), True, (127, 127, 127))
        screen.blit(text_surface, dest=(20,130))
        pg.display.flip()
        
    except serial.serialutil.SerialException:
      retry -= 1
      if retry == 0:
        print("No data found, quitting.")
        return 1
    except KeyboardInterrupt:
      print("Stopped sending data.")
      break
        
    except:
      continue

  return



if __name__=="__main__":
  main()
  pg.quit()
  sys.exit()