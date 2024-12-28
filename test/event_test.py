env = None
pg = None


# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    tests = [test_event_get,
             test_event_poll,
             test_event_wait,
             test_event_peek,
             test_event_clear,
             test_event_block,
             test_event_post]
    return tests


def test_event_get():
    events = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.USEREVENT]
    event_obj = {}
    for evt in events:
        event_obj[evt] = pg.event.Event(evt)
    pg.event.clear()
    assert pg.event.get() == []
    for evt in events:
        pg.event.post(event_obj[evt])
    evts = pg.event.get()
    assert [e.type for e in evts] == events
    for evt in events:
        pg.event.post(event_obj[evt])
    evts = pg.event.get(events[0])
    assert [e.type for e in evts] == events[:1]
    evts = pg.event.get()
    assert [e.type for e in evts] == events[1:]
    for evt in events:
        pg.event.post(event_obj[evt])
    evts = pg.event.get([events[1],events[2]])
    assert [e.type for e in evts] == events[1:]
    evts = pg.event.get()
    assert [e.type for e in evts] == events[:1]


def test_event_poll():
    events = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.USEREVENT]
    event_obj = {}
    for evt in events:
        event_obj[evt] = pg.event.Event(evt)
    pg.event.clear()
    assert pg.event.poll().type == pg.NOEVENT
    for evt in events:
        pg.event.post(event_obj[evt])
    evts = [pg.event.poll() for i in range(len(events))]


def test_event_wait():
    events = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.USEREVENT]
    event_obj = {}
    for evt in events:
        event_obj[evt] = pg.event.Event(evt)
    pg.event.clear()
    for evt in events:
        pg.event.post(event_obj[evt])
    evts = [pg.event.wait() for i in range(len(events))]
    assert [e.type for e in evts] == events
    assert pg.event.get() == []
    if env['platform'] != 'js':    #waiting not implemented
        pg.time.set_timer(events[0], 30)
        evt = pg.event.wait()
        assert evt.type == events[0]
        pg.time.set_timer(events[0], 0)


def test_event_peek():
    events = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.USEREVENT]
    event_obj = {}
    for evt in events:
        event_obj[evt] = pg.event.Event(evt)
    pg.event.clear()
    for evt in events:
        assert pg.event.peek(evt) == False
        pg.event.post(event_obj[evt])
        assert pg.event.peek(evt) == True


def test_event_clear():
    events = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.USEREVENT]
    event_obj = {}
    for evt in events:
        event_obj[evt] = pg.event.Event(evt)
    pg.event.clear()
    for evt in events:
        pg.event.post(event_obj[evt])
    pg.event.clear()
    assert pg.event.get() == []
    for evt in events:
        pg.event.post(event_obj[evt])
    pg.event.clear(events[0])
    evts = pg.event.get()
    assert [e.type for e in evts] == events[1:]
    for evt in events:
        pg.event.post(event_obj[evt])
    pg.event.clear((events[0], events[1]))
    evts = pg.event.get()
    assert [e.type for e in evts] == events[2:]


def test_event_block():
    events = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION]
    event_obj = {}
    for evt in events:
        event_obj[evt] = pg.event.Event(evt)
    for evt in events:
        pg.event.post(event_obj[evt])
    pg.event.set_blocked(events[2])
    pg.event.clear()
    for evt in events:
        pg.event.post(event_obj[evt])
    evts = pg.event.get()
    assert [e.type for e in evts] == events[:2]
    if env['platform'] not in ('jvm','js'):    #changed in pg2
        pg.event.set_allowed(None)
    else:
        pg.event.set_blocked(None)
    pg.event.clear()
    for evt in events:
        pg.event.post(event_obj[evt])
    evts = pg.event.get()
    assert [e.type for e in evts] == events


def test_event_post():
    events = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.USEREVENT]
    event_obj = {}
    for evt in events:
        event_obj[evt] = pg.event.Event(evt)
    pg.event.clear()
    for evt in events:
        pg.event.post(event_obj[evt])
    evts = pg.event.get()
    assert [e.type for e in evts if e.type in events] == events
    evt_obj = pg.event.Event(pg.USEREVENT,{'x':1,'y':2,'z':3})
    pg.event.post(evt_obj)
    evts = pg.event.get()
    e = [ev for ev in evts if ev.type==pg.USEREVENT][0]
    assert (e.type==pg.USEREVENT and e.x==1 and e.y==2 and e.z==3)

