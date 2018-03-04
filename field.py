#!/usr/bin/python

from line import *
from net import *
from post import *


class Field:
    def __init__(self, sfce, width=FIELD_W, height=FIELD_H):
        self.sfce = sfce
        self.rect = pygame.Rect(0, 0, width, height)
        self.bkgImg = pygame.image.load(BKG_IMG)
        self.bkgImg = pygame.transform.scale(self.bkgImg, (width, height))
        self.height = height
        self.width = width
        self.posts = pygame.sprite.Group([])
        self.goals = pygame.sprite.Group([])
        self.field_sfce = self.bkgImg
        self.draw()
        self.sfce.blit(self.field_sfce, (0, 0))

    def draw(self):
        Line(BORDER_TOP_IMG, (0, 0), (self.width, BORDER_HEIGHT), sfce=self.field_sfce)
        Line(BORDER_BOT_IMG, (0, self.height - BORDER_HEIGHT), (self.width, BORDER_HEIGHT), sfce=self.field_sfce)
        Line(CENTER_LINE_IMG, (self.rect.centerx, self.rect.centery), (0, 0),  sfce=self.field_sfce)
#       pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.topright), (self.FieldRect.bottomright), 1)
#       pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.midtop), (self.FieldRect.midbottom), 3)
#       pygame.draw.circle(self.FieldSfce, SNOW, (self.FieldRect.centerx+1, self.FieldRect.centery+1), FIELD_CENTER_SIZE, 3)
        Net(self.field_sfce, 0, 0, NET_SIZE, FIELD_H)
        Net(self.field_sfce, FIELD_W - NET_SIZE+1, 0, NET_SIZE*2, FIELD_H)
        Line(BORDER_SIDE_IMG, (self.width-1, self.rect.centery), (0, 0), sfce=self.sfce)
        line_goalleft=Line(GOAL_LINE_IMG, (POST_LEFT_X, (POST_TOP_Y+POST_BOT_Y)/2), (0, 0), self.goals, self.field_sfce)
        line_goalleft.rect = pygame.Rect(POST_LEFT_X - 1, POST_TOP_Y + POST_SIZE, 3, (POST_BOT_Y - POST_TOP_Y - POST_SIZE))

        line_topleft=Line(BORDER_SIDE_IMG, (POST_LEFT_X, 0), (0, 0))
        line_topleft.rect.midbottom = (POST_LEFT_X, POST_TOP_Y)
        self.field_sfce.blit(line_topleft.image, line_topleft.rect)
        line_botleft=Line(BORDER_SIDE_IMG, (POST_LEFT_X, 0), (0, 0))
        line_botleft.rect.midtop = (POST_LEFT_X, POST_BOT_Y)
        self.field_sfce.blit(line_botleft.image, line_botleft.rect)

        line_goalright=Line(GOAL_LINE_IMG, (POST_RIGHT_X, (POST_TOP_Y+POST_BOT_Y)/2), (0, 0), self.goals, self.field_sfce)
        line_goalright.rect = pygame.Rect(POST_RIGHT_X-1, POST_TOP_Y+POST_SIZE, 3, (POST_BOT_Y - POST_TOP_Y - POST_SIZE))

        line_topright=Line(BORDER_SIDE_IMG, (POST_RIGHT_X, 0), (0, 0))
        line_topright.rect.midbottom = (POST_RIGHT_X, POST_TOP_Y)
        self.field_sfce.blit(line_topright.image, line_topright.rect)
        line_botright=Line(BORDER_SIDE_IMG, (POST_RIGHT_X, 0), (0, 0))
        line_botright.rect.midtop = (POST_RIGHT_X, POST_BOT_Y)
        self.field_sfce.blit(line_botright.image, line_botright.rect)

        Post(POST_IMG, (POST_SIZE, ), (POST_RIGHT_X, POST_TOP_Y), self.posts, self.field_sfce)
        Post(POST_IMG, (POST_SIZE, ), (POST_LEFT_X, POST_TOP_Y), self.posts, self.field_sfce)
        Post(POST_IMG, (POST_SIZE, ), (POST_LEFT_X, POST_BOT_Y), self.posts, self.field_sfce)
        Post(POST_IMG, (POST_SIZE, ), (POST_RIGHT_X, POST_BOT_Y), self.posts, self.field_sfce)
