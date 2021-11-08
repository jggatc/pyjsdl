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
    tests = [test_transform_rotate,
             test_transform_rotozoom,
             test_transform_scale,
             test_transform_flip]
    return tests


def test_transform_rotate():
    surface.fill((0,0,0))
    surface.fill((255,0,0), (0,0,width//2,height))
    surf = pg.transform.rotate(surface, 180)
    assert surf.get_size() == (width, height)
    assert surf.get_at((5,5)).r == 0 and surf.get_at((width-5,5)).r == 255


def test_transform_rotozoom():
    surface.fill((0,0,0))
    surface.fill((255,0,0), (0,0,width//2,height))
    surf = pg.transform.rotozoom(surface, 180, 2.0)
    assert int(surf.get_width()/width) == 2 and int(surf.get_height()/height) == 2
    assert surf.get_at((5,5)).r == 0 and surf.get_at((width*2-5,5)).r == 255



def test_transform_scale():
    surface.fill((0,0,0))
    surface.fill((255,0,0), (0,0,width//2,height))
    size = (width*2, height*2)
    surf = pg.transform.scale(surface, size)
    assert int(surf.get_width()/width) == 2 and int(surf.get_height()/height) == 2
    assert surf.get_at((5,5)).r == 255 and surf.get_at((width*2-5,5)).r == 0
    surf = pg.transform.smoothscale(surface, size)
    assert int(surf.get_width()/width) == 2 and int(surf.get_height()/height) == 2
    assert surf.get_at((5,5)).r == 255 and surf.get_at((width*2-5,5)).r == 0
    surf = pg.transform.scale2x(surface)
    assert int(surf.get_width()/width) == 2 and int(surf.get_height()/height) == 2
    assert surf.get_at((5,5)).r == 255 and surf.get_at((width*2-5,5)).r == 0


def test_transform_flip():
    surface.fill((0,0,0))
    surface.fill((255,0,0), (0,0,width//2,height))
    surf = pg.transform.flip(surface, True, False)
    assert surf.get_size() == (width, height)
    assert surf.get_at((5,5)).r == 0 and surf.get_at((width-5,5)).r == 255
    surf = pg.transform.flip(surface, False, True)
    assert surf.get_size() == (width, height)
    assert surf.get_at((5,5)).r == 255 and surf.get_at((width-5,5)).r == 0
    surf = pg.transform.flip(surface, True, True)
    assert surf.get_size() == (width, height)
    assert surf.get_at((5,5)).r == 0 and surf.get_at((width-5,5)).r == 255

