env = None
pg = None


# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_sprite,
             test_sprite_group]
    return tests


def test_sprite():
    Sprite = pg.sprite.Sprite
    Group = pg.sprite.Group
    g = [Group() for i in range(20)]
    sx, rx, i = {}, {}, 10
    sx[0] = Sprite()
    sx[1] = Sprite(*g)
    sx[2] = Sprite(g)
    sx[3] = Sprite([])
    sx[4] = Sprite(g[0])
    sx[5] = Sprite([g[0],g[1]])
    sx[6] = Sprite([g])
    sx[7] = Sprite([g],g)
    sx[8] = Sprite(g); sx[8].remove(g[0]); sx[8].remove([g[0],g[1]],g[10])
    sx[9] = Sprite(g); sx[9].kill()
    sx[0+i] = Sprite(); sx[0+i].add()
    sx[1+i] = Sprite(); sx[1+i].add(*g)
    sx[2+i] = Sprite(); sx[2+i].add(g)
    sx[3+i] = Sprite(); sx[3+i].add([])
    sx[4+i] = Sprite(); sx[4+i].add(g[0])
    sx[5+i] = Sprite(); sx[5+i].add([g[0],g[1]])
    sx[6+i] = Sprite(); sx[6+i].add([g])
    sx[7+i] = Sprite(); sx[7+i].add([g],g)
    sx[8+i] = Sprite(); sx[8+i].add(g); sx[8+i].remove(g[0]); sx[8+i].remove([g[0],g[1]],g[10])
    sx[9+i] = Sprite(); sx[9+i].add(g); sx[9+i].kill()
    rx[0] = rx[0+i] = [ 0, False ]
    rx[1] = rx[1+i] = [ 20, True ]
    rx[2] = rx[2+i] = [ 20, True ]
    rx[3] = rx[3+i] = [ 0, False ]
    rx[4] = rx[4+i] = [ 1, True ]
    rx[5] = rx[5+i] = [ 2, True ]
    rx[6] = rx[6+i] = [ 20, True ]
    rx[7] = rx[7+i] = [ 20, True ]
    rx[8] = rx[8+i] = [ 17, True ]
    rx[9] = rx[9+i] = [ 0, False ]
    for i in range(20):
        s,r = sx[i],rx[i]
        assert len(s.groups()) == r[0]
        assert s.alive() == r[1]


def test_sprite_group():
    for Group in (pg.sprite.Group,
                  pg.sprite.RenderUpdates,
                  pg.sprite.OrderedUpdates,
                  pg.sprite.LayeredUpdates):
        Sprite = pg.sprite.Sprite
        s = [Sprite() for i in range(20)]
        grp = Group(s)
        gx, rx, i = {}, {}, 12
        gx[0] = Group()
        gx[1] = Group(*s)
        gx[2] = Group(s)
        gx[3] = Group([])
        gx[4] = Group(s[0])
        gx[5] = Group([s[0],s[1]])
        gx[6] = Group([s])
        gx[7] = Group([s],s)
        gx[8] = Group(grp)
        gx[9] = Group([grp])
        gx[10] = Group(s); gx[8].remove(s[0]); gx[8].remove([s[0],s[1]],s[10])
        gx[11] = Group(s); gx[9].empty()
        gx[0+i] = Group(); gx[0+i].add()
        gx[1+i] = Group(); gx[1+i].add(*s)
        gx[2+i] = Group(); gx[2+i].add(s)
        gx[3+i] = Group(); gx[3+i].add([])
        gx[4+i] = Group(); gx[4+i].add(s[0])
        gx[5+i] = Group(); gx[5+i].add([s[0],s[1]])
        gx[6+i] = Group(); gx[6+i].add([s])
        gx[7+i] = Group(); gx[7+i].add([s],s)
        gx[8+i] = Group(); gx[8+i].add(grp)
        gx[9+i] = Group(); gx[9+i].add([grp])
        gx[10+i] = Group(s); gx[10+i].add(s); gx[10+i].remove(s[0]); gx[10+i].remove([s[0],s[1]],s[10])
        gx[11+i] = Group(s); gx[11+i].add(s); gx[11+i].empty()
        rx[0] = rx[0+i] = [ 0, False, False, False ]
        rx[1] = rx[1+i] = [ 20, True, True, True ]
        rx[2] = rx[2+i] = [ 20, True, True, True ]
        rx[3] = rx[3+i] = [ 0, False, False, False ]
        rx[4] = rx[4+i] = [ 1, True, False, False ]
        rx[5] = rx[5+i] = [ 2, True, False, False ]
        rx[6] = rx[6+i] = [ 20, True, True, True ]
        rx[7] = rx[7+i] = [ 20, True, True, True ]
        rx[8] = rx[8+i] = [ 20, True, True, True ]
        rx[9] = rx[9+i] = [ 20, True, True, True ]
        rx[10] = rx[10+i] = [ 17, False, False, True ]
        rx[11] = rx[11+i] = [ 0, False, False, False ]
        for x in range(i*2):
            g,r = gx[i],rx[i]
            assert len(g.sprites()) == r[0]
            assert g.has(s[0]) == r[1]
            assert g.has([s[0],s[1],s[2]]) == r[2]
            assert g.has([s[2],s[5]],s[6]) == r[3]

