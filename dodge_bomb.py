import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0 , -5),  # 上
    pg.K_DOWN: (0 , +5),  # 下
    pg.K_LEFT: (-5, 0),  # 左
    pg.K_RIGHT: (+5, 0),  # 右
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    画面の範囲の判定
    引数: コウカトンのRect or 爆弾Rect
    戻り値: X , Y XYの判定結果(True: 画面内, Falise: 画面内) 
    """
    x , y = True, True
    if rct.left < 0 or WIDTH < rct.right:#横方向がこえるときの判定
        x = False
    if rct.top < 0 or HEIGHT < rct.bottom:#縦方向を超える時の判定
        y = False
    return x , y

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200


    bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 爆弾の黒い部分を透過させる
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得する
    bb_rct.center = random.randint(0, WIDTH),random.randint(0, HEIGHT)  # 爆弾の初期横座標を設定する
    vx, vy = +5, +5  # 爆弾の速度


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        """
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        """
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):#壁にぶつかった時に停止(マイナスで打ち消し)
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾の移動処理
        screen.blit(bb_img, bb_rct)  # 爆弾を表示
        x , y=check_bound(bb_rct)
        if not x:
            vx *= -1
        if not y:
            vy *= -1
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()