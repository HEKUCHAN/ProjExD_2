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
    オブジェクトが画面内に収まっているかを判定する関数。

    画面内に収まっている場合はTrue、画面外に出ている場合はFalseを返す。

    :param scr_rct: 画面のRectオブジェクト
    :param obj_rct: 判定対象のオブジェクトのRectオブジェクト
    :return: {"x": x方向の判定結果, "y": y方向の判定結果}
    """
    return {
        "x": scr_rct.left <= obj_rct.left and obj_rct.right <= scr_rct.right,
        "y": scr_rct.top <= obj_rct.top and obj_rct.bottom <= scr_rct.bottom,
    }


def load_assets():
    """
    ゲームのアセット（画像やサーフェス）を読み込んで返す関数。
    """
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))

    return bg_img, kk_img, bb_img


def initialize_objects(kk_img, bb_img):
    """
    プレイヤーと爆弾のRectオブジェクトを初期化して返す。
    """
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)

    return kk_rct, bb_rct


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen_rct = screen.get_rect()

    bg_img, kk_img, bb_img = load_assets()
    kk_rct, bb_rct = initialize_objects(kk_img, bb_img)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
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
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
