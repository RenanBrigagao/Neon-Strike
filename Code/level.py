#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.entity import Entity
from Code.entityFactory import EntityFactory


class Level:
    def __init__(self, screen, name, game_mode):
        self.screen = screen
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg', (0, 0)))

    def run(self):
        while True:
            for ent in self.entity_list:
                self.screen.blit(source=ent.surf, dest=ent.rect)
                ent.move()
            pygame.display.flip()
