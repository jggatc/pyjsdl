env = None
pg = None


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_vector_constructor,
             test_vector_update,
             test_vector_get,
             test_vector_operator,
             test_vector_magnitude,
             test_vector_direction,
             test_vector_dot,
             test_vector_cross,
             test_vector_lerp]
    return tests


def _rd(val):
    return round(val, 3)


def test_vector_constructor():
    Vector2 = pg.Vector2
    v = Vector2(2.2, 3.0)
    assert v.x == 2.2 and v.y == 3.0
    v = Vector2((2.2, 3.0))
    assert v.x == 2.2 and v.y == 3.0
    v = Vector2(v)
    assert v.x == 2.2 and v.y == 3.0


def test_vector_update():
    Vector2 = pg.Vector2
    v = Vector2(0.0, 0.0)
    v.update(2.2, 3.0)
    assert v.x == 2.2 and v.y == 3.0
    v.update((3.2, 4.0))
    assert v.x == 3.2 and v.y == 4.0
    v.update(v)
    assert v.x == 3.2 and v.y == 4.0


def test_vector_get():
    Vector2 = pg.Vector2
    v = Vector2(0.0, 0.0)
    assert v.x == 0.0 and v.y == 0.0
    assert v[0] == 0.0 and v[1] == 0.0
    v.x = 1.0
    v.y = 1.0
    assert v.x == 1.0 and v.y == 1.0
    assert v[0] == 1.0 and v[1] == 1.0
    v[0] = 2.0
    v[1] = 2.0
    assert v.x == 2.0 and v.y == 2.0
    assert v[0] == 2.0 and v[1] == 2.0
    x, y = v[0], v[1]
    assert x == 2.0 and y == 2.0
    x, y = v
    assert x == 2.0 and y == 2.0
    vl = []
    for _v in v:
        vl.append(_v)
    assert vl[0] == 2.0 and vl[1] == 2.0


