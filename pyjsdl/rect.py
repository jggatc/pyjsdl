#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

__docformat__ = 'restructuredtext'


class Rect(object):
    """
    **pyjsdl.Rect**
    
    * Rect.copy
    * Rect.move
    * Rect.move_ip
    * Rect.inflate
    * Rect.inflate_ip
    * Rect.contains
    * Rect.union
    * Rect.union_ip
    * Rect.unionall
    * Rect.unionall_ip
    * Rect.clamp
    * Rect.clamp_ip
    * Rect.clip
    * Rect.collidepoint
    * Rect.colliderect
    * Rect.collidelist
    * Rect.collidelistall
    * Rect.collidedict
    * Rect.collidedictall
    """

    __slots__ = ['x', 'y', 'width', 'height']

    def __init__(self, *args):
        """
        Return Rect object.
        
        Alternative arguments:
        
        * x, y, width, height
        * (x, y), (width, height)
        * (x, y, width, height)
        * Rect
        * Obj with rect attribute

        Rect has the attributes::
        
        x, y, width, height
        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        center, centerx, centery
        size, w, h

        Attribute access is functional in strict mode (-S),
        while in optimized mode (-O) direct access can be used
        with x/y/width/height whereas other attributes can be
        accessed with getattr/setattr functions or build with
        the --enable-descriptor-proto option.
        
        Module initialization places pyjsdl.Rect in module's namespace.
        """
        if len(args) == 1:
            arg = args[0]
        else:
            arg = args
        ln = len(arg)
        if ln == 4:
            x = arg[0]
            y = arg[1]
            width = arg[2]
            height = arg[3]
        elif ln == 2:
            x = arg[0][0]
            y = arg[0][1]
            width = arg[1][0]
            height = arg[1][1]
        else:
            if hasattr(arg, 'rect'):
                arg = arg.rect
            x = arg.x
            y = arg.y
            width = arg.width
            height = arg.height
        object.__setattr__(self, 'x', int(x))
        object.__setattr__(self, 'y', int(y))
        object.__setattr__(self, 'width', int(width))
        object.__setattr__(self, 'height', int(height))

    def __str__(self):
        return "<rect(%s, %s, %s, %s)>" % (self.x,
                                           self.y,
                                           self.width,
                                           self.height)

    def __repr__(self):
        return "%s(%s,%s,%s,%s)" % (self.__class__, self.x,
                                                    self.y,
                                                    self.width,
                                                    self.height)

    def __setattr__(self, attr, val):   #not implemented in pyjs -O
        try:
            getattr(self, '_set_'+attr)(val)
        except AttributeError:
            msg = 'Rect object has no attribute %s' % attr
            raise AttributeError(msg)

    def __getitem__(self, key):
        return getattr(self, ('x','y','width','height')[key])

    def __setitem__(self, key, val):
        setattr(self, ('x','y','width','height')[key], val)

    def __iter__(self):
        return iter([self.x, self.y, self.width, self.height])

    def __len__(self):
        return 4

    def __bool__(self):
        return self.width and self.height

    def __nonzero__(self):
        return self.width and self.height

    def __eq__(self, other):
        #pyjs compares rect==tuple not __eq__
        return (self.x == other.x and
                self.y == other.y and
                self.width == other.width
                and self.height == other.height)

    def __ne__(self, other):
        #pyjs compares rect!=tuple not __ne__
        return (self.x != other.x or
                self.y != other.y or
                self.width != other.width or
                self.height != other.height)

    def setLocation(self, x, y):
        object.__setattr__(self, 'x', int(x))
        object.__setattr__(self, 'y', int(y))
        return None

    def setSize(self, width, height):
        object.__setattr__(self, 'width', int(width))
        object.__setattr__(self, 'height', int(height))
        return None

    def copy(self):
        """
        Returns Rect that is a copy of this rect.
        """
        return Rect(self.x, self.y, self.width, self.height)

    def move(self, *offset):
        """
        Return Rect of same dimension at position offset by x,y.
        """
        if len(offset) == 2:
            x, y = offset
        else:
            x, y = offset[0]
        return Rect(self.x+x, self.y+y, self.width, self.height)

    def move_ip(self, *offset):
        """
        Moves this rect to position offset by x,y.
        """
        if len(offset) == 2:
            x, y = offset
        else:
            x, y = offset[0]
        self.setLocation(self.x+x, self.y+y)
        return None

    def inflate(self, *offset):
        """
        Return Rect at same position but size offset by x,y.
        """
        if len(offset) == 2:
            x, y = offset
        else:
            x, y = offset[0]
        return Rect(self.x-x//2, self.y-y//2, self.width+x, self.height+y)

    def inflate_ip(self, *offset):
        """
        Change size of this rect offset by x,y.
        """
        if len(offset) == 2:
            x, y = offset
        else:
            x, y = offset[0]
        self.setSize(self.width+x, self.height+y)
        self.setLocation(self.x-x//2, self.y-y//2)
        return None

    def clip(self, rect):
        """
        Return Rect representing this rect clipped by rect.
        """
        if not self.intersects(rect):
            return Rect(0,0,0,0)
        else:
            x = self.x if self.x > rect.x else rect.x
            y = self.y if self.y > rect.y else rect.y
            s = self.x+self.width
            r = rect.x+rect.width
            w = (s if s < r else r) - x
            s = self.y+self.height
            r = rect.y+rect.height
            h = (s if s < r else r) - y
            return Rect(x, y, w, h)

    def intersection(self, rect):
        """
        Return Rect representing this rect clipped by rect.
        """
        return self.clip(rect)

    def contains(self, rect):
        """
        Check if rect is in this rect.
        """
        return (self.x <= rect.x and
                (self.x + self.width) >= (rect.x + rect.width) and
                self.y <= rect.y and
                (self.y + self.height) >= (rect.y + rect.height))

    def intersects(self, rect):
        """
        Check if rect intersects this rect.
        """
        return (self.x < (rect.x + rect.width) and
                rect.x < (self.x + self.width) and
                self.y < (rect.y + rect.height) and
                rect.y < (self.y + self.height))

    def union(self, rect):
        """
        Return Rect representing the union of rect and this rect.
        """
        x = self.x if self.x < rect.x else rect.x
        y = self.y if self.y < rect.y else rect.y
        s = self.x + self.width
        r = rect.x + rect.width
        w = (s if s > r else r) - x
        s = self.y + self.height
        r = rect.y + rect.height
        h = (s if s > r else r) - y
        return Rect(x, y, w, h)

    def union_ip(self, rect):
        """
        Change this rect to represent the union of rect and this rect.
        """
        x = self.x if self.x < rect.x else rect.x
        y = self.y if self.y < rect.y else rect.y
        s = self.x + self.width
        r = rect.x + rect.width
        w = (s if s > r else r) - x
        s = self.y + self.height
        r = rect.y + rect.height
        h = (s if s > r else r) - y
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        return None

    def unionall(self, rect_list):
        """
        Return Rect representing the union of rect list and this rect.
        """
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height
        for r in rect_list:
            if r.x < x1:
                x1 = r.x
            if r.y < y1:
                y1 = r.y
            rx2 = r.x + r.width
            if rx2 > x2:
                x2 = rx2
            ry2 = r.y + r.height
            if ry2 > y2:
                y2 = ry2
        return Rect(x1, y1, x2-x1, y2-y1)

    def unionall_ip(self, rect_list):
        """
        Change this rect to represent the union of rect list and this rect.
        """
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height
        for r in rect_list:
            if r.x < x1:
                x1 = r.x
            if r.y < y1:
                y1 = r.y
            rx2 = r.x + r.width
            if rx2 > x2:
                x2 = rx2
            ry2 = r.y + r.height
            if ry2 > y2:
                y2 = ry2
        self.x = x1
        self.y = y1
        self.width = x2 - x1
        self.height = y2 - y1
        return None

    def clamp(self, rect):
        """
        Return Rect of same dimension as this rect moved within rect.
        """
        if self.width < rect.width:
            if self.x < rect.x:
                x = rect.x
            elif self.x + self.width > rect.x + rect.width:
                x = rect.x + rect.width - self.width
            else:
                x = self.x
        else:
            x = rect.x - int((self.width - rect.width)/2)
        if self.height < rect.height:
            if self.y < rect.y:
                y = rect.y
            elif self.y + self.height > rect.y + rect.height:
                y = rect.y + rect.height - self.height
            else:
                y = self.y
        else:
            y = rect.y - int((self.height - rect.height)/2)
        return Rect(x, y, self.width, self.height)

    def clamp_ip(self, rect):
        """
        Move this rect within rect.
        """
        if self.width < rect.width:
            if self.x < rect.x:
                x = rect.x
            elif self.x + self.width > rect.x + rect.width:
                x = rect.x + rect.width - self.width
            else:
                x = self.x
        else:
            x = rect.x - int((self.width - rect.width)/2)
        if self.height < rect.height:
            if self.y < rect.y:
                y = rect.y
            elif self.y + self.height > rect.y + rect.height:
                y = rect.y + rect.height - self.height
            else:
                y = self.y
        else:
            y = rect.y - int((self.height - rect.height)/2)
        self.setLocation(x, y)
        return None

    def set(self, *args):
        """
        Set rect x,y,width,height attributes to argument.
        Alternative arguments:
        * x,y,w,h
        * (x,y),(w,h)
        * (x,y,w,h)
        * Rect
        * Obj with rect attribute
        """
        if len(args) == 1:
            arg = args[0]
        else:
            arg = args
        ln = len(arg)
        if ln == 4:
            x = arg[0]
            y = arg[1]
            width = arg[2]
            height = arg[3]
        elif ln == 2:
            x = arg[0][0]
            y = arg[0][1]
            width = arg[1][0]
            height = arg[1][1]
        else:
            if hasattr(arg, 'rect'):
                arg = arg.rect
            x = arg.x
            y = arg.y
            width = arg.width
            height = arg.height
        object.__setattr__(self, 'x', int(x))
        object.__setattr__(self, 'y', int(y))
        object.__setattr__(self, 'width', int(width))
        object.__setattr__(self, 'height', int(height))

    def collidepoint(self, *point):
        """
        Return True if point is in this rect.
        """
        if len(point) == 2:
            return (self.x <= point[0] < (self.x + self.width) and
                    self.y <= point[1] < (self.y + self.height))
        else:
            return (self.x <= point[0][0] < (self.x + self.width) and
                    self.y <= point[0][1] < (self.y + self.height))

    def colliderect(self, rect):
        """
        Return True if rect collides with this rect.
        """
        return self.intersects(rect)

    def collidelist(self, rects):
        """
        Return index of rect in list that collide with this rect, otherwise returns -1.
        """
        for i, rect in enumerate(rects):
            if self.intersects(rect):
                return i
        return -1

    def collidelistall(self, rects):
        """
        Return list of indices of rects list that collide with this rect.
        """
        collided = []
        for i, rect in enumerate(rects):
            if self.colliderect(rect):
                collided.append(i)
        return collided

    def collidedict(self, rects):
        """
        Return (key,value) of first rect from rects dict that collide with this rect, otherwise returns None.
        """
        for rect in rects:
            if self.colliderect(rects[rect]):
                return (rect,rects[rect])
        return None

    def collidedictall(self, rects):
        """
        Return list of (key,value) from rects dict that collide with this rect.
        """
        collided = []
        for rect in rects:
            if self.colliderect(rects[rect]):
                collided.append((rect,rects[rect]))
        return collided

    def _get_center(self):
        return (self.x+(self.width//2), self.y+(self.height//2))

    def _get_centerx(self):
        return self.x+(self.width//2)

    def _get_centery(self):
        return self.y+(self.height//2)

    def _get_top(self):
        return self.y

    def _get_left(self):
        return self.x

    def _get_bottom(self):
        return self.y+self.height

    def _get_right(self):
        return self.x+self.width

    def _get_topleft(self):
        return (self.x, self.y)

    def _get_bottomleft(self):
        return (self.x, self.y+self.height)

    def _get_topright(self):
        return (self.x+self.width, self.y)

    def _get_bottomright(self):
        return (self.x+self.width, self.y+self.height)

    def _get_midtop(self):
        return (self.x+(self.width//2), self.y)

    def _get_midleft(self):
        return (self.x, self.y+(self.height//2))

    def _get_midbottom(self):
        return (self.x+(self.width//2), self.y+self.height)

    def _get_midright(self):
        return (self.x+self.width, self.y+(self.height//2))

    def _get_size(self):
        return (self.width, self.height)

    def _get_w(self):
        return self.width

    def _get_h(self):
        return self.height

    def _set_x(self, val):
        object.__setattr__(self, 'x', int(val))

    def _set_y(self, val):
        object.__setattr__(self, 'y', int(val))

    def _set_width(self, val):
        object.__setattr__(self, 'width', int(val))

    def _set_height(self, val):
        object.__setattr__(self, 'height', int(val))

    def _set_center(self, val):
        self.setLocation(val[0]-(self.width//2), val[1]-(self.height//2))

    def _set_centerx(self, val):
        self.setLocation(val-(self.width//2), self.y)

    def _set_centery(self, val):
        self.setLocation(self.x, val-(self.height//2))

    def _set_top(self, val):
        self.setLocation(self.x, val)

    def _set_left(self, val):
        self.setLocation(val, self.y)

    def _set_bottom(self, val):
        self.setLocation(self.x, val-self.height)

    def _set_right(self, val):
        self.setLocation(val-self.width, self.y)

    def _set_topleft(self, val):
        self.setLocation(val[0], val[1])

    def _set_bottomleft(self, val):
        self.setLocation(val[0], val[1]-self.height)

    def _set_topright(self, val):
        self.setLocation(val[0]-self.width, val[1])

    def _set_bottomright(self, val):
        self.setLocation(val[0]-self.width, val[1]-self.height)

    def _set_midtop(self, val):
        self.setLocation(val[0]-(self.width//2), val[1])

    def _set_midleft(self, val):
        self.setLocation(val[0], val[1]-(self.height//2))

    def _set_midbottom(self, val):
        self.setLocation(val[0]-(self.width//2), val[1]-self.height)

    def _set_midright(self, val):
        self.setLocation(val[0]-self.width, val[1]-(self.height//2))

    def _set_size(self, val):
        self.setSize(val[0], val[1])

    def _set_w(self, val):
        self.setSize(val, self.height)

    def _set_h(self, val):
        self.setSize(self.width, val)

    size = property(_get_size, _set_size)
    center = property(_get_center, _set_center)
    centerx = property(_get_centerx, _set_centerx)
    centery = property(_get_centery, _set_centery)
    top = property(_get_top, _set_top)
    left = property(_get_left, _set_left)
    bottom = property(_get_bottom, _set_bottom)
    right = property(_get_right, _set_right)
    topleft = property(_get_topleft, _set_topleft)
    bottomleft = property(_get_bottomleft, _set_bottomleft)
    topright = property(_get_topright, _set_topright)
    bottomright = property(_get_bottomright, _set_bottomright)
    midtop = property(_get_midtop, _set_midtop)
    midleft = property(_get_midleft, _set_midleft)
    midbottom = property(_get_midbottom, _set_midbottom)
    midright = property(_get_midright, _set_midright)
    w = property(_get_w, _set_w)
    h = property(_get_h, _set_h)


class RectPool(list):
    """
    **pyjsdl.rect.rectPool**
    
    * rectPool.append
    * rectPool.extend
    * rectPool.get
    * rectPool.copy

    Rect pool accessed by rectPool instance through append method to add Rect, extend method to add Rect list, get method to return Rect set with x,y,width,height attributes, and copy method to return copy of a given Rect. If pool is empty, return is a new Rect.
    """

    def __init__(self):
        list.__init__(self)
        self.add = self.append
        self.addAll = self.extend

    def get(self, x, y, width, height):
        """
        Return a Rect with x,y,width,height attributes.
        """
        if self:
            rect = self.pop()
            rect.x = x
            rect.y = y
            rect.width = width
            rect.height = height
            return rect
        else:
            return Rect(x,y,width,height)

    def copy(self, r):
        """
        Return a Rect with x,y,width,height attributes of the Rect argument.
        """
        if self:
            rect = self.pop()
            rect.x = r.x
            rect.y = r.y
            rect.width = r.width
            rect.height = r.height
            return rect
        else:
            return Rect(r.x, r.y, r.width, r.height)

rectPool = RectPool()

