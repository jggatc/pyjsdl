env = None
pg = None


# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_rect,
             test_rect_copy,
             test_rect_move,
             test_rect_inflate,
             test_rect_clip,
             test_rect_union,
             test_rect_collidepoint,
             test_rect_colliderect,
             test_rect_collidelist]
    return tests


def test_rect():
    #construction
    rect = pg.Rect(0,0,10,10)
    assert (rect.x,rect.y,rect.width,rect.height) == (0,0,10,10)
    rect = pg.Rect((0,0),(10,10))
    assert (rect.x,rect.y,rect.width,rect.height) == (0,0,10,10)
    rect = pg.Rect((0,0,10,10))
    assert (rect.x,rect.y,rect.width,rect.height) == (0,0,10,10)
    rect = pg.Rect(rect)
    assert (rect.x,rect.y,rect.width,rect.height) == (0,0,10,10)
    obj = pg.sprite.Sprite()
    obj.rect = rect
    rect = pg.Rect(obj)
    assert (rect.x,rect.y,rect.width,rect.height) == (0,0,10,10)
    assert (rect[0],rect[1],rect[2],rect[3]) == (0,0,10,10)
    #comparison
    rect = pg.Rect(0,0,10,10)
    if env['platform'] != 'js':
        #pyjs compares rect==tuple not __eq__
        assert rect == (0,0,10,10)
        assert rect != (0,0,100,100)
        assert not (rect == (0,0,100,100))
    if not env['pyjs_opt']:
        #pyjs -O __eq__ not called
        assert rect == pg.Rect(0,0,10,10)
        assert rect != pg.Rect(0,0,100,100)
        assert not (rect == pg.Rect(0,0,100,100))
    #get/set
    rect = pg.Rect(0,0,10,10)
    rect.x,rect.y,rect.width,rect.height = 10,10,100,100
    assert (rect.x,rect.y,rect.width,rect.height) == (10,10,100,100)
    rect[0],rect[1],rect[2],rect[3] = 20,20,200,200
    assert (rect[0],rect[1],rect[2],rect[3]) == (20,20,200,200)
    r = pg.Rect(25,25,40,40)
    r.x = 30
    assert r.x==30 and (r.x,r.y,r.width,r.height)==(30,25,40,40)
    r.y = 40
    assert r.y==40 and (r.x,r.y,r.width,r.height)==(30,40,40,40)
    r.width = 50
    assert r.width==50 and (r.x,r.y,r.width,r.height)==(30,40,50,40)
    r.height = 60
    assert r.height==60 and (r.x,r.y,r.width,r.height)==(30,40,50,60)
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        #pyjs -O __getattr__/__setattr__ not called,
        #unless --enable-descriptor-proto option.
        r = pg.Rect(25,25,40,40)
        r.center = (10,20)
        assert r.center==(10,20) and (r.x,r.y,r.width,r.height)==(-10,0,40,40)
        r.centerx = 30
        assert r.centerx==30 and (r.x,r.y,r.width,r.height)==(10,0,40,40)
        r.centery = 40
        assert r.centery==40 and (r.x,r.y,r.width,r.height)==(10,20,40,40)
        r.top = 50
        assert r.top==50 and (r.x,r.y,r.width,r.height)==(10,50,40,40)
        r.left = 60
        assert r.left==60 and (r.x,r.y,r.width,r.height)==(60,50,40,40)
        r.bottom = 70
        assert r.bottom==70 and (r.x,r.y,r.width,r.height)==(60,30,40,40)
        r.right = 80
        assert r.right==80 and (r.x,r.y,r.width,r.height)==(40,30,40,40)
        r.topleft = (90,100)
        assert r.topleft==(90,100) and (r.x,r.y,r.width,r.height)==(90,100,40,40)
        r.bottomleft = (100,110)
        assert r.bottomleft==(100,110) and (r.x,r.y,r.width,r.height)==(100,70,40,40)
        r.topright = (120,130)
        assert r.topright==(120,130) and (r.x,r.y,r.width,r.height)==(80,130,40,40)
        r.bottomright = (140,150)
        assert r.bottomright==(140,150) and (r.x,r.y,r.width,r.height)==(100,110,40,40)
        r.midtop = (160,170)
        assert r.midtop==(160,170) and (r.x,r.y,r.width,r.height)==(140,170,40,40)
        r.midleft = (180,190)
        assert r.midleft==(180,190) and (r.x,r.y,r.width,r.height)==(180,170,40,40)
        r.midbottom = (200,210)
        assert r.midbottom==(200,210) and (r.x,r.y,r.width,r.height)==(180,170,40,40)
        r.midright = (220,230)
        assert r.midright==(220,230) and (r.x,r.y,r.width,r.height)==(180,210,40,40)
        r.size = (240,250)
        assert r.size==(240,250) and (r.x,r.y,r.width,r.height)==(180,210,240,250)
        r.w = 260
        assert r.w==260 and (r.x,r.y,r.width,r.height)==(180,210,260,250)
        r.h = 270
        assert r.h==270 and (r.x,r.y,r.width,r.height)==(180,210,260,270)
    r = pg.Rect(25,25,40,40)
    setattr(r, 'center', (10,20))
    assert getattr(r, 'center')==(10,20) and (r.x,r.y,r.width,r.height)==(-10,0,40,40)


