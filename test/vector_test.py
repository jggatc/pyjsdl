env = None
pg = None


# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_vector,
             test_vector_magnitude,
             test_vector_direction,
             test_vector_dot,
             test_vector_cross,
             test_vector_lerp]
    return tests


def _rd(val):
    return round(val, 3)


def test_vector():
    Vector2 = pg.Vector2
    v1 = Vector2(2.2,3.0)
    v2 = Vector2(3.0,4.0)
    assert v1.x == 2.2 and v1.y == 3.0
    assert v1[0] == 2.2 and v1[1] == 3.0
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        v = v1 + v2
        assert v.x == 5.2 and v.y == 7.0
        v = v1 + (5,5)
        assert v.x == 7.2 and v.y == 8.0
    v = Vector2(v1)
    assert v.x == 2.2 and v.y == 3.0
    v.x = 1.0
    v.y = 2.0
    assert v.x == 1.0 and v.y == 2.0
    v.x += 0.5
    v.y -= 0.5
    assert v.x == 1.5 and v.y == 1.5
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        el = v1.elementwise()
        v = el + v2
        assert v.x == 5.2 and v.y == 7.0


def test_vector_magnitude():
    Vector2 = pg.Vector2
    v1 = Vector2(2.2,3.0)
    v2 = Vector2(6.0,8.0)
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
    v1 = Vector2(2,3)
    v2 = Vector2(6,8)
    v3 = Vector2(0,5)
    v4 = Vector2(0,-5)
    assert _rd(v1.angle_to(v2)) == -3.180
    assert _rd(v3.angle_to(v4)) == -180.0
    v = v1.rotate(30)
    assert _rd(v.x) == 0.232 and _rd(v.y) == 3.598
    if env['platform'] in ('jvm', 'js'):
        v = v1.rotate_rad(1.0)
        assert _rd(v.x) == -1.444 and _rd(v.y) == 3.304
    v = Vector2(v1)
    v.rotate_ip(30)
    assert _rd(v.x) == 0.232 and _rd(v.y) == 3.598
    if env['platform'] in ('jvm', 'js'):
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
    v.from_polar((3.606,56.310))
    assert _rd(v.x) == 2.0 and _rd(v.y) == 3.0


def test_vector_dot():
    Vector2 = pg.Vector2
    v1 = Vector2(2,3)
    v2 = Vector2(2,0)
    v3 = Vector2(0,3)
    v4 = Vector2(-6,-8)
    v5 = Vector2(3,4)
    assert v1.dot(v2) == 4.0
    assert v1.dot(v3) == 9.0
    assert v1.dot(v4) == -36.0
    assert v1.dot(v5) == 18.0
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        assert (v1*v2) == 4.0
        assert (v1*v3) == 9.0
        assert (v1*v4) == -36.0
        assert (v1*v5) == 18.0


def test_vector_cross():
    Vector2 = pg.Vector2
    v1 = Vector2(2,3)
    v2 = Vector2(2,0)
    v3 = Vector2(0,3)
    v4 = Vector2(-6,-8)
    v5 = Vector2(3,4)
    assert v1.cross(v2) == -6.0
    assert v1.cross(v3) == 6.0
    assert v1.cross(v4) == 2.0
    assert v1.cross(v5) == -1.0


def test_vector_lerp():
    Vector2 = pg.Vector2
    v1 = Vector2(2,3)
    v2 = Vector2(6,8)
    v = v1.lerp(v2, 0)
    assert _rd(v.x) == 2.0 and _rd(v.y) == 3.0
    v = v1.lerp(v2, 0.1)
    assert _rd(v.x) == 2.4 and _rd(v.y) == 3.5
    v = v1.lerp(v2, 0.5)
    assert _rd(v.x) == 4.0 and _rd(v.y) == 5.5
    v = v1.lerp(v2, 0.9)
    assert _rd(v.x) == 5.6 and _rd(v.y) == 7.5
    v = v1.lerp(v2, 1.0)
    assert _rd(v.x) == 6.0 and _rd(v.y) == 8.0
    v = v1.slerp(v2, 0)
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
    v = v1.slerp(v1,0.5)
    assert _rd(v.x) == 2.0 and _rd(v.y) == 3.0
    if not (env['pyjs_opt'] and not env['pyjs_attr']):
        v = v1.slerp(v1*2, 0.5)
        assert _rd(v.x) == 3.0 and _rd(v.y) == 4.5
    v = v1.slerp(Vector2(-6, -8), 0.5)
    assert _rd(v.x) == -5.553 and _rd(v.y) == 3.929
    v = Vector2(5,5).slerp(Vector2(-5,5), 0.2)
    assert _rd(v.x) == 3.210 and _rd(v.y) == 6.300

