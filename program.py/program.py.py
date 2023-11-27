# -*- coding: cp1251 -*-
import pygame
import random

# Инициализация Pygame
pygame.init()

# Ширина и высота окна игры
width = 1280
height = 720

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Создание окна игры
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Гоночная игра')

# Инициализация часов
clock = pygame.time.Clock()

# Плавное передвижения игрока при зажатых кнопках
pygame.key.set_repeat(100, 30)

# Класс автомобиля
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_left(self, pixels):
        self.rect.x -= pixels

    def move_right(self, pixels):
        self.rect.x += pixels

    def move_up(self, pixels):
        self.rect.y -= pixels

    def move_down(self, pixels):
        self.rect.y += pixels

# Класс противника
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height, speed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = 0 - self.rect.height
            self.rect.x = random.randrange(0, width - self.rect.width)

# Игровой цикл
def game_loop():
    game_exit = False
    game_over = False

    player_car = Car(width * 0.45, height * 0.8, blue, 30, 60)
    enemy_cars = pygame.sprite.Group()

    for i in range(10):
        enemy = Enemy(random.randrange(0, width - 50), random.randrange(-1500, -100),
                      red, 50, 80, random.randint(4, 8))
        enemy_cars.add(enemy)
        
    # Вывод окна 
    while not game_exit:
        while game_over:
            game_display.fill(black)
            font_style = pygame.font.SysFont(None, 40)
            message = font_style.render("Игра окончена. Нажмите R чтобы сыграть еще раз или Q чтобы выйти.", True, white)
            game_display.blit(message, [width * 0.15, height * 0.45])
            pygame.display.update()

            # Отработка нажатий рестарта и выхода из игры
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_r:
                        game_loop()
                        
        # Передвижение игрока по нажатию кнопок
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_car.move_left(5)
                elif event.key == pygame.K_RIGHT:
                    player_car.move_right(5)
                elif event.key == pygame.K_UP:
                    player_car.move_up(5)
                elif event.key == pygame.K_DOWN:
                    player_car.move_down(5)

        # Обновление позиции противников
        enemy_cars.update()

        # Отрисовка экрана игры
        game_display.fill(black)
        player_car_group = pygame.sprite.Group(player_car)
        player_car_group.draw(game_display)
        enemy_cars.draw(game_display)

        # Проверка столкновения с противником
        if pygame.sprite.spritecollide(player_car, enemy_cars, False):
            game_over = True

        # Обновление экрана
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

# Запуск игры
game_loop()
