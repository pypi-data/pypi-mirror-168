import pygame

pygame.init()


class Button(object):
    def __init__(self, x:int = 0, y:int = 0, width:int = 200, height:int = 50, text:str = "TEXT HERE", font:str = 'calibri', fontsize:int = 11, color:tuple = (0, 0, 0), background:tuple = (230, 230, 230), backgroundHover:tuple = (200, 200, 200), borderColour:tuple = (230, 230, 230), borderHoverColour:tuple = (200, 200, 200), borderWeight:int = 1, bold:bool = False, italic:bool = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.fs = fontsize
        self.bold = bold
        self.italic = italic
        self.color = color
        self.bg = background
        self.bgHover = backgroundHover
        self.border = borderColour
        self.hBorder = borderHoverColour
        self.borderWidth = borderWeight
        self.visible = True
        self.hover = False

    def draw(self, window):
        self.isHover()
        if self.visible:
            if self.hover:
                pygame.draw.rect(window, self.bgHover, (self.x, self.y, self.width, self.height))
                if self.borderWidth > 0:
                    pygame.draw.rect(window, self.hBorder, (self.x, self.y, self.width, self.height), self.borderWidth)
            else:
                pygame.draw.rect(window, self.bg, (self.x, self.y, self.width, self.height))
                if self.borderWidth > 0:
                    pygame.draw.rect(window, self.border, (self.x, self.y, self.width, self.height), self.borderWidth)

            font = pygame.font.SysFont(self.font, self.fs, self.bold, self.italic)
            text = font.render(self.text, True, self.color)
            text_rect = text.get_rect()
            width = text_rect.width
            height = text_rect.height

            textX = (self.x + (self.width // 2)) - width // 2
            textY = (self.y + (self.height // 2)) - height // 2

            window.blit(text, (textX, textY))

    def isHover(self):
        mouse = pygame.mouse.get_pos()

        if mouse[0] >= self.x and mouse[0] <= self.x + self.width:
            if mouse[1] >= self.y and mouse[1] <= self.y + self.height:
                self.hover = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                self.hover = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.hover = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return self.hover

    def getPressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.hover:
            return True
        else:
            return False
