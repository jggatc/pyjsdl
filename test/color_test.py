env = None
pg = None

# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_color]
    return tests


def _color_convert(color):
    if isinstance(color,tuple):
        if len(color) == 4:
            r,g,b,a = color[0],color[1],color[2],color[3]
        else:
            r,g,b,a = color[0],color[1],color[2],255
    else:
        r,g,b,a = int((color>>16) & 0xff), int((color>>8) & 0xff), int(color & 0xff), int((color>>24) & 0xff)
    return r,g,b,a


def test_color():
    #construct
    c = pg.Color(255,0,0)
    r,g,b,a = _color_convert((255,0,0))
    assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    c = pg.Color(0,255,0,255)
    r,g,b,a = _color_convert((0,255,0,255))
    assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    if env['platform'] in ('jvm', 'js'):    #pg error?
        c = pg.Color((0xff<<24)+255)
        r,g,b,a = _color_convert((0xff<<24)+255)
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    if env['platform'] == 'jvm':
        c = pg.Color((255,0,0))
        r,g,b,a = _color_convert((255,0,0))
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
        c = pg.Color((0,255,0,255))
        r,g,b,a = _color_convert((0,255,0,255))
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    #get/set
    c = pg.Color(0,255,0,255)
    r,g,b,a = 0,255,0,255
    assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    assert (c[0],c[1],c[2],c[3]) == (r,g,b,a)
    if env['platform'] == 'jvm':   #java.awt.Color
        assert (c.getRed(),c.getGreen(),c.getBlue(),c.getAlpha()) == (r,g,b,a)
    try:
        c[0] = 10
        c.g = 20
        assert (c.r,c.g,c.b,c.a) == (10,20,b,a)
        assert (c[0],c[1],c[2],c[3]) == (10,20,b,a)
        if env['platform'] == 'jvm':   #java.awt.Color
            assert (c.getRed(),c.getGreen(),c.getBlue(),c.getAlpha()) == (10,20,b,a)
    except:     #jy2.2.1
        import sys
        if not (env['platform'] == 'jvm' and sys.version_info[1] < 5):
            raise
    #comparison
    c = pg.Color(255,0,0,255)
    c1 = pg.Color(255,0,0,255)
    c2 = pg.Color(0,0,0,255)
    c3 = pg.Color(255,0,0)
    c4 = pg.Color(0,0,0)
    if env['executor'] != 'pyjs':
        #pyjs compares rect==tuple not __eq__
        assert c == (255,0,0,255)
        assert c != (0,0,0,255)
        assert c == (255,0,0)
        assert c != (0,0,0)
    if not env['pyjs_opt']:
        #pyjs -O __eq__ ignored
        assert c == c1
        assert c != c2
        assert c == c3
        assert c != c4
    assert c.r==c1.r and c.g==c1.g and c.b==c1.b and c.a==c1.a
    assert c.r!=c2.r and c.g==c2.g and c.b==c2.b and c.a==c2.a
    assert c.r==c3.r and c.g==c3.g and c.b==c3.b and c.a==c3.a
    assert c.r!=c4.r and c.g==c4.g and c.b==c4.b and c.a==c4.a

