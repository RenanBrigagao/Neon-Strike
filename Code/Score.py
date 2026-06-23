import sys
from datetime import datetime

import pygame
from pygame.constants import K_RETURN, KEYDOWN, K_BACKSPACE, K_ESCAPE
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.font import Font

from Code.DBProxy import DBProxy
from Code.const import C_WHITE, SCORE_POS, C_PINK, MENU_OPTION


class Score:

    def __init__(self, screen):
        self.screen = screen
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.wav')
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DBScore')
        name = ''
        while True:
            self.screen.blit(source=self.surf, dest=self.rect)
            self.score_text(48, 'YOU WIN!', C_PINK, SCORE_POS['Title'])
            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = 'Enter Player 1 name (4 characters):'
            if game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = 'Enter Team name (4 characters):'
            if game_mode == MENU_OPTION[2]:
                if player_score[0] >= player_score[1]:
                    score = player_score[0]
                    text = 'Enter Player 1 name (4 characters):'
                else:
                    score = player_score[1]
                    text = 'Enter Player 2 name (4 characters):'

            self.score_text(20, text, C_PINK, SCORE_POS['EnterName'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4:
                            name += event.unicode
            self.score_text(20, name, C_PINK, SCORE_POS['Name'])
            pygame.display.flip()
            pass

    def show(self):
        pygame.mixer_music.load('./asset/Score.wav')
        pygame.mixer_music.play(-1)
        self.screen.blit(source=self.surf, dest=self.rect)
        self.draw_score_panel()
        self.score_text(48, 'TOP 10 SCORE', C_PINK, SCORE_POS['Title'])
        self.score_text(20, 'NAME     SCORE           DATE      ', C_PINK, SCORE_POS['Label'])
        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player_score in list_score:
            id_, name, score, date = player_score
            self.score_text(20, f'{name}     {score:05d}     {date}', C_PINK,
                            SCORE_POS[list_score.index(player_score)])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()


    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.screen.blit(source=text_surf, dest=text_rect)

    def draw_score_panel(self):

        panel = pygame.Surface((380, 220), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        panel_rect = panel.get_rect(center=(self.screen.get_width() // 2,
                                            self.screen.get_height() // 2 - 20))

        self.screen.blit(panel, panel_rect)
        pygame.draw.rect(
            self.screen,
            C_PINK,
            panel_rect,
            3
        )

def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"
