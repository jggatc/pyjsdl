env = None
pg = None


# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_cursor]
    return tests


def test_cursor():
    cursor_str = ( '.      .',
                   ' .    . ',
                   '   ..   ',
                   '  .XX.  ',
                   '  .XX.  ',
                   '   ..   ',
                   ' .    . ',
                   '.      .' )
    size = (8,8)
    hotspot = (0,0)
    cursor_dat = pg.cursors.compile(cursor_str)
    pg.mouse.set_cursor(size, hotspot, *cursor_dat)
    if env['platform'] in ('jvm', 'js'):
        data, mask = cursor_dat[0], cursor_dat[1]
        cursor_surf = pg.cursors.create_cursor(size, data, mask)
        pg.mouse.set_cursor(cursor_surf, hotspot)
        cc1 = cursor_surf.get_at((0,0))
        cc2 = cursor_surf.get_at((0,1))
        c1 = pg.Color(255,255,255,255)
        c2 = pg.Color(0,0,0,0)
        if not env['pyjs_opt']:
            assert cc1 == c1
            assert cc2 == c2
        else:   #pyjs -O __eq__ ignored
            assert cc1.r==c1.r and cc1.g==c1.g and cc1.b==c1.b and cc1.a==c1.a
            assert cc2.r==c2.r and cc2.g==c2.g and cc2.b==c2.b and cc2.a==c2.a

