import numpy as np
import pygame
import time


class ArrowKeysDisplay:

    def __init__(self, unselected_color, selected_color, border=None, scale=1, position=None):
        self.position = position
        self.scale = scale
        self.unselected_color = unselected_color
        self.selected_color = selected_color
        self.border = border
        self.width = 100  # pixels
        # rectangles
        self._left_key_rect = None
        self._up_key_rect = None
        self._right_key_rect = None
        self._down_key_rect = None
        self.build_model()

    def render(self, window, position, current_actions: list[int]):
        """

        :param window: window to blit model onto
        :param current_actions: list of actions that the agent has choosen
        :param position: position on the screen for the model to be printed on
        :param current_action:
        :return:
        """
        pygame.draw.rect(window, (self.unselected_color if current_actions.count(0) == 0 else self.selected_color),
                         self._left_key_rect.move(*position), border_radius=10)
        pygame.draw.rect(window, (self.unselected_color if current_actions.count(1) == 0 else self.selected_color),
                         self._up_key_rect.move(*position), border_radius=10)
        pygame.draw.rect(window, (self.unselected_color if current_actions.count(2) == 0 else self.selected_color),
                         self._right_key_rect.move(*position), border_radius=10)
        pygame.draw.rect(window, (self.unselected_color if current_actions.count(3) == 0 else self.selected_color),
                         self._down_key_rect.move(*position), border_radius=10)
        if self.border is not None:
            pygame.draw.rect(window, self.border,
                             self._left_key_rect.move(*position), width=10, border_radius=10)
            pygame.draw.rect(window, self.border,
                             self._up_key_rect.move(*position), width=10, border_radius=10)
            pygame.draw.rect(window, self.border,
                             self._right_key_rect.move(*position), width=10, border_radius=10)
            pygame.draw.rect(window, self.border,
                             self._down_key_rect.move(*position), width=10, border_radius=10)


    def build_model(self) -> np.array:
        # format is x1, y1, width, height
        self.width *= self.scale
        self._up_key_rect = pygame.rect.Rect(self.width, 0, self.width, self.width)
        self._left_key_rect = pygame.rect.Rect(0, self.width, self.width, self.width)
        self._down_key_rect = pygame.rect.Rect(self.width, self.width, self.width, self.width)
        self._right_key_rect = pygame.rect.Rect(self.width * 2, self.width, self.width, self.width)


class Label:

    def __init__(self, position, text="", size=12, font=None, color=(0, 0, 0), refresh_count=None, background=None,
                 anti_alias=False):
        """
        - Custom label class for rendering labels
        :param position:
        :param text:
        :param size:
        :param font:
        :param color:
        :param refresh_count:
        :param background:
        :param anti_alias:
        """
        self.font = font
        self.original_text = text
        self.text = text
        self.color = color
        self.size = size
        self.position = position
        self.background = background
        self.anti_alias = anti_alias
        self.refresh_count = refresh_count
        self.current_count = 0

        if font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.size)

    def render(self, window, position=None):
        text = self.font.render(self.text, self.anti_alias, self.color, self.background)
        window.blit(text, self.position if position is None else position)

    def append_text(self, text, refresh_count=None, append_to_front=False):
        if refresh_count is not None:
            self.refresh_count = refresh_count
        if self.refresh_count is None or self.current_count >= self.refresh_count:
            self.text = self.original_text + text if not append_to_front else text + self.original_text
            self.current_count = 0
        else:
            self.current_count += 1

    def update_text(self, text, refresh_count=None):
        if refresh_count is not None:
            self.refresh_count = refresh_count
        if self.refresh_count is None or self.current_count >= self.refresh_count:
            self.original_text = text
            self.text = text
        else:
            self.current_count += 1


class TimedLabel(Label):

    def __init__(self, position, timeout: float, queue, text="", size=12, font=None, color=(0, 0, 0),
                 refresh_count=None, background=None,
                 anti_alias=False):
        """
        :param position: (x, y)
        :param timeout: number of seconds for the label to last
        :param text:
        :param size:
        :param font:
        :param color:
        :param refresh_count:
        :param background:
        :param anti_alias:
        """
        super().__init__(position=position, text=text, size=size, font=font, color=color, refresh_count=refresh_count,
                         background=background, anti_alias=anti_alias)
        self.time_created = time.time()
        self.timeout = timeout
        self.queue = queue

    def render(self, window):
        if (time.time() - self.time_created) < self.timeout:
            text = self.font.render(self.text, self.anti_alias, self.color, self.background)
            window.blit(text, self.position)
        else:
            self._remove_label()

    def _remove_label(self):
        self.queue.remove_label()


class TimedLabelQueue:

    def __init__(self, window):
        self.labels = []
        self.current_label = None
        self._is_label_showing = False
        self._window = window

    def remove_label(self):
        self.current_label = None
        if len(self.labels) != 0:
            self.current_label = self.labels.pop(0)

    def display_label(self, label, force=False):
        if force or len(self.labels) == 0:
            self.current_label = label
        else:
            self.labels.append(label)

    def render(self):
        if self.current_label is not None:
            self.current_label.render(self._window)
