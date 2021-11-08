env = None
pg = None


# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_mask,
             test_mask_from_surface,
             test_mask_from_threshold]
    return tests


def test_mask():
    surface = pg.Surface((15,10),pg.SRCALPHA)
    pg.draw.rect(surface, (10,20,30), (0,0,4,3))
    mask = pg.mask.from_surface(surface)
    assert mask.get_size() == (15,10)
    assert mask.count() == 12
    assert mask.get_at((0,0)) == 1
    assert mask.get_at((4,0)) == 0
    mask.set_at((4,0))
    assert mask.get_at((4,0)) == 1
    assert mask.count() == 13
    assert bool(mask.overlap(mask, (0,0))) == True
    assert bool(mask.overlap(mask, (2,2))) == True
    assert bool(mask.overlap(mask, (5,5))) == False
    assert bool(mask.overlap(mask, (5,0))) == False
    assert bool(mask.overlap(mask, (0,5))) == False
    assert mask.get_at((8,0)) == 0
    mask.fill()
    assert mask.get_at((8,0)) == 1
    assert mask.count() == 150
    mask.clear()
    assert mask.get_at((8,0)) == 0
    assert mask.count() == 0
    mask.invert()
    assert mask.get_at((8,0)) == 1
    assert mask.count() == 150


def test_mask_from_surface():
    surface = pg.Surface((15,10),pg.SRCALPHA)
    pg.draw.rect(surface, (10,20,30), (0,0,4,3))
    mask = pg.mask.from_surface(surface)
    assert mask.get_at((0,0)) == 1
    assert mask.get_at((3,0)) == 1
    assert mask.get_at((4,0)) == 0
    assert mask.get_at((0,1)) == 1
    assert mask.get_at((3,1)) == 1
    assert mask.get_at((4,1)) == 0
    assert mask.count() == 12
    mask = pg.mask.from_surface(surface,254)
    assert mask.get_at((0,0)) == 1
    assert mask.get_at((3,0)) == 1
    assert mask.get_at((4,0)) == 0
    assert mask.count() == 12
    mask = pg.mask.from_surface(surface,255)
    assert mask.get_at((0,0)) == 0
    assert mask.get_at((3,0)) == 0
    assert mask.get_at((4,0)) == 0
    assert mask.count() == 0


def test_mask_from_threshold():
    surface = pg.Surface((15,10),pg.SRCALPHA)
    pg.draw.rect(surface, (50,100,150), (0,0,4,3))
    mask = pg.mask.from_threshold(surface, (50,100,150), (1,1,1,255))
    assert mask.get_at((0,0)) == 1
    assert mask.get_at((3,0)) == 1
    assert mask.get_at((4,0)) == 0
    assert mask.get_at((0,1)) == 1
    assert mask.get_at((3,1)) == 1
    assert mask.get_at((4,1)) == 0
    assert mask.count() == 12
    mask = pg.mask.from_threshold(surface, (50,100,150), (1,1,0,255))
    if env['platform'] in ('jvm', 'js'):   #pg error?
        assert mask.get_at((0,0)) == 1
        assert mask.get_at((3,0)) == 1
        assert mask.get_at((4,0)) == 0
        assert mask.count() == 12
    else:
        assert mask.count() == 0
    mask = pg.mask.from_threshold(surface, (50,100,150), (1,1,0,254))
    if env['platform'] in ('jvm', 'js'):   #pg error?
        assert mask.get_at((0,0)) == 1
        assert mask.get_at((3,0)) == 1
        assert mask.get_at((4,0)) == 0
        assert mask.count() == 12
    else:
        assert mask.count() == 0
    mask = pg.mask.from_threshold(surface, (50,100,150))
    if env['platform'] in ('jvm' 'js'):    #pg error?
        assert mask.get_at((0,0)) == 1
        assert mask.get_at((3,0)) == 1
        assert mask.get_at((4,0)) == 0
        assert mask.get_at((0,1)) == 1
        assert mask.get_at((3,1)) == 1
        assert mask.get_at((4,1)) == 0
        assert mask.count() == 12
    else:
        assert mask.count() == 0

