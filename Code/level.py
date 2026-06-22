#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame._freetype import Font
from pygame.rect import Rect
from pygame.surface import Surface

from Code.const import COLOR_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY
from Code.entity import Entity
from Code.entityFactory import EntityFactory


class Level:
    def __init__(self, screen, name, game_mode):
        self.timeout = 20000
        self.screen = screen
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg', (0, 0)))
        self.entity_list.append(EntityFactory.get_entity('Player1', (0, 0)))
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            self.entity_list.append(EntityFactory.get_entity('Player2', (0, 0)))
        pygame.time.set_timer(EVENT_ENEMY, 2000)

    def run(self):
        pygame.mixer_music.load(f'./asset/{self.name}.wav')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for ent in self.entity_list:
                self.screen.blit(source=ent.surf, dest=ent.rect)
                ent.move()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', COLOR_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', COLOR_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', COLOR_WHITE, (10, WIN_HEIGHT - 20))
            self.level_text(14, f'Renan Brigagão RU: 5180714', COLOR_WHITE, (10, WIN_HEIGHT - 10))
            pygame.display.flip()
            pass

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.screen.blit(source=text_surf, dest=text_rect)
