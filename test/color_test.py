import sys

env = None
pg = None

# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_color_constructor,
             test_color_update,
             test_color_get,
             test_color_comparison,
             test_color_operator,
             test_color_transform,
             test_color_conversion]
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


def _attr(color):
    return color.r, color.g, color.b, color.a


def _rd(v1,v2,v3,v4=None):
    if v4 is None:
        return round(v1,3), round(v2,3), round(v3,3)
    else:
        return round(v1,3), round(v2,3), round(v3,3), round(v4,3)


def test_color_constructor():
    c = pg.Color(255,0,0)
    r,g,b,a = _color_convert((255,0,0))
    assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    c = pg.Color(0,255,0,255)
    r,g,b,a = _color_convert((0,255,0,255))
    assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    if env['platform'] in ('jvm', 'js'):    #pg: integer is rgba, not argb
        c = pg.Color((0xff<<24)+255)
        r,g,b,a = _color_convert((0xff<<24)+255)
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    if env['platform'] in ['jvm', 'pc']:
        c = pg.Color((255,0,0))
        r,g,b,a = _color_convert((255,0,0))
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
        c = pg.Color((0,255,0,255))
        r,g,b,a = _color_convert((0,255,0,255))
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    c = pg.Color('0xff0000')
    assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    c = pg.Color('0xff0000ff')
    assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    c = pg.Color('#ff0000')
    assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    c = pg.Color('#ff0000ff')
    assert (c.r,c.g,c.b,c.a) == (255,0,0,255)


def test_color_update():
    c = pg.Color(0,0,0)
    c.update(255,0,0)
    r,g,b,a = _color_convert((255,0,0))
    assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    c.update(0,255,0,255)
    r,g,b,a = _color_convert((0,255,0,255))
    assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    if env['platform'] in ('jvm', 'js'):    #pg: integer is rgba, not argb
        c.update((0xff<<24)+255)
        r,g,b,a = _color_convert((0xff<<24)+255)
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    if env['platform'] in ['jvm', 'pc']:
        c.update((255,0,0))
        r,g,b,a = _color_convert((255,0,0))
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
        c.update((0,255,0,255))
        r,g,b,a = _color_convert((0,255,0,255))
        assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    c = pg.Color('0xff0000')
    assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    c = pg.Color('0xff0000ff')
    assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    c = pg.Color('#ff0000')
    assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    c = pg.Color('#ff0000ff')
    assert (c.r,c.g,c.b,c.a) == (255,0,0,255)


def test_color_get():
    c = pg.Color(0,255,0,255)
    r,g,b,a = 0,255,0,255
    assert (c.r,c.g,c.b,c.a) == (r,g,b,a)
    assert (c[0],c[1],c[2],c[3]) == (r,g,b,a)
    if env['platform'] == 'jvm':   #java.awt.Color
        assert (c.getRed(),c.getGreen(),c.getBlue(),c.getAlpha()) == (r,g,b,a)
    if not (env['platform'] == 'jvm' and sys.version_info[1] < 5):
        #jy2.2.1 issue with property assignment
        c[0] = 10
        c.g = 20
        assert (c.r,c.g,c.b,c.a) == (10,20,b,a)
        assert (c[0],c[1],c[2],c[3]) == (10,20,b,a)
        if env['platform'] == 'jvm':   #java.awt.Color
            assert (c.getRed(),c.getGreen(),c.getBlue(),c.getAlpha()) == (10,20,b,a)
    c = pg.Color(50,100,150,200)
    for i, _c in enumerate(c):
        assert _c == {0:50, 1:100, 2:150, 3:200}[i]
    assert [_c for _c in c] == [50,100,150,200]


def test_color_comparison():
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
        assert c == pg.Color(255,0,0,255)
        assert c != pg.Color(0,0,0,255)
        assert c == pg.Color(255,0,0)
        assert c != pg.Color(0,0,0)
        assert c == c1
        assert c != c2
        assert c == c3
        assert c != c4
    assert c.r==c1.r and c.g==c1.g and c.b==c1.b and c.a==c1.a
    assert c.r!=c2.r and c.g==c2.g and c.b==c2.b and c.a==c2.a
    assert c.r==c3.r and c.g==c3.g and c.b==c3.b and c.a==c3.a
    assert c.r!=c4.r and c.g==c4.g and c.b==c4.b and c.a==c4.a


