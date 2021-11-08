env = None
pg = None


# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_surfarray_blit_array,
             test_surfarray_make_surface,
             test_surfarray_array2d,
             test_surfarray_array3d,
             test_surfarray_array_alpha]
    return tests


def test_surfarray_blit_array():
    if env['platform'] == 'jvm':
        try:
            pg.surfarray._init()
        except ImportError:
            raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array2d = pg.surfarray.array2d(surface)
    surface.fill((255,0,0))
    if env['executor'] != 'pyjs':
        assert surface.get_at((0,0)) == (255,0,0,255)
    else:
        c = surface.get_at((0,0))
        assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    pg.surfarray.blit_array(surface, array2d)
    if env['executor'] != 'pyjs':
        assert surface.get_at((0,0)) == (0,0,0,255)
    else:
        c = surface.get_at((0,0))
        assert (c.r,c.g,c.b,c.a) == (0,0,0,255)
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array3d = pg.surfarray.array3d(surface)
    surface.fill((255,0,0))
    if env['executor'] != 'pyjs':
        assert surface.get_at((0,0)) == (255,0,0,255)
    else:
        c = surface.get_at((0,0))
        assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    pg.surfarray.blit_array(surface, array3d)
    if env['executor'] != 'pyjs':
        assert surface.get_at((0,0)) == (0,0,0,255)
    else:
        c = surface.get_at((0,0))
        assert (c.r,c.g,c.b,c.a) == (0,0,0,255)


def test_surfarray_make_surface():
    if env['platform'] == 'jvm':
        try:
            pg.surfarray._init()
        except ImportError:
            raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((255,0,0))
    if env['platform'] in ('jvm', 'js'):
        array2d = pg.surfarray.array2d(surface)
        surface2d = pg.surfarray.make_surface(array2d)
        if env['executor'] != 'pyjs':
            assert surface2d.get_size() == (15,10)
            assert surface2d.get_at((0,0)) == (255,0,0,255)
        else:
            c = surface.get_at((0,0))
            assert (c.r,c.g,c.b,c.a) == (255,0,0,255)
    array3d = pg.surfarray.array3d(surface)
    surface3d = pg.surfarray.make_surface(array3d)
    assert surface3d.get_size() == (15,10)
    if env['executor'] != 'pyjs':
        assert surface3d.get_at((0,0)) == (255,0,0,255)
    else:
        c = surface.get_at((0,0))
        assert (c.r,c.g,c.b,c.a) == (255,0,0,255)


def test_surfarray_array2d():
    if env['platform'] == 'jvm':
        try:
            pg.surfarray._init()
        except ImportError:
            raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array = pg.surfarray.array2d(surface)
    for i in range(10):
        array[0,i] = 255
    assert array[0,0] == 255
    assert array[0,1]>>24 & 0xff == 0
    if env['platform'] == 'jvm':   #array has alpha
    	assert array[1,0]>>24 & 0xff == 255
    surface2 = pg.Surface((15,10), pg.SRCALPHA)
    array2 = pg.surfarray.array2d(surface2)
    for i in range(10):
        array2[0,i] = 255
    assert array2[0,0] == 255
    assert array2[1,0] == 0
    if env['platform'] == 'js':
        array = pg.surfarray.array2d(surface, True)
        for i in range(10):
            array[0,i] = 255
        assert array[0,0] == 255
        surface2 = pg.Surface((15,10), pg.SRCALPHA)
        array2 = pg.surfarray.array2d(surface2, True)
        for i in range(10):
            array2[0,i] = 255
        assert array2[0,0] == 255
        assert array2[1,0] == 0


def test_surfarray_array3d():
    if env['platform'] == 'jvm':
        try:
            pg.surfarray._init()
        except:
            raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array = pg.surfarray.array3d(surface)
    if env['platform'] != 'js':
        assert array.shape == (15,10,3)
    else:
        if not env['pyjs_opt']:
            assert array.shape == (10,15,4)
        else:
            assert array.getshape() == (10,15,4)
    for i in range(10):
        array[0,i] = (0,0,255)
    assert array[0,0,2] == 255
    assert array[1,0,2] == 0
    if env['platform'] == 'js':
        array = pg.surfarray.array3d(surface, True)
        if not env['pyjs_opt']:
            assert array.shape == (15,10,3)
        else:
            assert array.getshape() == (15,10,3)
        for i in range(10):
            array[0,i] = (0,0,255)
        assert array[0,0,2] == 255
        assert array[1,0,2] == 0


def test_surfarray_array_alpha():
    if env['platform'] == 'jvm':
        try:
            pg.surfarray._init()
        except ImportError:
            raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array = pg.surfarray.array_alpha(surface)
    if env['platform'] != 'js':
        assert array.shape == (15,10)
    else:
        if not env['pyjs_opt']:
            assert array.shape == (10,15,4)
        else:
            assert array.getshape() == (10,15,4)
    assert array[1,1] & 0xff == 255
    surface2 = pg.Surface((15,10),pg.SRCALPHA)
    array2 = pg.surfarray.array_alpha(surface2)
    for i in range(10):
        array2[0,i] = 255
    assert array2[0,0] & 0xff == 255
    assert array2[1,0] & 0xff == 0
    if env['platform'] == 'js':
        array = pg.surfarray.array_alpha(surface)
        assert array[1,1] & 0xff == 255
        surface2 = pg.Surface((15,10),pg.SRCALPHA)
        array2 = pg.surfarray.array_alpha(surface2)
        for i in range(10):
            array2[0,i] = 255
        assert array2[0,0] & 0xff == 255
        assert array2[1,0] & 0xff == 0

