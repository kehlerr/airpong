#!/usr/bin/python
# --*- coding: utf-8 -*-

import math
from collections import deque
from random import randint
from numpy import sign

import pygame
import obj_template
from field_defs import *
from slider_defs import SLIDER_H, SLIDER_W
from ball_defs  import *
from phys_defs  import *
from color_defs  import *
from sparkle import *


ANG_HIST_MAX=75
ANG_RND_DISP_MAX=3
WITH_SLIDER='slider'
WITH_GOAL_LEFT='goal_left'
WITH_GOAL_RIGHT='goal_right'


class Ball(obj_template.T):
    def __init__(self,
                 spr_img,
                 bkgImg,
                 pos,
                 group = None,
                 size = BALL_RAD,
                 start_ang = 45,
                 start_vel = BALL_SPEED,
                 max_vel   = MAX_BALL_SPEED,
                 delta_vel = BALL_DELTA_VEL
                ):

         obj_template.T.__init__(self, spr_img, (size, ), pos, group)
         self.bkgImg = bkgImg
         self.rad = self.size
         self.ang = start_ang
         self.ang_hist = deque([start_ang for i in range(ANG_HIST_MAX)], ANG_HIST_MAX)
         self.vel = start_vel
         self.max_vel   = max_vel
         self.delta_vel = delta_vel
         self.sparkles = pygame.sprite.RenderPlain([])

    def Live(self, sliders, posts):
         self.Move(sliders, posts)
         for sparkle in self.sparkles:
              sparkle.Live()