def test_vector_operator():
    Vector2 = pg.Vector2
    v1 = Vector2(2.2, 3.0)
    v2 = Vector2(3.0, 4.0)
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        v = v1 + v2
        assert v.x == 5.2 and v.y == 7.0
        v = v1 + (5.0, 5.0)
        assert v.x == 7.2 and v.y == 8.0
        v = v1 - (1.0, 1.0)
        assert _rd(v.x) == 1.2 and v.y == 2.0
        v += v1
        assert _rd(v.x) == 3.4 and v.y == 5.0
        v -= (1.0, 1.0)
        assert _rd(v.x) == 2.4 and v.y == 4.0
        v = v1 * v2
        assert v == 18.6
        v = v1 * (3.0, 4.0)
        assert v == 18.6
    else:
        v = Vector2(v1)
        assert v.x == 2.2 and v.y == 3.0
        v.x = v.x + 1.0
        v.y = v.y + 2.0
        assert v.x == 3.2 and v.y == 5.0
        v.x += 0.5
        v.y -= 0.5
        assert v.x == 3.7 and v.y == 4.5
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        #-S / -O --enable-descriptor-proto --enable-operator-funcs
        #unable cmp vector to tuple
        el = v1.elementwise()
        v = el + v2
        assert v.x == 5.2 and v.y == 7.0
        v1 = Vector2(2.0, 3.0)
        v2 = Vector2(3.0, 4.0)
        vx = v1 + v2
        if not env['pyjs_opt']:
            assert vx == Vector2(5.0, 7.0)
        else:    #__eq__ not called
            assert (vx.x, vx.y) == (5.0, 7.0)
    if not env['pyjs_opt']:
        assert (v1 + v2) == Vector2(5.0, 7.0)
        assert (v1 + (3.0,4.0)) == Vector2(5.0, 7.0)
        assert (v1 - v2) == Vector2(-1.0, -1.0)
        assert (v1 - (3.0,4.0)) == Vector2(-1.0, -1.0)
        assert (v1 * v2) == 18.0
        assert (v1 * (3.0,4.0)) == 18.0
        assert (v1 * 2) == Vector2(4.0, 6.0)
        assert (v1 / 2) == Vector2(1.0, 1.5)
        assert (v1 // 2) == Vector2(1.0, 1.0)
        if env['platform'] != 'js':    ##
            assert ((2.0,3.0) + v2) == Vector2(5.0, 7.0)
            assert ((2.0,3.0) - v2) == Vector2(-1.0, -1.0)
            assert ((2.0,3.0) * v2) == 18.0
        assert (2 * v2) == Vector2(6.0, 8.0)
        v = Vector2(v1)
        v += v2
        assert v == Vector2(5.0, 7.0)
        v = Vector2(v1)
        v += (3.0,4.0)
        assert v == Vector2(5.0, 7.0)
        v = Vector2(v1)
        v -= v2
        assert v == Vector2(-1.0, -1.0)
        v = Vector2(v1)
        v -= (3.0,4.0)
        assert v == Vector2(-1.0, -1.0)
        v = Vector2(v1)
        v *= v2
        assert v == 18.0
        v = Vector2(v1)
        v *= (3.0,4.0)
        assert v == 18.0
        v = Vector2(v1)
        v *= 2
        assert v == Vector2(4.0, 6.0)
        v = Vector2(v1)
        v /= 2
        assert v == Vector2(1.0, 1.5)
        v = Vector2(v1)
        v //= 2
        assert v == Vector2(1.0, 1.0)
        v = Vector2(v1)
        el = v.elementwise()
        assert (el + v2) == Vector2(5.0, 7.0)
        assert (el - v2) == Vector2(-1.0, -1.0)
        assert (el * v2) == Vector2(6.0, 12.0)
        vx = (el / v2)
        assert (_rd(vx[0]), _rd(vx[1])) == (0.667, 0.75)
        assert (el // v2) == Vector2(0.0, 0.0)
        assert (v2 + el) == Vector2(5.0, 7.0)
        assert (v2 - el) == Vector2(1.0, 1.0)
        assert (v2 * el) == Vector2(6.0, 12.0)
        vx = (v2 / el)
        assert (_rd(vx[0]), _rd(vx[1])) == (1.5, 1.333)
        assert (v2 // el) == Vector2(1.0, 1.0)
        assert (el + (3.0,4.0)) == Vector2(5.0, 7.0)
        assert (el - (3.0,4.0)) == Vector2(-1.0, -1.0)
        assert (el * (3.0,4.0)) == Vector2(6.0, 12.0)
        vx = (el / (3.0,4.0))
        assert (_rd(vx[0]), _rd(vx[1])) == (0.667, 0.75)
        assert (el // (3.0,4.0)) == Vector2(0.0, 0.0)
        if env['platform'] != 'js':
            assert ((3.0,4.0) + el) == Vector2(5.0, 7.0)
            assert ((3.0,4.0) - el) == Vector2(1.0, 1.0)
            assert ((3.0,4.0) * el) == Vector2(6.0, 12.0)
            vx = ((3.0,4.0) / el)
            assert (_rd(vx[0]), _rd(vx[1])) == (1.5, 1.333)
            assert ((3.0,4.0) // el) == (1.0, 1.0)
        assert (el + 2) == Vector2(4.0, 5.0)
        assert (el - 2) == Vector2(0.0, 1.0)
        assert (el * 2) == Vector2(4.0, 6.0)
        assert (el / 2) == Vector2(1.0, 1.5)
        assert (el // 2) == Vector2(1.0, 1.0)
        assert (2 + el) == Vector2(4.0, 5.0)
        assert (2 - el) == Vector2(0.0, -1.0)
        assert (2 * el) == Vector2(4.0, 6.0)
        vx = (2 / el)
        assert (_rd(vx[0]), _rd(vx[1])) == (1.0, 0.667)
        assert (2 // el) == Vector2(1.0, 0.0)
        assert (v1 == v1) == True
        assert (v1 == v2) == False
        assert (v1 != v1) == False
        assert (v1 != v2) == True
        assert (v1 == Vector2(2.0,3.0)) == True
        assert (v1 == Vector2(3.0,4.0)) == False
        assert (v1 != Vector2(2.0,3.0)) == False
        assert (v1 != Vector2(3.0,4.0)) == True
        assert (v1 == 2) == False
        assert (v1 != 2) == True
        assert (el == el) == True
        assert (el != el) == False
        if env['platform'] != 'js':    ##pyjs cmp obj identity
            assert (el == v1) == True
            assert (el == v2) == False
            assert (el != v1) == False
            assert (el != v2) == True
            assert (el == (2.0,3.0)) == True
            assert (el == (3.0,4.0)) == False
            assert (el != (2.0,3.0)) == False
            assert (el != (3.0,4.0)) == True

def test_vector_magnitude():
    Vector2 = pg.Vector2
    v1 = Vector2(2.2, 3.0)
    v2 = Vector2(6.0, 8.0)
    if env['platform'] != 'js':
        assert _rd(v1.magnitude()) == _rd(v1.length()) == 3.720
    else:   #length is js keyword
        assert _rd(v1.magnitude()) == 3.720
    assert _rd(v1.magnitude_squared()) == _rd(v1.length_squared()) == 13.84
    v = v1.normalize()
    assert _rd(v.x) == 0.591 and _rd(v.y) == 0.806
    v = Vector2(v1)
    v.normalize_ip()
    assert _rd(v.x) == 0.591 and _rd(v.y) == 0.806
    assert v.is_normalized() == True
    v.scale_to_length(10)
    assert _rd(v.x) == 5.914 and _rd(v.y) == 8.064
    assert _rd(v1.distance_to(v2)) == 6.28
    assert _rd(v1.distance_squared_to(v2)) == 39.44


def test_vector_direction():
    Vector2 = pg.Vector2
    v1 = Vector2(2.0, 3.0)
    v2 = Vector2(6.0, 8.0)
    v3 = Vector2(0.0, 5.0)
    v4 = Vector2(0.0, -5.0)
    assert _rd(v1.angle_to(v2)) == -3.180
    assert _rd(v3.angle_to(v4)) == -180.0
    v = v1.rotate(30)
    assert _rd(v.x) == 0.232 and _rd(v.y) == 3.598
#    if env['platform'] in ('jvm', 'js'):
    v = v1.rotate_rad(1.0)
    assert _rd(v.x) == -1.444 and _rd(v.y) == 3.304
    v = Vector2(v1)
    v.rotate_ip(30)
    assert _rd(v.x) == 0.232 and _rd(v.y) == 3.598
#    if env['platform'] in ('jvm', 'js'):
    v = Vector2(v1)
    v.rotate_ip_rad(1.0)
    assert _rd(v.x) == -1.444 and _rd(v.y) == 3.304
    v = v1.reflect(v2)
    assert _rd(v.x) == -2.32 and _rd(v.y) == -2.76
    v = Vector2(v1)
    v.reflect_ip(v2)
    assert _rd(v.x) == -2.32 and _rd(v.y) == -2.76
    r = v1.as_polar()
    assert _rd(r[0]) == 3.606 and _rd(r[1]) == 56.310
    v = Vector2(v1)
    v.from_polar((3.606, 56.310))
    assert _rd(v.x) == 2.0 and _rd(v.y) == 3.0


def test_vector_dot():
    Vector2 = pg.Vector2
    v1 = Vector2(2.0, 3.0)
    v2 = Vector2(2.0, 0.0)
    v3 = Vector2(0.0, 3.0)
    v4 = Vector2(-6.0, -8.0)
    v5 = Vector2(3.0, 4.0)
    assert v1.dot(v2) == 4.0
    assert v1.dot(v3) == 9.0
    assert v1.dot(v4) == -36.0
    assert v1.dot(v5) == 18.0
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        assert (v1 * v2) == 4.0
        assert (v1 * v3) == 9.0
        assert (v1 * v4) == -36.0
        assert (v1 * v5) == 18.0


def test_vector_cross():
    Vector2 = pg.Vector2
    v1 = Vector2(2.0, 3.0)
    v2 = Vector2(2.0, 0.0)
    v3 = Vector2(0.0, 3.0)
    v4 = Vector2(-6.0, -8.0)
    v5 = Vector2(3.0, 4.0)
    assert v1.cross(v2) == -6.0
    assert v1.cross(v3) == 6.0
    assert v1.cross(v4) == 2.0
    assert v1.cross(v5) == -1.0


def test_vector_lerp():
    Vector2 = pg.Vector2
    v1 = Vector2(2.0, 3.0)
    v2 = Vector2(6.0, 8.0)
    v = v1.lerp(v2, 0.0)
    assert _rd(v.x) == 2.0 and _rd(v.y) == 3.0
    v = v1.lerp(v2, 0.1)
    assert _rd(v.x) == 2.4 and _rd(v.y) == 3.5
    v = v1.lerp(v2, 0.5)
    assert _rd(v.x) == 4.0 and _rd(v.y) == 5.5
    v = v1.lerp(v2, 0.9)
    assert _rd(v.x) == 5.6 and _rd(v.y) == 7.5
    v = v1.lerp(v2, 1.0)
    assert _rd(v.x) == 6.0 and _rd(v.y) == 8.0
    v = v1.slerp(v2, 0.0)
    assert _rd(v.x) == 2.0 and _rd(v.y) == 3.0
    v = v1.slerp(v2, 0.1)
    assert _rd(v.x) == 2.374 and _rd(v.y) == 3.519
    v = v1.slerp(v2, 0.5)
    assert _rd(v.x) == 3.929 and _rd(v.y) == 5.553
    v = v1.slerp(v2, 0.9)
    assert _rd(v.x) == 5.575 and _rd(v.y) == 7.519
    v = v1.slerp(v2, 1.0)
    assert _rd(v.x) == 6.0 and _rd(v.y) == 8.0
    v = v1.slerp(v2, -0.5)
    assert _rd(v.x) == -3.929 and _rd(v.y) == -5.553
    v = v1.slerp(v2, -1.0)
    assert _rd(v.x) == 6.0 and _rd(v.y) == 8.0
    v = v1.slerp(v1, 0.5)
    assert _rd(v.x) == 2.0 and _rd(v.y) == 3.0
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        v = v1.slerp(v1*2.0, 0.5)
        assert _rd(v.x) == 3.0 and _rd(v.y) == 4.5
    v = v1.slerp(Vector2(-6.0, -8.0), 0.5)
    assert _rd(v.x) == -5.553 and _rd(v.y) == 3.929
    v = Vector2(5.0, 5.0).slerp(Vector2(-5.0, 5.0), 0.2)
    assert _rd(v.x) == 3.210 and _rd(v.y) == 6.300

