env = None
pg = None
surface = None


# __pragma__ ('opov')


def init(environ):
    global env, pg, surface
    env = environ
    pg = env['pg']
    surface = env['surface']
    tests = [test_draw_rect,
             test_draw_circle,
             test_draw_ellipse,
             test_draw_arc,
             test_draw_polygon,
             test_draw_line,
             test_draw_lines]
    return tests


def test_draw_rect():
    data = [((10,6),0), ((10,8),1), ((10,10),1)], (5,8,10,5)
    surface.fill((0,0,0))
    rect = pg.draw.rect(surface, (255,0,0), (5,8,10,5))
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    assert (rect.x,rect.y,rect.width,rect.height) == data[1]
    data = [((10,6),0), ((10,8),1), ((10,10),0)], (5,8,10,5)
    surface.fill((0,0,0))
    rect = pg.draw.rect(surface, (255,0,0,255), pg.Rect((5,8,10,5)), 1)
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    assert (rect.x,rect.y,rect.width,rect.height) == data[1]
    data = [((3,0),1), ((3,2),1), ((3,4),0)], (0,0,5,3)
    surface.fill((0,0,0))
    rect = pg.draw.rect(surface, (255,0,0), (-5,-2,10,5))
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    assert (rect.x,rect.y,rect.width,rect.height) == data[1]


def test_draw_circle():
    data = [((10,0),0), ((10,5),1), ((10,10),1)], (5,5,10,10)
    surface.fill((0,0,0))
    rect = pg.draw.circle(surface, (255,0,0), (10,10), 5)
    data = [((10,0),0), ((10,5),1), ((10,10),0)], (5,5,10,10)
    surface.fill((0,0,0))
    rect = pg.draw.circle(surface, (255,0,0,255), (10,10), 5, 1)
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    assert (rect.x,rect.y,rect.width,rect.height) == data[1]


def test_draw_ellipse():
    data = [((10,6),1), ((10,8),1), ((10,10),0)], (5,5,10,5)
    surface.fill((0,0,0))
    rect = pg.draw.ellipse(surface, (255,0,0), (5,5,10,5))
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    assert (rect.x,rect.y,rect.width,rect.height) == data[1]


def test_draw_arc():
    data = [((10,0),0), ((10,5),1), ((10,10),0)], (5,5,11,6)
    surface.fill((0,0,0))
    rect = pg.draw.arc(surface, (255,0,0), (5,5,10,10), 0, 3.14)
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    if env['platform'] not in ('jvm','js'):
        try:
            assert (rect.x,rect.y,rect.width,rect.height) == data[1]
        except AssertionError:      #pg1.9.6
            assert (rect.x,rect.y,rect.width,rect.height) == (5,5,10,10)
    else:   #update to new boundary process
        assert (rect.x,rect.y,rect.width,rect.height) == (5,5,10,10)


def test_draw_polygon():
    data = [((10,4),0), ((10,6),1), ((10,8),1)], (5,5,11,11)
    surface.fill((0,0,0))
    rect = pg.draw.polygon(surface, (255,0,0), ((10,5),(15,15),(5,15)))
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    assert (rect.x,rect.y,rect.width,rect.height) == data[1]


def test_draw_line():
    data = [((10,6),0), ((10,8),1), ((10,10),0)], (5,8,11,1)
    surface.fill((0,0,0))
    rect = pg.draw.line(surface, (255,0,0), (5,8), (15,8), 1)
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    assert (rect.x,rect.y,rect.width,rect.height) == data[1]


def test_draw_lines():
    data = [((10,6),0), ((10,8),1), ((10,10),0)], (5,8,11,1)
    surface.fill((0,0,0))
    rect = pg.draw.lines(surface, (255,0,0), True, ((7,8),(5,8),(15,8)))
    for pos in data[0]:
        c = surface.get_at(pos[0])
        c = {True:1,False:0}[c.r>0]
        assert c == pos[1]
    assert (rect.x,rect.y,rect.width,rect.height) == data[1]