def test_rect_copy():
    r1 = pg.Rect(0,0,100,100)
    r2 = r1.copy()
    if not env['pyjs_opt']:
        #pyjs -O __eq__ not called
        assert r1 == r2
    assert (r1.x,r1.y,r1.width,r1.height) == (r2.x,r2.y,r2.width,r2.height)


def test_rect_move():
    r1 = pg.Rect(10,10,100,100)
    r2 = r1.move(10,5)
    assert (r1.x,r1.y) == (10,10) and (r2.x,r2.y) == (20,15)
    r1 = pg.Rect(10,10,100,100)
    r2 = r1.move((10,5))
    assert (r1.x,r1.y) == (10,10) and (r2.x,r2.y) == (20,15)
    r = pg.Rect(10,10,100,100)
    r.move_ip(10,5)
    assert (r.x,r.y) == (20,15)
    r = pg.Rect(10,10,100,100)
    r.move_ip((10,5))
    assert (r.x,r.y) == (20,15)


def test_rect_inflate():
    r1 = pg.Rect(10,10,100,100)
    r2 = r1.inflate(10,20)
    assert (r1.width,r1.height) == (100,100) and (r2.width,r2.height) == (110,120)
    assert (r1.x,r1.y) == (10,10) and (r2.x,r2.y) == (5,0)
    r1 = pg.Rect(10,10,100,100)
    r2 = r1.inflate(-10,-20)
    assert (r1.width,r1.height) == (100,100) and (r2.width,r2.height) == (90,80)
    assert (r1.x,r1.y) == (10,10) and (r2.x,r2.y) == (15,20)
    r1 = pg.Rect(10,10,100,100)
    r2 = r1.inflate((10,20))
    assert (r1.width,r1.height) == (100,100) and (r2.width,r2.height) == (110,120)
    assert (r1.x,r1.y) == (10,10) and (r2.x,r2.y) == (5,0)
    r = pg.Rect(10,10,100,100)
    r.inflate_ip(10,20)
    assert (r.width,r.height) == (110,120)
    assert (r.x,r.y) == (5,0)
    r = pg.Rect(10,10,100,100)
    r.inflate_ip(-10,-20)
    assert (r.width,r.height) == (90,80)
    assert (r.x,r.y) == (15,20)
    r = pg.Rect(10,10,100,100)
    r.inflate_ip((10,20))
    assert (r.width,r.height) == (110,120)
    assert (r.x,r.y) == (5,0)


def test_rect_clip():
    r1 = pg.Rect(0,0,100,150)
    r2 = pg.Rect(50,50,100,150)
    r3 = pg.Rect(200,200,50,100)
    r = r1.clip(r2)
    assert (r.x,r.y,r.width,r.height) == (50,50,50,100)
    r = r1.clip(r3)
    assert (r.x,r.y,r.width,r.height) == (0,0,0,0)


def test_rect_union():
    r1 = pg.Rect(0,0,100,150)
    r2 = pg.Rect(50,50,100,150)
    r3 = pg.Rect(200,200,50,100)
    r4 = pg.Rect(-10,-10,50,100)
    r = r1.union(r2)
    assert (r.x,r.y,r.width,r.height) == (0,0,150,200)
    r = r1.copy()
    r.union_ip(r2)
    assert (r.x,r.y,r.width,r.height) == (0,0,150,200)
    r = r1.unionall([r2,r3,r4])
    assert (r.x,r.y,r.width,r.height) == (-10, -10, 260, 310)
    r = r1.copy()
    r.unionall_ip([r2,r3,r4])
    assert (r.x,r.y,r.width,r.height) == (-10, -10, 260, 310)


def test_rect_collidepoint():
    r = pg.Rect(10,20,100,200)
    assert r.collidepoint((30,40)) == True
    assert r.collidepoint(50,60) == True
    assert r.collidepoint((5,5)) == False


def test_rect_colliderect():
    r1 = pg.Rect(0,0,100,150)
    r2 = pg.Rect(50,50,100,150)
    r3 = pg.Rect(200,200,50,100)
    assert r1.colliderect(r2) == True
    assert r1.colliderect(r3) == False


def test_rect_collidelist():
    r1 = pg.Rect(0,0,100,150)
    r2 = pg.Rect(50,50,100,150)
    r3 = pg.Rect(200,200,50,100)
    r4 = pg.Rect(75,80,50,50)
    assert r1.collidelist([r2,r3,r4]) == 0
    assert r1.collidelist([r3,r4,r2]) == 1
    assert r1.collidelist([r3]) == -1

