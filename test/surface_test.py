env = None
pg = None
surface = None
width = None
height = None


# __pragma__ ('opov')


def init(environ):
    global env, pg, surface, width, height
    env = environ
    pg = env['pg']
    surface = env['surface']
    width = env['width']
    height = env['height']
    tests = [test_surface_get_size,
             test_surface_get_rect,
             test_surface_copy,
             test_surface_blit,
             test_surface_fill,
             test_surface_set_colorkey,
             test_surface_get_colorkey,
             test_surface_set_at,
             test_surface_get_at]
    return tests


def _color_convert(color):
    if len(color) == 4:
        r,g,b,a = color[0],color[1],color[2],color[3]
    else:
        r,g,b,a = color[0],color[1],color[2],255
    return r,g,b,a


def test_surface_get_size():
    assert surface.get_size() == (width,height)
    assert surface.get_width() == width
    assert surface.get_height() == height


def test_surface_get_rect():
    rect = surface.get_rect()
    if env['platform'] != 'js':    #pyjs compares rect==tuple not __eq__
        assert rect == (0,0,width,height)
    assert (rect.x,rect.y,rect.width,rect.height) == (0,0,width,height)
    rect = surface.get_rect(center=(15,15))
    assert (rect.x,rect.y,rect.width,rect.height) == (5,5,width,height)


def test_surface_copy():
    new_surface = surface.copy()
    assert surface == surface
    assert surface != new_surface
    assert surface.get_size() == new_surface.get_size()


def test_surface_blit():
    new_surface = pg.Surface((5,5))
    surface.fill((0,0,0))
    new_surface.fill((100,100,100))
    rect = surface.blit(new_surface, (1,0))
    if env['executor'] != 'pyjs':
        assert surface.get_at((0,0)) == (0,0,0,255)
        assert surface.get_at((1,0)) == (100,100,100,255)
    else:
        if not env['pyjs_opt']:   #pyjs -s compares color==tuple not __eq__ 
            assert surface.get_at((0,0)) == pg.Color(0,0,0,255)
            assert surface.get_at((1,0)) == pg.Color(100,100,100,255)
        else:   #pyjs -O __eq__ ignored
            c = surface.get_at((0,0))
            assert (c.r,c.g,c.b,c.a) == (0,0,0,255)
            c = surface.get_at((1,0))
            assert (c.r,c.g,c.b,c.a) == (100,100,100,255)
    assert (rect.x,rect.y,rect.width,rect.height) == (1,0,5,5)


def test_surface_fill():
    color = (255,0,0), (0,255,0,255)
    for c in color:
        surface.fill((0,0,0))
        surface.fill(pg.Color(c))
        if env['executor'] != 'pyjs':
            assert surface.get_at((0,0)) == c
        else:
            cc = surface.get_at((0,0))
            assert (cc[0],cc[1],cc[2],cc[3]) == _color_convert(c)


def test_surface_set_colorkey():
    color = (255,0,0), (0,255,0,255), None
    for c in color:
        surface.set_colorkey(c)
        if surface.get_colorkey():
            if not env['pyjs_opt']:
                assert pg.Color(*surface.get_colorkey()) == pg.Color(*c)
            else:   #pyjs -O no __eq__ call
                r,g,b,a = pg.Color(*surface.get_colorkey())
                cr,cg,cb,ca = pg.Color(*c)
                assert r==cr and g==cg and b==cb and a==ca


def test_surface_get_colorkey():
    surface.fill((0,0,0))
    surface.set_colorkey((0,0,0))
    assert surface.get_colorkey() == (0,0,0,255)
    surface.set_colorkey(None)
    assert surface.get_colorkey() is None


def test_surface_set_at():
    color = (255,0,0), (0,255,0,255)
    for c in color:
        surface.fill((0,0,0))
        surface.set_at((0,0), c)
        if env['executor'] != 'pyjs':
            assert surface.get_at((0,0)) == c
        else:   #pyjs compares color==tuple not __eq__
            cc = surface.get_at((0,0))
            assert (cc.r,cc.g,cc.b,cc.a) == _color_convert(c)


def test_surface_get_at():
    color = (0,0,255,255)
    surface.fill((0,0,0))
    surface.set_at((0,0), (0,0,255,255))
    if env['executor'] != 'pyjs':
        assert surface.get_at((0,0)) == (0,0,255,255)
        assert surface.get_at((0,0)) == (0,0,255)
    else:   #pyjs compares color==tuple not __eq__
        cc = surface.get_at((0,0))
        assert (cc.r,cc.g,cc.b,cc.a) == (0,0,255,255)