def test_color_operator():
    if (env['pyjs_opt'] and not env['pyjs_attr']):    #special methods ignored
        raise NotImplementedError
    if not env['pyjs_opt']:
        c1 = pg.Color(60,220,120,100)
        c2 = pg.Color(40,40,40,255)
        c3 = pg.Color(255,0,0,100)
        assert c1 + c2 == pg.Color(100,255,160,255)
        assert c1 + c3 == pg.Color(255,220,120,200)
        assert c1 - c2 == pg.Color(20,180,80,0)
        assert c1 - c3 == pg.Color(0,220,120,0)
        assert c1 * c2 == pg.Color(255,255,255,255)
        assert c1 * c3 == pg.Color(255,0,0,255)
        assert c1 // c2 == pg.Color(1,5,3,0)
        assert c1 // c3 == pg.Color(0,0,0,1)
        assert c1 % c2 == pg.Color(20,20,0,100)
        assert c1 % c3 == pg.Color(60,0,0,0)
        c = pg.Color(0,10,20,255)
        c += c1
        assert c == pg.Color(60,230,140,255)
        c = pg.Color(0,10,20,255)
        c -= c1
        assert c == pg.Color(0,0,0,155)
        c = pg.Color(0,10,20,255)
        c *= c1
        assert c == pg.Color(0,255,255,255)
        c = pg.Color(0,10,20,255)
        if not (env['platform'] == 'js'
                and env['executor'] == 'transcrypt'):
            #ts compiles //=, but bad js script, requires the skip pragma.
            # __pragma__ ('skip')
            c //= c1
            # __pragma__ ('noskip')
        else:
            c.__ifloordiv__(c1)
        assert c == pg.Color(0,0,0,2)
        c = pg.Color(0,10,20,255)
        c %= c1
        assert c == pg.Color(0,10,20,55)
        c = pg.Color(0,10,20,255)
        if not (env['platform'] == 'js'
                and env['executor'] == 'transcrypt'):    #ts error with ~
            assert ~c == pg.Color(255,245,235,0)
        else:
            assert c.__invert__() == pg.Color(255,245,235,0)
    if (env['pyjs_opt'] and env['pyjs_attr']):
        c1 = pg.Color(60,220,120,100)
        c2 = pg.Color(40,40,40,255)
        c3 = pg.Color(255,0,0,100)
        assert _attr(c1 + c2) == (100,255,160,255)
        assert _attr(c1 + c3) == (255,220,120,200)
        assert _attr(c1 - c2) == (20,180,80,0)
        assert _attr(c1 - c3) == (0,220,120,0)
        assert _attr(c1 * c2) == (255,255,255,255)
        assert _attr(c1 * c3) == (255,0,0,255)
        assert _attr(c1 // c2) == (1,5,3,0)
        assert _attr(c1 // c3) == (0,0,0,1)
        assert _attr(c1 % c2) == (20,20,0,100)
        assert _attr(c1 % c3) == (60,0,0,0)
        c = pg.Color(0,10,20,255)
        c += c1
        assert _attr(c) == (60,230,140,255)
        c = pg.Color(0,10,20,255)
        c -= c1
        assert _attr(c) == (0,0,0,155)
        c = pg.Color(0,10,20,255)
        c *= c1
        assert _attr(c) == (0,255,255,255)
        c = pg.Color(0,10,20,255)
        if not (env['platform'] == 'js'
                and env['executor'] == 'transcrypt'):
            #ts compiles //=, but bad js script, requires the skip pragma.
            # __pragma__ ('skip')
            c //= c1
            # __pragma__ ('noskip')
        else:
            c.__ifloordiv__(c1)
        assert _attr(c) == (0,0,0,2)
        c = pg.Color(0,10,20,255)
        c %= c1
        assert _attr(c) == (0,10,20,55)
        c = pg.Color(0,10,20,255)
        assert _attr(c.__invert__()) == (255,245,235,0)    #pyjs -O error with ~


def test_color_transform():
    if not env['pyjs_opt']:
        c = pg.Color(0, 10, 100, 100)
        nr,ng,nb,na = c.normalize()
        assert (_rd( nr,ng,nb,na )) == (0.0, 0.039, 0.392, 0.392)
        c = pg.Color(255, 0, 100, 150)
        nc = c.normalize()
        nr,ng,nb,na = nc
        assert (_rd( nr,ng,nb,na )) == (1.0, 0.0, 0.392, 0.588)
        c = pg.Color(0, 10, 100, 100)
        assert c.premul_alpha() == pg.Color(0,4,39,100)
        c = pg.Color(255, 0, 100, 150)
        assert c.premul_alpha() == pg.Color(150,0,59,150)
        c = pg.Color(0, 10, 100, 100)
        assert c.correct_gamma(0.1) == pg.Color(0,184,232,232)
        assert c.correct_gamma(0.9) == pg.Color(0,14,110,110)
        assert c.correct_gamma(2.0) == pg.Color(0,0,39,39)
        c = pg.Color(255, 0, 100, 150)
        assert c.correct_gamma(0.1) == pg.Color(255,0,232,242)
        assert c.correct_gamma(0.9) == pg.Color(255,0,110,158)
        assert c.correct_gamma(2.0) == pg.Color(255,0,39,88)
        c1 = pg.Color(0, 10, 100, 100)
        c2 = pg.Color(0, 20, 200, 100)
        assert c1.lerp(c2, 0.0) == pg.Color(0, 10, 100, 100)
        assert c1.lerp(c2, 0.3) == pg.Color(0, 13, 130, 100)
        assert c1.lerp(c2, 0.5) == pg.Color(0, 15, 150, 100)
        assert c1.lerp(c2, 0.7) == pg.Color(0, 17, 170, 100)
        assert c1.lerp(c2, 1.0) == pg.Color(0, 20, 200, 100)
        c1 = pg.Color(50, 100, 150, 100)
        c2 = pg.Color(100,200,250,200)
        assert c1.lerp(c2, 0.0) == pg.Color(50, 100, 150, 100)
        assert c1.lerp(c2, 0.3) == pg.Color(65, 130, 180, 130)
        assert c1.lerp(c2, 0.5) == pg.Color(75, 150, 200, 150)
        assert c1.lerp(c2, 0.7) == pg.Color(85, 170, 220, 170)
        assert c1.lerp(c2, 1.0) == pg.Color(100, 200, 250, 200)
        c1 = pg.Color(255,0,100,150)
        c2 = (50,100,150,200)
        if not (env['platform'] == 'js'
                and env['executor'] == 'transcrypt'):    #python round 0.5 to even
            assert c1.lerp(c2, 0.5) == pg.Color(153, 50, 125, 175)
        else:
            assert c1.lerp(c2, 0.5) == pg.Color(152, 50, 125, 175)
        c1 = pg.Color(255,0,100,150)
        c2 = (50,100,150)
        if not (env['platform'] == 'js'
                and env['executor'] == 'transcrypt'):    #python round 0.5 to even
            assert c1.lerp(c2, 0.5) == pg.Color(153, 50, 125, 203)
        else:
            assert c1.lerp(c2, 0.5) == pg.Color(152, 50, 125, 202)
    if (env['pyjs_opt'] and env['pyjs_attr']):
        c = pg.Color(0, 10, 100, 100)
        nr,ng,nb,na = c.normalize()
        assert (_rd( nr,ng,nb,na )) == (0.0, 0.039, 0.392, 0.392)
        c = pg.Color(255, 0, 100, 150)
        nc = c.normalize()
        nr,ng,nb,na = nc
        assert (_rd( nr,ng,nb,na )) == (1.0, 0.0, 0.392, 0.588)
        c = pg.Color(0, 10, 100, 100)
        assert _attr(c.premul_alpha()) == (0,4,39,100)
        c = pg.Color(255, 0, 100, 150)
        assert _attr(c.premul_alpha()) == (150,0,59,150)
        c = pg.Color(0, 10, 100, 100)
        assert _attr(c.correct_gamma(0.1)) == (0,184,232,232)
        assert _attr(c.correct_gamma(0.9)) == (0,14,110,110)
        assert _attr(c.correct_gamma(2.0)) == (0,0,39,39)
        c = pg.Color(255, 0, 100, 150)
        assert _attr(c.correct_gamma(0.1)) == (255,0,232,242)
        assert _attr(c.correct_gamma(0.9)) == (255,0,110,158)
        assert _attr(c.correct_gamma(2.0)) == (255,0,39,88)
        c1 = pg.Color(0, 10, 100, 100)
        c2 = pg.Color(0, 20, 200, 100)
        assert _attr(c1.lerp(c2, 0.0)) == (0, 10, 100, 100)
        assert _attr(c1.lerp(c2, 0.3)) == (0, 13, 130, 100)
        assert _attr(c1.lerp(c2, 0.5)) == (0, 15, 150, 100)
        assert _attr(c1.lerp(c2, 0.7)) == (0, 17, 170, 100)
        assert _attr(c1.lerp(c2, 1.0)) == (0, 20, 200, 100)
        c1 = pg.Color(50, 100, 150, 100)
        c2 = pg.Color(100,200,250,200)
        assert _attr(c1.lerp(c2, 0.0)) == (50, 100, 150, 100)
        assert _attr(c1.lerp(c2, 0.3)) == (65, 130, 180, 130)
        assert _attr(c1.lerp(c2, 0.5)) == (75, 150, 200, 150)
        assert _attr(c1.lerp(c2, 0.7)) == (85, 170, 220, 170)
        assert _attr(c1.lerp(c2, 1.0)) == (100, 200, 250, 200)
        c1 = pg.Color(255,0,100,150)
        c2 = (50,100,150,200)
        if not (env['platform'] == 'js'
                and env['executor'] == 'transcrypt'):    #python round 0.5 to even
            assert _attr(c1.lerp(c2, 0.5)) == (153, 50, 125, 175)
        else:
            assert _attr(c1.lerp(c2, 0.5)) == (152, 50, 125, 175)
        c1 = pg.Color(255,0,100,150)
        c2 = (50,100,150)
        if not (env['platform'] == 'js'
                and env['executor'] == 'transcrypt'):    #python round 0.5 to even
            assert _attr(c1.lerp(c2, 0.5)) == (153, 50, 125, 203)
        else:
            assert _attr(c1.lerp(c2, 0.5)) == (152, 50, 125, 202)

def test_color_conversion():
    if (env['pyjs_opt'] and not env['pyjs_attr']):    #property ignored
        c = pg.Color(255,0,0)
        assert _attr(c) == (255,0,0,255)
        assert c._get_cmy() == (0.0, 1.0, 1.0)
        assert c._get_hsva() == (0.0, 100.0, 100.0, 100.0)
        assert c._get_hsla() == (0.0, 100.0, 50.0, 100.0)
        c._set_cmy((0.1, 0.2, 0.3))
        _c,_m,_y = c._get_cmy()
        assert (_rd( _c,_m,_y )) == (0.102, 0.2, 0.302)
        assert _attr(c) == (229, 204, 178, 255)
        c._set_hsva((360.0, 100.0, 100.0, 100.0))
        assert c._get_hsva() == (0.0, 100.0, 100.0, 100.0)
        assert _attr(c) == (255,0,0,255)
        c._set_hsla((50.0, 50.0, 50.0, 50.0))
        h,s,l,a = c._get_hsla()
        assert (_rd( h,s,l,a )) == (50.156, 50.394, 49.804, 49.804)
        assert _attr(c) == (191,170,63,127)
        return
    c = pg.Color(255,0,0)
    if not env['pyjs_opt']:
        assert c == pg.Color(255,0,0,255)
    else:
        assert _attr(c) == (255,0,0,255)
    assert c.cmy == (0.0, 1.0, 1.0)
    assert c.hsva == (0.0, 100.0, 100.0, 100.0)
    assert c.hsla == (0.0, 100.0, 50.0, 100.0)
    c = pg.Color(10, 100, 200, 200)
    _c,_m,_y = c.cmy
    assert (_rd( _c,_m,_y )) == (0.961, 0.608, 0.216)
    h,s,v,a = c.hsva
    assert (_rd( h,s,v,a )) == (211.579, 95.0, 78.431, 78.431)
    h,s,l,a = c.hsla
    assert (_rd( h,s,l,a )) == (211.579, 90.476, 41.176, 78.431)
    if env['platform'] == 'jvm' and sys.version_info < (2,5):
        #jy2.2.1 issue with property assignment
        return
    c = pg.Color(255,0,0)
    assert c.cmy == (0.0, 1.0, 1.0)
    c.cmy = (0.1, 0.2, 0.3)
    _c,_m,_y = c.cmy
    assert (_rd( _c,_m,_y )) == (0.102, 0.2, 0.302)
    if not env['pyjs_opt']:
        assert c == pg.Color(229, 204, 178, 255)
    else:
        assert _attr(c) == (229, 204, 178, 255)
    c.cmy = (0.5, 0.5, 0.5)
    _c,_m,_y = c.cmy
    assert (_rd( _c,_m,_y )) == (0.502, 0.502, 0.502)
    if not env['pyjs_opt']:
        assert c == pg.Color(127, 127, 127, 255)
    else:
        assert _attr(c) == (127, 127, 127, 255)
    c.cmy = (0.0, 0.5, 1.0)
    _c,_m,_y = c.cmy
    assert (_rd( _c,_m,_y )) == (0.0, 0.502, 1.0)
    if not env['pyjs_opt']:
        assert c == pg.Color(255, 127, 0, 255)
    else:
        assert _attr(c) == (255, 127, 0, 255)
    c = pg.Color(255,0,0)
    assert c.hsva == (0.0, 100.0, 100.0, 100.0)
    c.hsva = (360.0, 100.0, 100.0, 100.0)
    assert c.hsva == (0.0, 100.0, 100.0, 100.0)
    if not env['pyjs_opt']:
        assert c == pg.Color(255,0,0,255)
    else:
        assert _attr(c) == (255,0,0,255)
    c.hsva = (60.0, 100.0, 100.0, 100.0)
    assert c.hsva == (60.0, 100.0, 100.0, 100.0)
    if not env['pyjs_opt']:
        assert c == pg.Color(255,255,0,255)
    else:
        assert _attr(c) == (255,255,0,255)
    c.hsva = (120.0, 100.0, 100.0, 100.0)
    assert c.hsva == (120.0, 100.0, 100.0, 100.0)
    if not env['pyjs_opt']:
        assert c == pg.Color(0,255,0,255)
    else:
        assert _attr(c) == (0,255,0,255)
    c.hsva = (0.0, 0.0, 0.0, 100.0)
    assert c.hsva == (0.0, 0.0, 0.0, 100.0)
    if not env['pyjs_opt']:
        assert c == pg.Color(0,0,0,255)
    else:
        assert _attr(c) == (0,0,0,255)
    c.hsva = (10.0, 100.0, 100.0, 100.0)
    h,s,v,a = c.hsva
    assert (_rd( h,s,v,a )) == (9.882, 100.0, 100.0, 100.0)
    if not env['pyjs_opt']:
        assert c == pg.Color(255,42,0,255)
    else:
        assert _attr(c) == (255,42,0,255)
    c = pg.Color(255,0,0)
    assert c.hsla == (0.0, 100.0, 50.0, 100.0)
    c.hsla = (360.0, 100.0, 100.0, 100.0)
    assert c.hsla == (0.0, 0.0, 100.0, 100.0)
    if not env['pyjs_opt']:
        assert c == pg.Color(255,255,255,255)
    else:
        assert _attr(c) == (255,255,255,255)
    c.hsla = (50.0, 50.0, 50.0, 50.0)
    h,s,l,a = c.hsla
    assert (_rd( h,s,l,a )) == (50.156, 50.394, 49.804, 49.804)
    if not env['pyjs_opt']:
        assert c == pg.Color(191,170,63,127)
    else:
        assert _attr(c) == (191,170,63,127)
    c.hsla = (0.0, 10.0, 20.0, 30.0)
    h,s,l,a = c.hsla
    assert (_rd( h,s,l,a )) == (0.0, 10.891, 19.804, 29.804)
    if not env['pyjs_opt']:
        assert c == pg.Color(56,45,45,76)
    else:
        assert _attr(c) == (56,45,45,76)
    c.hsla = (10.0, 20.0, 30.0, 40.0)
    h,s,l,a = c.hsla
    assert (_rd( h,s,l,a )) == (10.0, 19.737, 29.804, 40.0)
    if not env['pyjs_opt']:
        assert c == pg.Color(91,66,61,102)
    else:
        assert _attr(c) == (91,66,61,102)

