import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate =True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    #画面をブラックアウトさせる
    bo = pg.Surface((WIDTH, HEIGHT)) #黒いSurfaceを生成
    pg.draw.rect(bo, (0, 0, 0), [0, 0, WIDTH, HEIGHT]) #画面を真っ黒にする
    bo.set_alpha(128) #透明度を指定
    screen.blit(bo, [0, 0]) #画面にブラックアウトを描画
    #Game Overの文字を描画
    font = pg.font.Font(None, 100) #フォントを生成
    text = font.render("Game Over", True, (255, 255, 255)) #テキストを生成
    screen.blit(text, [WIDTH//2-200, HEIGHT//2-50]) #テキストを描画
    #gameoverの文字の両脇に画像を配置
    #画像を描画
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)  # 工科トン読み込み
    screen.blit(kk_img, [WIDTH//2-200-50, HEIGHT//2-50])  # 工科とん描画
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(kk_img, [WIDTH//2+190, HEIGHT//2-50])

    pg.display.update() #画面を更新
    time.sleep(5) #5秒待つ
    return

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 20
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤円描く
    bb_img.set_colorkey((0, 0, 0))  # 爆弾四隅消す
    bb_rct = bb_img.get_rect()  # 爆弾rectセット
    bb_rct.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
