import pygame as py
from pygame.locals import *
from sys import exit
import os
import json

# Paths relative to this file
_DIR  = os.path.dirname(os.path.abspath(__file__))
_IMG  = os.path.join(_DIR, "Images")
_SAVE = os.path.join(_DIR, "Saves", "cookie_clicker_save.json")

# Initialise
py.init()
clock = py.time.Clock()
FPS = 60

# Window
WIDTH, HEIGHT = 720, 900
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Cookie Clicker")

# Images
images = {
    "grandma_image":       py.image.load(os.path.join(_IMG, "GrandmaIconTransparent.webp")),
    "farm_image":          py.image.load(os.path.join(_IMG, "FarmIconTransparent.webp")),
    "cursor_image":        py.image.load(os.path.join(_IMG, "CursorIconTransparent.webp")),
    "multiplicator_image": py.image.load(os.path.join(_IMG, "MultiplicatorTransparent.webp"))
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Cookie():
    def __init__(self, screen):
        self.screen = screen
        self._base_image = py.transform.scale(
            py.image.load(os.path.join(_IMG, "Cookie.png")), (200, 200))
        self.image = self._base_image.copy()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Points():
    def __init__(self, screen):
        self.screen = screen
        self.font = py.font.SysFont("Arial", 30, bold=True)
        self.cookies = 0

    def draw(self):
        text = f"{int(self.cookies)} cookies"
        img = self.font.render(text, True, WHITE)
        rect = img.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(img, rect)

class Shop():
    def __init__(self, screen):
        self.screen = screen
        self.font = py.font.SysFont("Arial", 25)
        self.items = [
            {"name": "Cursor",        "image": images["cursor_image"],        "price": 10,    "amount": 0},
            {"name": "Grandma",       "image": images["grandma_image"],       "price": 100,   "amount": 0},
            {"name": "Farm",          "image": images["farm_image"],          "price": 1000,  "amount": 0},
            {"name": "Multiplicator", "image": images["multiplicator_image"], "price": 10000, "amount": 0}
        ]

    def draw(self):
        for i, item in enumerate(self.items):
            img = py.transform.scale(item["image"], (50, 50))
            self.screen.blit(img, (50, 150 + i * 100))
            text = f"{item['name']} - {item['price']} cookies - {item['amount']} owned"
            img_text = self.font.render(text, True, WHITE)
            self.screen.blit(img_text, (110, 150 + i * 100))

def save_game(points, shop):
    data = {
        "cookies": points.cookies,
        "shop": [{"name": item["name"], "amount": item["amount"]} for item in shop.items]
    }
    os.makedirs(os.path.dirname(_SAVE), exist_ok=True)
    with open(_SAVE, "w") as f:
        json.dump(data, f)

def load_game(points, shop):
    if os.path.exists(_SAVE):
        with open(_SAVE, "r") as f:
            data = json.load(f)
            points.cookies = data["cookies"]
            for item in shop.items:
                for saved_item in data["shop"]:
                    if item["name"] == saved_item["name"]:
                        item["amount"] = saved_item["amount"]

def main_Cookie_Clicker():
    clock = py.time.Clock()
    FPS = 60

    BACKGROUND = py.image.load(os.path.join(_IMG, "Background.png"))

    points = Points(screen)
    cookie = Cookie(screen)
    shop   = Shop(screen)

    load_game(points, shop)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(BACKGROUND, (0, 0))

        # Passive income
        for item in shop.items:
            if item["name"] == "Cursor":
                points.cookies += item["amount"] * 0.1 / FPS
            elif item["name"] == "Grandma":
                points.cookies += item["amount"] * 1.0 / FPS
            elif item["name"] == "Farm":
                points.cookies += item["amount"] * 8.0 / FPS

        multiplicator_amount = next(
            item["amount"] for item in shop.items if item["name"] == "Multiplicator")
        cookie_click_value = 1 * (2 ** multiplicator_amount)

        for event in py.event.get():
            if event.type == py.QUIT:
                save_game(points, shop)
                py.quit()
                exit()

            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = py.mouse.get_pos()
                if event.button == 1 or event.button == 3:
                    if cookie.rect.collidepoint(mouse_x, mouse_y):
                        points.cookies += cookie_click_value
                        cookie.image = py.transform.scale(cookie._base_image, (180, 180))
                    for item in shop.items:
                        item_rect = py.Rect(50, 150 + shop.items.index(item) * 100, 50, 50)
                        if item_rect.collidepoint(mouse_x, mouse_y) and points.cookies >= item["price"]:
                            points.cookies -= item["price"]
                            item["amount"] += 1

            elif event.type == py.MOUSEBUTTONUP:
                mx, my = py.mouse.get_pos()
                if cookie.rect.collidepoint(mx, my):
                    cookie.image = cookie._base_image.copy()

        points.draw()
        cookie.draw()
        shop.draw()

        py.display.flip()
        clock.tick(FPS)

main_Cookie_Clicker()
