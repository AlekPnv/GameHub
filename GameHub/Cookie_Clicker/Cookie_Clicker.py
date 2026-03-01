import pygame
import pygame.gfxdraw
import os
import json
import math

_DIR  = os.path.dirname(os.path.abspath(__file__))
_IMG  = os.path.join(_DIR, "Images")
_SAVE = os.path.join(_DIR, "Saves", "cookie_clicker_save.json")

pygame.init()
clock = pygame.time.Clock()
FPS   = 60

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cookie Clicker")

C_BG_LEFT   = (30,  20,  10)
C_BG_RIGHT  = (20,  13,   6)
C_PANEL     = (45,  30,  12)
C_PANEL_HI  = (65,  45,  18)
C_BORDER    = (120, 80,  30)
C_TEXT      = (255, 235, 180)
C_SUBTEXT   = (180, 150,  90)
C_GOLD      = (255, 200,  50)
C_GREEN     = (100, 220, 100)
C_BTN_BUY   = (80,  180,  60)
C_BTN_GREY  = (60,   60,  50)
C_DIVIDER   = (80,   55,  20)


F_HUGE   = pygame.font.SysFont("Arial", 38, bold=True)
F_BIG    = pygame.font.SysFont("Arial", 26, bold=True)
F_MED    = pygame.font.SysFont("Arial", 20)
F_SMALL  = pygame.font.SysFont("Arial", 16)
F_TINY   = pygame.font.SysFont("Arial", 13)

LEFT_W  = 420
RIGHT_X = LEFT_W + 1
RIGHT_W = WIDTH - RIGHT_X

SHOP_DATA = [
    {"name": "Cursor",        "img": "CursorIconTransparent.webp",       "price": 10,    "cps": 0.1,  "desc": "+0.1 cookies/sec"},
    {"name": "Grandma",       "img": "GrandmaIconTransparent.webp",      "price": 100,   "cps": 1.0,  "desc": "+1 cookie/sec"},
    {"name": "Farm",          "img": "FarmIconTransparent.webp",         "price": 1000,  "cps": 8.0,  "desc": "+8 cookies/sec"},
    {"name": "Multiplicator", "img": "MultiplicatorTransparent.webp",    "price": 10000, "cps": 0,    "desc": "×2 per click"},
]

def load_img(filename, size=None):
    img = pygame.image.load(os.path.join(_IMG, filename)).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img

cookie_img_base = load_img("Cookie.png", (200, 200))
shop_icons = [load_img(d["img"], (48, 48)) for d in SHOP_DATA]

def draw_rect_rounded(surf, color, rect, radius=10, alpha=255):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), (0, 0, rect[2], rect[3]), border_radius=radius)
    surf.blit(s, (rect[0], rect[1]))

def fmt_num(n):
    n = int(n)
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000:     return f"{n/1_000:.1f}K"
    return str(n)

def fmt_cps(v):
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M/s"
    if v >= 1_000:     return f"{v/1_000:.1f}K/s"
    if v < 1:          return f"{v:.1f}/s"
    return f"{v:.0f}/s"

cookies  = 0.0
items    = [{"amount": 0} for _ in SHOP_DATA]
click_scale   = 1.0 
click_particles = [] 
hover_item    = -1 

def save():
    os.makedirs(os.path.dirname(_SAVE), exist_ok=True)
    with open(_SAVE, "w") as f:
        json.dump({"cookies": cookies, "shop": [it["amount"] for it in items]}, f)

def load():
    global cookies
    if not os.path.exists(_SAVE): return
    try:
        with open(_SAVE) as f:
            data = json.load(f)
        cookies = data.get("cookies", 0)
        shop_data = data.get("shop", [])
        for i, amt in enumerate(shop_data):
            if i < len(items):
                if isinstance(amt, dict):
                    items[i]["amount"] = amt.get("amount", 0)
                else:
                    items[i]["amount"] = int(amt)
    except Exception:
        pass

def total_cps():
    cps = 0.0
    for i, d in enumerate(SHOP_DATA):
        cps += items[i]["amount"] * d["cps"]
    return cps

def click_value():
    mult = items[3]["amount"]   
    return 1 * (2 ** mult)


SHOP_ROW_H = 80
SHOP_TOP   = 90

def shop_row_rect(i):
    y = SHOP_TOP + i * (SHOP_ROW_H + 8)
    return pygame.Rect(RIGHT_X + 10, y, RIGHT_W - 20, SHOP_ROW_H)

