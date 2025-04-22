import os
import random
import sys

import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(scr_rct, obj_rct) -> dict[str, bool]:
    """
    オブジェクトの位置が画面内に収まっているかをチェックする関数。

    収まっている場合はTrue、収まっていない場合はFalseを返す。
    """
    return {
        "x": scr_rct.left <= obj_rct.left and obj_rct.right <= scr_rct.right,
        "y": scr_rct.top <= obj_rct.top and obj_rct.bottom <= scr_rct.bottom,
    }



def load_assets():
    bg_img = pg.image.load("fig/pg_bg.jpg")

    return bg_img


def initialize_objects(kk_img):
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    return kk_rct


def gameover(screen: pg.Surface, bg_img: pg.Surface) -> None:
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_img.get_rect()

    font = pg.font.Font(None, 80)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    font = pg.font.Font(None, 40)
    text2 = font.render("Press SPACE to Restart", True, (255, 255, 255))
    text_rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    kk_img = pg.image.load("fig/8.png")

    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)

    while True:
        pg.display.update()

        screen.blit(bg_img, bg_rct)
        screen.blit(overlay, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        screen.blit(kk_img, (WIDTH // 2 - 240, HEIGHT // 2 - 15))
        screen.blit(kk_img, (WIDTH // 2 + 200, HEIGHT // 2 - 15))

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    kk_img = pg.image.load("fig/3.png")
    x, y = sum_mv

    if x > 0 and y < 0: # 右上
        kk_img = pg.transform.flip(kk_img, True, False)
        kk_img = pg.transform.rotate(kk_img, 45)
    elif x > 0 and y > 0: # 右下
        kk_img = pg.transform.flip(kk_img, True, False)
        kk_img = pg.transform.rotate(kk_img, -45)
    elif x < 0 and y < 0: # 左上
        kk_img = pg.transform.rotate(kk_img, -45)
    elif x < 0 and y > 0: # 左下
        kk_img = pg.transform.rotate(kk_img, 45)
    elif x > 0:
        kk_img = pg.transform.flip(kk_img, True, False)
    elif x < 0:
        kk_img = pg.transform.flip(kk_img, False, False)
    elif y > 0:
        kk_img = pg.transform.rotate(kk_img, 90)
    elif y < 0:
        kk_img = pg.transform.rotate(kk_img, -90)

    return kk_img

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen_rct = screen.get_rect()

    bg_img = load_assets()
    vx_init, vy_init = 5, 5

    bb_accs = [i for i in range(1, 11)]

    bb_imgs = []
    for i in bb_accs:
        surface = pg.Surface((20 * i, 20 * i), pg.SRCALPHA)
        pg.draw.circle(surface, (255, 0, 0), (10 * i, 10 * i), 10 * i)
        bb_imgs.append(surface)

    clock = pg.time.Clock()
    tmr = 0

    bb_img = bb_imgs[min(tmr // 500, 9)]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = vx_init, vy_init

    while True:
        vx = (vx / abs(vx)) * vx_init * bb_accs[min(tmr // 500, 9)]
        vy = (vy / abs(vy)) * vy_init * bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr // 500, 9)]
        bb_rct = bb_img.get_rect(center=bb_rct.center)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_img = get_kk_img(sum_mv)
        if tmr == 0:
            kk_rct = initialize_objects(kk_img)

        kk_rct.move_ip(sum_mv)
        kk_rct.clamp_ip(screen_rct)
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        bound = check_bound(screen_rct, bb_rct)
        if not bound["x"]:
            vx = -vx
        if not bound["y"]:
            vy = -vy

        screen.blit(bb_img, bb_rct)

        if kk_rct.colliderect(bb_rct):
            tmr = 0

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