# TODO: [ref] привести в порядок функцию:
    def HandleCol(self, collision):
         if collision:
              if collision is WITH_SLIDER:
                   if self.vel < self.max_vel: self.vel += self.delta_vel
                   for i in range(30):
                        Sparkle(SPARKLE_IMG, (self.rect.centerx, self.rect.centery), ang=(randint(-180, 180)), group=self.sparkles)
              elif collision is WITH_GOAL_LEFT:
                   pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'collision':WITH_GOAL_LEFT}))
              elif collision is WITH_GOAL_RIGHT:
                   pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'collision':WITH_GOAL_RIGHT}))
         else:
              self.rect.centerx += self.dx
              self.rect.centery += self.dy


    def Move(self, sliders, posts):
    # движение мяча; sliders - возможные слайдеры (лист), posts - возможные штанги (лист)
    # расчет смещений
         self.dx = int(math.ceil(self.vel*math.cos(math.radians(self.ang))))
         self.dy = int(math.ceil(self.vel*math.sin(math.radians(self.ang))))
    # проверка и обработка столкновений
         self.HandleCol(self.ChkCollision(sliders, posts))

         self.ang_hist.popleft()
         self.ang_hist.append(math.ceil(math.fabs(int(self.ang))))
         if self.ang_hist.count(self.ang_hist[0]) == ANG_HIST_MAX:
              self.ang += randint(-ANG_RND_DISP_MAX, ANG_RND_DISP_MAX)


    def ShiftVectors(self, lim_dx, lim_dy):
    # создаём вектора с малыми частями смещений (dx и dy)
        if self.dx < lim_dx and self.dy < lim_dy:          # если смещения не слишком велики (до лимитов)
            return zip([self.dx], [self.dy])               # просто вернуть их

        if math.fabs(self.dx) >= math.fabs(self.dy):
            DX = [sign(self.dx) * lim_dx for i in range(int(math.fabs(self.dx)) / lim_dx)]
            if int(math.fabs(self.dx)) % lim_dx: DX.append(sign(self.dx) * (int(math.fabs(self.dx)) % lim_dx))

            DY = [self.dy / len(DX) for i in range(len(DX))]
            if int(math.fabs(self.dy)) % len(DX): DY[-1] += sign(self.dy) * (self.dy % len(DX))
        else:
            DY = [sign(self.dy) * lim_dx/2 for i in range(int(math.fabs(self.dy)) / lim_dx/2)]
            if int(math.fabs(self.dy)) % (lim_dx/2): DY.append(sign(self.dy) * (int(math.fabs(self.dy)) % (lim_dx/2)))

            DX = [self.dx / len(DY) for i in range(len(DY))]
            if int(math.fabs(self.dx)) % len(DY): DX[-1] += sign(self.dx) * (self.dx % len(DY))

        DX[len(DX) / 2], DX[-1] = DX[-1], DX[len(DX) / 2]
        DY[len(DY) / 2], DY[-1] = DY[-1], DY[len(DY) / 2]

        return zip(DX, DY)

    def ChkCollision(self, Sliders = None, Posts = None):
    # проверяем на столкновения с объектами и границами, Sliders - лист, Posts - лист; возвращает bool

         # границы сверху и снизу
         if math.fabs(FIELD_H/2 - (self.rect.centery + self.dy)) > FIELD_H/2:
              self.rect.centery = self.rad if self.rect.centery + self.dy < FIELD_H/2 else FIELD_H - self.rad
              self.ang *= -1
              return True

         # боковые границы
         if   self.rect.left + self.dx < L_GOAL_LINE:
              self.rect.left = L_GOAL_LINE
              self.ang = math.degrees(math.pi) - self.ang
              return WITH_GOAL_LEFT

         if   self.rect.right + self.dx > R_GOAL_LINE:
              self.rect.right = R_GOAL_LINE
              self.ang = math.degrees(math.pi) - self.ang
              return WITH_GOAL_RIGHT

         # столкновения со штангами
         for post in Posts:
              if math.sqrt((post.rect.centerx - self.rect.centerx) ** 2 + (post.rect.centery - self.rect.centery) ** 2) < self.rad + post.size/2:
                   self.GetRound(post.rect.centerx, post.rect.centery, post.size/2)
                   return True

         # столкновения со слайдерами
         for slider in Sliders:
              slider_xl = slider.rect.left
              slider_xr = slider.rect.right
              slider_xc = slider.rect.centerx
              slider_yt = slider.rect.top + slider.width/2
              slider_yb = slider.rect.bottom - slider.width/2

              if (self.rect.centerx < slider_xr and self.rect.centerx > slider_xl and self.rect.bottom>slider.rect.top and self.rect.top<slider.rect.bottom or self.ChkIntersect(slider)):

                  for (dx, dy) in self.ShiftVectors(slider.width/2, slider.height/2):
                       self.rect.centerx += dx
                       self.rect.centery += dy
                       collision = pygame.sprite.collide_mask(self, slider)
                       if collision:
                           if ( self.rect.centery >= slider_yt  and
                                self.rect.centery <= slider_yb ):
                               self.rect.centerx = slider_xc - sign(self.dx)*(slider.width/2 + self.rad)
                               self.ang = math.degrees(math.pi) - self.ang
                           elif self.rect.centery < slider_yt:
                               self.GetRound(slider_xc, slider_yt, slider.width/2)
                           elif self.rect.centery > slider_yb:
                               self.GetRound(slider_xc, slider_yb, slider.width/2)
                           return WITH_SLIDER

                  self.rect.centerx -= self.dx
                  self.rect.centery -= self.dy

         return False


    def ChkIntersect(self, slider):
        def onSegment((ax, ay), (bx, by), (cx, cy)):
            if (ax <= max(bx, cx) and ax >= min(bx, cx) and
               ay <= max(by, cy) and ay >= min(by, cy)):
                return True

            return False

        def CCW_orientation((ax, ay), (bx, by), (cx, cy)):
            val = (ay - by) * (cx - ax) - (ax - bx) * (cy - ay);
            if (val == 0):  return 0
            return 1 if val > 0 else 2

        x1 = self.rect.centerx
        y1 = self.rect.centery
        ball_p1 = (x1,y1)

        x2 = self.rect.centerx + self.dx
        y2 = self.rect.centery + self.dy
        ball_p2 = (x2, y2)

        x3 = slider.rect.centerx - sign(self.dx)*slider.width/2
        y3 = slider.rect.top
        slider_p1 = (x3, y3)

        x4 = slider.rect.centerx - sign(self.dx)*slider.width/2
        y4 = slider.rect.bottom
        slider_p2 = (x4, y4)

        o1 = CCW_orientation(ball_p1, ball_p2, slider_p1)
        o2 = CCW_orientation(ball_p1, ball_p2, slider_p2)
        o3 = CCW_orientation(slider_p1, slider_p2, ball_p1)
        o4 = CCW_orientation(slider_p1, slider_p2, ball_p2)

        if (o1 != o2 and o3 != o4):   return True
        if (o1 == 0 and onSegment(ball_p1, slider_p1, ball_p2)):   return True
        if (o2 == 0 and onSegment(ball_p1, slider_p2, ball_p2)):   return True
        if (o3 == 0 and onSegment(slider_p1, ball_p1, slider_p2)): return True
        if (o4 == 0 and onSegment(slider_p1, ball_p2, slider_p2)): return True

        return False


    def GetRound(self, centerx, centery, rad):
         h_cathet  = math.fabs(centery - self.rect.centery)
         c_hypoten = math.sqrt((centerx - self.rect.centerx)**2 + (centery - self.rect.centery)**2)
         try:
              ang_collide = math.asin(h_cathet/c_hypoten) if self.rect.centerx >= centerx else math.pi-math.asin(h_cathet/c_hypoten) # radians
         except ValueError:
              ang_collide = 1
         ang_collide *= 1 if self.rect.centery >= centery else -1
         self.rect.centerx = centerx + (rad + self.rad+5) * math.cos(ang_collide)
         self.rect.centery = centery + (rad + self.rad+5) * math.sin(ang_collide)
         self.ang = math.degrees((math.pi*2 + ang_collide) % (math.pi*2))