def draw_left():
    # background
    pygame.draw.rect(screen, C_BG_LEFT, (0, 0, LEFT_W, HEIGHT))

    # header
    cps = total_cps()
    cookie_text   = F_HUGE.render(f"{fmt_num(cookies)} cookies", True, C_GOLD)
    cps_text      = F_MED.render(f"per second: {fmt_cps(cps)}", True, C_SUBTEXT)
    click_txt     = F_SMALL.render(f"per click: {fmt_num(click_value())}", True, C_SUBTEXT)

    screen.blit(cookie_text, cookie_text.get_rect(centerx=LEFT_W//2, y=18))
    screen.blit(cps_text,    cps_text.get_rect(centerx=LEFT_W//2, y=62))
    screen.blit(click_txt,   click_txt.get_rect(centerx=LEFT_W//2, y=86))

    pygame.draw.line(screen, C_DIVIDER, (30, 110), (LEFT_W-30, 110), 1)

    cx, cy = LEFT_W // 2, 340
    scaled = int(200 * click_scale)
    img = pygame.transform.smoothscale(cookie_img_base, (scaled, scaled))
    r   = img.get_rect(center=(cx, cy))
    screen.blit(img, r)

    pygame.gfxdraw.aacircle(screen, cx, cy, 108, (*C_BORDER, 60))
    pygame.gfxdraw.aacircle(screen, cx, cy, 110, (*C_BORDER, 30))

    for p in click_particles:
        alpha = int(255 * p[4] / p[5])
        s = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(s, 3, 3, 3, (255, 200, 50, alpha))
        screen.blit(s, (int(p[0])-3, int(p[1])-3))

    hint = F_TINY.render("click the cookie!", True, C_SUBTEXT)
    screen.blit(hint, hint.get_rect(centerx=LEFT_W//2, y=HEIGHT-30))

    return r

def draw_right():
    pygame.draw.rect(screen, C_BG_RIGHT, (RIGHT_X, 0, RIGHT_W, HEIGHT))
    pygame.draw.line(screen, C_BORDER, (RIGHT_X, 0), (RIGHT_X, HEIGHT), 2)

    # title
    title = F_BIG.render("SHOP", True, C_GOLD)
    screen.blit(title, title.get_rect(centerx=RIGHT_X + RIGHT_W//2, y=18))
    pygame.draw.line(screen, C_DIVIDER, (RIGHT_X+10, 56), (WIDTH-10, 56), 1)

    cps_label = F_TINY.render(f"Total CPS: {fmt_cps(total_cps())}", True, C_SUBTEXT)
    screen.blit(cps_label, cps_label.get_rect(centerx=RIGHT_X + RIGHT_W//2, y=68))

    item_rects = []
    for i, d in enumerate(SHOP_DATA):
        r      = shop_row_rect(i)
        amt    = items[i]["amount"]
        price  = d["price"]
        can    = cookies >= price
        hovered = (i == hover_item)

        bg_col = C_PANEL_HI if hovered else C_PANEL
        draw_rect_rounded(screen, bg_col, r, radius=8)
        if hovered:
            pygame.draw.rect(screen, C_BORDER, r, border_radius=8, width=1)

        screen.blit(shop_icons[i], (r.x + 10, r.y + r.h//2 - 24))

        name_surf = F_MED.render(d["name"], True, C_TEXT if can else C_SUBTEXT)
        desc_surf = F_TINY.render(d["desc"], True, C_SUBTEXT)
        screen.blit(name_surf, (r.x + 68, r.y + 14))
        screen.blit(desc_surf, (r.x + 68, r.y + 38))

        if amt > 0:
            badge_r = pygame.Rect(r.right - 44, r.y + r.h//2 - 14, 34, 28)
            draw_rect_rounded(screen, C_BORDER, badge_r, radius=6)
            amt_s = F_MED.render(str(amt), True, C_GOLD)
            screen.blit(amt_s, amt_s.get_rect(center=badge_r.center))

        price_col = C_GREEN if can else (150, 60, 60)
        price_s = F_SMALL.render(f"🍪 {fmt_num(price)}", True, price_col)
        screen.blit(price_s, (r.x + 68, r.y + 56))

        item_rects.append(r)

    return item_rects


def main_Cookie_Clicker():
    global cookies, click_scale, hover_item

    load()
    running = True
    last_save = pygame.time.get_ticks()

    while running:
        dt = clock.tick(FPS) / 1000.0   

        cookies += total_cps() * dt

        if click_scale < 1.0:
            click_scale = min(1.0, click_scale + 4 * dt)
        elif click_scale > 1.0:
            click_scale = max(1.0, click_scale - 4 * dt)

        for p in click_particles:
            p[0] += p[2] * dt * 60
            p[1] += p[3] * dt * 60
            p[3] += 0.3              
            p[4] -= 1
        click_particles[:] = [p for p in click_particles if p[4] > 0]

        screen.fill(C_BG_LEFT)
        cookie_rect  = draw_left()
        item_rects   = draw_right()
        pygame.display.flip()

        mx, my = pygame.mouse.get_pos()
        hover_item = next((i for i, r in enumerate(item_rects) if r.collidepoint(mx, my)), -1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if cookie_rect.collidepoint(mx, my):
                    cv = click_value()
                    cookies += cv
                    click_scale = 0.88
                    import random
                    for _ in range(8):
                        click_particles.append([
                            float(mx), float(my),
                            random.uniform(-3, 3), random.uniform(-5, -1),
                            30, 30
                        ])

                for i, r in enumerate(item_rects):
                    if r.collidepoint(mx, my):
                        price = SHOP_DATA[i]["price"]
                        if cookies >= price:
                            cookies -= price
                            items[i]["amount"] += 1

        if pygame.time.get_ticks() - last_save > 10_000:
            save()
            last_save = pygame.time.get_ticks()

main_Cookie_Clicker()
