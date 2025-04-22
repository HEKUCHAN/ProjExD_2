import math
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
    """
    複数の画像を読み込む関数。
    """
    bg_img = pg.image.load("fig/pg_bg.jpg")

    return bg_img


def initialize_random_object(img: pg.Surface) -> pg.Rect:
    """
    画像をランダムな位置に配置する関数。
    """
    kk_rct = img.get_rect()
    kk_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    return kk_rct


def gameover(screen: pg.Surface, bg_img: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数。

    画面を黒く塗りつぶし、"GAME OVER"と"Press SPACE to Restart"のテキストを表示する。
    """
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_img.get_rect()

    # ゲームオーバータイトル
    font = pg.font.Font(None, 80)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # リスタート方法の説明 😺
    font = pg.font.Font(None, 40)
    text2 = font.render("Press SPACE to Restart", True, (255, 255, 255))
    text_rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    # こうかとんの画像を読み込む
    kk_img = pg.image.load("fig/8.png")

    # 画面を黒く塗りつぶす（薄い）
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)

    while True:
        pg.display.update()

        # 画面を黒く塗りつぶす
        screen.blit(bg_img, bg_rct)
        screen.blit(overlay, (0, 0))
        # 画面の中央にテキストを表示
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        # こうかとんの画像を表示
        screen.blit(kk_img, (WIDTH // 2 - 240, HEIGHT // 2 - 15))
        screen.blit(kk_img, (WIDTH // 2 + 200, HEIGHT // 2 - 15))

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    こうかとんの画像を取得する関数。
    移動方向に応じて画像を回転させる。
    """
    kk_img = pg.image.load("fig/3.png")
    x, y = sum_mv

    if x > 0 and y < 0:  # 右上
        kk_img = pg.transform.flip(kk_img, True, False)
        kk_img = pg.transform.rotate(kk_img, 45)
    elif x > 0 and y > 0:  # 右下
        kk_img = pg.transform.flip(kk_img, True, False)
        kk_img = pg.transform.rotate(kk_img, -45)
    elif x < 0 and y < 0:  # 左上
        kk_img = pg.transform.rotate(kk_img, -45)
    elif x < 0 and y > 0:  # 左下
        kk_img = pg.transform.rotate(kk_img, 45)
    elif x > 0:  # 右
        kk_img = pg.transform.flip(kk_img, True, False)
    elif x < 0:  # 左
        kk_img = pg.transform.flip(kk_img, False, False)
    elif y > 0:  # 下
        kk_img = pg.transform.rotate(kk_img, 90)
    elif y < 0:  # 上
        kk_img = pg.transform.rotate(kk_img, -90)

    return kk_img


def vector_diff(rect1: pg.Rect, rect2: pg.Rect) -> tuple[int, int]:
    """
    サーフェース間のベクトル差を計算する関数。

    surface1とsurface2の中心座標を取得し、その差を計算して返す。
    """
    center1 = rect1.center
    center2 = rect2.center

    return (center1[0] - center2[0], center1[1] - center2[1])


def verctor_norm(vector: tuple[int, int]) -> float:
    """
    ベクトルの大きさを計算する関数。

    vectorのx成分とy成分を取得し、ピタゴラスの定理を使って大きさを計算して返す。
    """
    return (vector[0] ** 2 + vector[1] ** 2) ** 0.5


def main():
    """
    ゲームのメイン関数。
    """
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen_rct = screen.get_rect()

    # 背景画像の読み込み
    bg_img = load_assets()
    # 加速値の初期値
    vx_init, vy_init = 5, 5

    # 爆弾の加速値を格納するリスト
    bb_accs = [i for i in range(1, 11)]

    # 爆弾の画像を格納するリスト
    bb_imgs = []
    for i in bb_accs:
        surface = pg.Surface((20 * i, 20 * i), pg.SRCALPHA)
        pg.draw.circle(surface, (255, 0, 0), (10 * i, 10 * i), 10 * i)
        bb_imgs.append(surface)

    clock = pg.time.Clock()
    tmr = 0

    bb_img = bb_imgs[min(tmr // 500, 9)]
    bb_rct = initialize_random_object(bb_img)
    vx, vy = vx_init, vy_init
    last_vx, last_vy = vx_init, vy_init

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
            kk_rct = initialize_random_object(kk_img)

        # こうかとんの表示、移動
        kk_rct.move_ip(sum_mv)
        kk_rct.clamp_ip(screen_rct)
        screen.blit(kk_img, kk_rct)

        # bb_rct.move_ip(vx, vy)
        bound = check_bound(screen_rct, bb_rct)
        if not bound["x"]:
            vx = -vx
        if not bound["y"]:
            vy = -vy

        # ベクトル差を計算する
        distance_kouka_bb = vector_diff(kk_rct, bb_rct)
        # ベクトルのノルムを計算
        distance_norm = verctor_norm(distance_kouka_bb)
        if distance_norm < 300:
            bb_rct.move_ip(last_vx, last_vy)
        else:
            vx = distance_kouka_bb[0] * (math.sqrt(50) / distance_norm)
            vy = distance_kouka_bb[1] * (math.sqrt(50) / distance_norm)
            bb_rct.move_ip(vx, vy)
            last_vx, last_vy = vx, vy
        screen.blit(bb_img, bb_rct)

        # こうかとんと爆弾が衝突した時
        if kk_rct.colliderect(bb_rct):
            gameover(screen, bg_img)
            kk_rct = initialize_random_object(kk_img)
            tmr = 0

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
