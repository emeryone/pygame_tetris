import pygame
from random import randrange
import sys
import os


New_block = True
End = False
speed = 1000
delay = speed
speed_step = 1.15
count = 1
score = 0
blocks = [[[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],              #1 * 4
          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 1, 0]],              #T-тетрамино
          [[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],              #z-тетрамино
          [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0]],              #L-тетрамино
          [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]]              #квадрат 2 * 2
FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def game():
    global count, End, New_block, speed, delay
    screen.fill((0, 0, 0))
    start_screen()

    screen.fill((0, 0, 0))
    well = Board(12, 25, screen)
    well.draw_score()
    well.draw()
    block_item = Block((randrange(64, 256), randrange(64, 256), randrange(64, 256)),
                       blocks[randrange(len(blocks))], well.width // 2 - 2, 0, well)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not End:
                if event.key == pygame.K_UP:
                    block_item.rotate()
                if event.key == pygame.K_LEFT:
                    block_item.shift(-1)
                if event.key == pygame.K_RIGHT:
                    block_item.shift(1)
                if event.key == pygame.K_DOWN:
                    block_item.full_down()
            if event.type == MYEVENTTYPE and not End:
                block_item.clean()
                block_item.down()
                if New_block:
                    if count % 5 == 0:
                        speed = int(speed / speed_step)
                    New_block = False
                    block_item = Block((randrange(64, 256), randrange(64, 256), randrange(64, 256)),
                                       blocks[randrange(len(blocks))], well.width // 2 - 2, 0, well)
                    delay = speed
                    pygame.time.set_timer(MYEVENTTYPE, delay)
                    count += 1
                    if not block_item.check(1):
                        End = True
                else:
                    block_item.draw()
                    pygame.time.set_timer(MYEVENTTYPE, delay)
        if End:
            game_over()
            end_screen()
            game()
        clock.tick()
        pygame.display.flip()
    pygame.quit()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ТЕТРИС", "",
                  "Думаю, все вы знаете правила тетриса, но на всякий случай:",
                  "Сверху экрана начнут падать фигурки",
                  "Нужно стараться сложить их так, чтобы получались полные ряды",
                  "Такие ряды исчезают, увеличивая счет на 100 очков",
                  "Вы можете поворачивать и двигать в стороны фигурки",
                  "Используйте для этого стрелки клавиатуры", "",
                  "Чтобы начать игру, нажмите мышкой на экран"]

    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('magenta'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    global End, New_block, score, speed
    intro_text = [' '.join(["ВАШ СЧЕТ:", str(score)]), "",
                  "Шелкните мышью, если хотите сыграть еще"]

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                End = False
                New_block = True
                score = 0
                speed = 1000
                return
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Board:
    def __init__(self, width, height, screen):
        self.screen = screen
        self.width = width
        self.height = height
        self.board = [[0] * (width + 2) for _ in range(height)]
        self.board.append([1] * (width + 2))
        for i in range(len(self.board)):
            self.board[i][0] = 1
            self.board[i][-1] = 1
        self.colors = [[] for _ in range(height + 1)]
        for i in range(height + 1):
            for j in range(width + 2):
                self.colors[i].append((0, 0, 0))
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def color_cell(self, x, y, color):
        pygame.draw.rect(screen, color,
                         (self.left + self.cell_size * x, self.top + self.cell_size * y,
                          self.cell_size, self.cell_size))
        self.draw_boarder()

    def draw_boarder(self):
        pygame.draw.line(self.screen, (255, 255, 255), (self.left + self.cell_size, self.top + 4 * self.cell_size),
                         (self.left + self.cell_size, self.height * self.cell_size + self.top), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (self.left + self.cell_size, self.top + 4 * self.cell_size),
                         ((self.width + 1) * self.cell_size + self.left, self.top + 4 * self.cell_size), 1)
        pygame.draw.line(self.screen, (255, 255, 255),
                         ((self.width + 1) * self.cell_size + self.left, self.height * self.cell_size + self.top),
                         (self.left + self.cell_size, self.height * self.cell_size + self.top), 1)
        pygame.draw.line(self.screen, (255, 255, 255),
                         ((self.width + 1) * self.cell_size + self.left, self.height * self.cell_size + self.top),
                         ((self.width + 1) * self.cell_size + self.left, self.top + 4 * self.cell_size), 1)

    def draw(self):
        for i in range(self.height + 1):
            for j in range(self.width + 2):
                self.color_cell(j, i, self.colors[i][j])
        self.draw_boarder()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def apply(self, points, x, y, color):
        global New_block, speed, delay
        for i in range(4):
            for j in range(4):
                if points[i][j] == 1:
                    self.board[y + i][x + j] = 1
                    self.colors[y + i][x + j] = color
                    New_block = True
        for i in range(self.height):
            if self.board[i] == [1] * (self.width + 2):
                self.del_row(i)
        self.screen.fill((0, 0, 0))
        self.draw_score()
        self.draw()
        delay = speed
        pygame.time.set_timer(MYEVENTTYPE, delay)

    def del_row(self, row):
        global score
        new_row = []
        for i in range(self.width + 2):
            new_row.append((0, 0, 0))
        del self.board[row]
        self.board.insert(0, [1] + [0] * self.width + [1])
        del self.colors[row]
        self.colors.insert(0, new_row)
        self.draw()
        score += 100

    def draw_score(self):
        global score
        font = pygame.font.Font(None, 50)
        text = font.render(' '.join(["Score:", str(score)]), True, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2 + self.width * (self.cell_size - 8) // 2
        text_y = self.top + self.cell_size * 8
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        #pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
        #                                      text_w + 20, text_h + 20), 1)


class Block:
    def __init__(self, color, points, x, y, well):
        self.points = points
        self.color = color
        self.x = x
        self.y = y
        self.well = well

    def b_copy(self):
        return Block(self.color, self.points, self.x, self.y, self.well)

    def clean(self):
        for i in range(4):
            for j in range(4):
                if self.points[i][j] == 1:
                    self.well.color_cell(j + self.x, i + self.y, (0, 0, 0))

    def draw(self):
        for i in range(4):
            for j in range(4):
                if self.points[i][j] == 1:
                    self.well.color_cell(j + self.x, i + self.y, self.color)

    def rotate(self):
        new_b = self.b_copy()
        #new_b.points = [[self.points[j][i] for j in range(4)] for i in range(4)]
        new_b.points = list(zip(*new_b.points[::-1]))
        if new_b.check(0):
            self.clean()
            self.points = new_b.points
            self.draw()

    def shift(self, dir):
        new_b = self.b_copy()
        new_b.x += dir
        if new_b.check(0):
            self.clean()
            self.x = new_b.x
            self.draw()

    def down(self):
        self.y += 1
        if not self.check(1):
            self.well.apply(self.points, self.x, self.y, self.color)

    def check(self, delta):
        for i in range(4):
            for j in range(4):
                if self.points[i][j] == 1 and self.y + i <= self.well.height - delta:
                    if self.well.board[self.y + i + delta][self.x + j] == 1:
                        return False
        return True

    def full_down(self):
        global delay
        delay = 10
        pygame.time.set_timer(MYEVENTTYPE, delay)


if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption('')
        size = width, height = 800, 800
        screen = pygame.display.set_mode(size)

        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, delay)
        clock = pygame.time.Clock()
        game()