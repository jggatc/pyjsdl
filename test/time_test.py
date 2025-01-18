env = None
pg = None
wait = 0


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_time_delay,
             test_time_wait,
             test_time_timer]
    return tests


def test_time_delay():
    _time = 30
    t = pg.time.get_ticks()
    pg.time.delay(_time)
    assert (pg.time.get_ticks()-t) >= _time


def test_time_wait():
    global wait
    _time = 30
    if env['platform'] != 'js':
        t = pg.time.get_ticks()
        pg.time.wait(_time)
        assert (pg.time.get_ticks()-t) >= _time
    else:
        if not wait:
            wait = pg.time.get_ticks()
            pg.time.wait(_time)
            return True
        else:
            assert (pg.time.get_ticks()-wait) >= _time
            wait = 0
            return False


def test_time_timer():
    global wait
    _time = 30
    event = pg.USEREVENT
    if env['platform'] != 'js':
        t = pg.time.get_ticks()
        pg.event.clear()
        pg.time.set_timer(event, _time)
        evt = pg.event.wait()
        pg.time.set_timer(event, 0)
        assert evt.type == event
        assert (pg.time.get_ticks()-t) >= _time
    else:
        if not wait:
            wait = pg.time.get_ticks()
            pg.event.clear()
            pg.time.set_timer(event, _time)
            pg.time.wait(_time)
            return True
        else:
            evt = pg.event.get()[0]
            pg.time.set_timer(event, 0)
            assert evt.type == event
            assert (pg.time.get_ticks()-wait) >= _time
            wait = 0
            return False

