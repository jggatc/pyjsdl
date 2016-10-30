#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from pyjsdl import env

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

    _xy = {
        'center': lambda self,val: self.setLocation( val[0]-int(self.width/2), val[1]-int(self.height/2) ),
        'centerx': lambda self,val: self.setLocation( val-int(self.width/2), self.y ),
        'centery': lambda self,val: self.setLocation( self.x, val-int(self.height/2) ),
        'top': lambda self,val: self.setLocation( self.x, val ),
        'left': lambda self,val: self.setLocation( val, self.y ),
        'bottom': lambda self,val: self.setLocation( self.x, val-self.height ),
        'right': lambda self,val: self.setLocation( val-self.width, self.y ),
        'topleft': lambda self,val: self.setLocation( val[0], val[1] ),
        'bottomleft': lambda self,val: self.setLocation( val[0], val[1]-self.height ),
        'topright': lambda self,val: self.setLocation( val[0]-self.width, val[1] ),
        'bottomright': lambda self,val: self.setLocation( val[0]-self.width, val[1]-self.height ),
        'midtop': lambda self,val: self.setLocation( val[0]-int(self.width/2), val[1] ),
        'midleft': lambda self,val: self.setLocation( val[0], val[1]-int(self.height/2) ),
        'midbottom': lambda self,val: self.setLocation( val[0]-int(self.width/2), val[1]-self.height ),
        'midright': lambda self,val: self.setLocation( val[0]-self.width, val[1]-int(self.height/2) ),
        'size': lambda self,val: self.setSize( val[0], val[1] ),
        'width': lambda self,val: self.setSize( val, self.height ),
        'height':lambda self,val: self.setSize( self.width, val ),
        'w': lambda self,val: self.setSize( val, self.height ),
        'h': lambda self,val: self.setSize( self.width, val ),
        'x': lambda self,val: self.setLocation( val, self.y ),
        'y': lambda self,val: self.setLocation( self.x, val )
          }
    _at = {
        'center': lambda self: (self.x+int(self.width/2), self.y+int(self.height/2)),
        'centerx': lambda self: self.x+int(self.width/2),
        'centery': lambda self: self.y+int(self.height/2),
        'top': lambda self: self.y,
        'left': lambda self: self.x,
        'bottom': lambda self: self.y+self.height,
        'right': lambda self: self.x+self.width,
        'topleft': lambda self: (self.x, self.y),
        'bottomleft': lambda self: (self.x, self.y+self.height),
        'topright': lambda self: (self.x+self.width, self.y),
        'bottomright': lambda self: (self.x+self.width, self.y+self.height),
        'midtop': lambda self: (self.x+int(self.width/2), self.y),
        'midleft': lambda self: (self.x, self.y+int(self.height/2)),
        'midbottom': lambda self: (self.x+int(self.width/2), self.y+self.height),
        'midright': lambda self: (self.x+self.width, self.y+int(self.height/2)),
        'size': lambda self: (self.width, self.height),
        'w': lambda self: self.width,
        'h': lambda self: self.height
          }

    def __init__(self, *args):
        """
        Return Rect object.
        
        Alternative arguments:
        
        * x,y,w,h
        * (x,y),(w,h)
        * (x,y,w,h)
        * Rect
        * Obj with rect attribute

        Rect has the attributes::
        
            x, y, width, height
        
        Additional Rect attributes::
        
            top, left, bottom, right, topleft, bottomleft, topright, bottomright,
            midtop, midleft, midbottom, midright, center, centerx, centery,
            size, w, h.
        
        Module initialization places pyjsdl.Rect in module's namespace.
        """
        if len(args) == 1:
            arg = args[0]
        else:
            arg = args
        ln = len(arg)
        if ln == 4:
            self.setLocation(arg[0], arg[1])
            self.setSize(arg[2], arg[3])
        elif ln == 2:
            self.setLocation(arg[0][0], arg[0][1])
            self.setSize(arg[1][0], arg[1][1])
        else:
            if hasattr(arg, 'rect'):
                arg = arg.rect
            self.setLocation(arg.x, arg.y)
            self.setSize(arg.width, arg.height)

    def __str__(self):
        """
        Return string representation of Rect object.
        """
        return "<rect(%d, %d, %d, %d)>" % (self.x, self.y, self.width, self.height)

    def __repr__(self):
        """
        Return string representation of Rect object.
        """
        return "%s(%d,%d,%d,%d)" % (self.__class__, self.x, self.y, self.width, self.height)

    def __getattr__(self, attr):   #not implemented in pyjs -O
        """
        Get Rect attributes.
        """
        if attr in self._at:
            return self._at[attr](self)
        else:
            raise AttributeError

    def __setattr__(self, attr, val):   #not implemented in pyjs -O
        """
        Set Rect attributes.
        """
        if attr in self._xy:
            self._xy[attr](self, val)
            return None
        else:
            raise AttributeError

    def __getitem__(self, key):
        """
        Get Rect [x,y,width,height] attributes by index.
        """
        return [self.x, self.y, self.width, self.height][key]

    def __setitem__(self, key, val):
        """
        Set Rect [x,y,width,height] attributes by index.
        """
        value = int(val)
        [lambda value: self.__setattr__("x", value), lambda value: self.__setattr__("y", value), lambda value: self.__setattr__("width", value), lambda value: self.__setattr__("height", value)][key](value)

    def __iter__(self):
        """
        Provides iterator to Rect.
        """
        return iter([self.x, self.y, self.width, self.height])

    def __len__(self):
        return 4

    def __nonzero__(self):
        """
        Rect nonzero check.
        """
        return self.width and self.height

    def __eq__(self, other):
        """
        Rects equality check.
        """
        return self.x==other.x and self.y==other.y and self.width==other.width and self.height==other.height    #pyjs compares rect==tuple not __eq__

    def __ne__(self, other):
        """
        Rects equality check.
        """
        return self.x!=other.x or self.y!=other.y or self.width!=other.width or self.height!=other.height   #pyjs compares rect==tuple not __eq__

    def setLocation(self, x, y):
        self.x = int(x)
        self.y = int(y)
        return None

    def setSize(self, w, h):
        self.width = int(w)
        self.height = int(h)
        return None

    def _setLocation(self, x, y):
        super(Rect, self).__setattr__('x', int(x))
        super(Rect, self).__setattr__('y', int(y))
        return None

    def _setSize(self, w, h):
        super(Rect, self).__setattr__('width', int(w))
        super(Rect, self).__setattr__('height', int(h))
        return None

    def copy(self):
        """
        Returns Rect that is a copy of this rect.
        """
        return Rect(self.x, self.y, self.width, self.height)

    def move(self, x, y):
        """
        Return Rect of same dimension at position offset by x,y.
        """
        return Rect(self.x+x, self.y+y, self.width, self.height)

    def move_ip(self, *pos):
        """
        Moves this rect to position offset by x,y.
        """
        if len(pos) == 2:
            self.setLocation(self.x+pos[0], self.y+pos[1])
        else:
            self.setLocation(self.x+pos[0][0], self.y+pos[0][1])
        return None

    def inflate(self, x, y):
        """
        Return Rect at same position but size offset by x,y.
        """
        return Rect(self.x-int(float(x)/2), self.y-int(float(y)/2), self.width+x, self.height+y)

    def inflate_ip(self, x, y):
        """
        Change size of this rect offset by x,y.
        """
        self.setSize(self.width+x, self.height+y)
        self.setLocation(self.x-int(float(x)/2), self.y-int(float(y)/2))
        return None

    def clip(self, rect):
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
        return self.clip(rect)

    def contains(self, rect):
        """
        Check if rect is in this rect.
        """
        return (self.x <= rect.x and (self.x+self.width) >= (rect.x+rect.width) and self.y <= rect.y and (self.y+self.height) >= (rect.y+rect.height))

    def intersects(self, rect):
        return (self.x < (rect.x+rect.width) and rect.x < (self.x+self.width) and self.y < (rect.y+rect.height) and rect.y < (self.y+self.height))

    def union(self, rect):
        """
        Return Rect representing the union of rect and this rect.
        """
        x = self.x if self.x < rect.x else rect.x
        y = self.y if self.y < rect.y else rect.y
        s = self.x+self.width
        r = rect.x+rect.width
        w = (s if s > r else r) - x
        s = self.y+self.height
        r = rect.y+rect.height
        h = (s if s > r else r) - y
        return Rect(x, y, w, h)

    def union_ip(self, rect):
        """
        Change this rect to represent the union of rect and this rect.
        """
        x = self.x if self.x < rect.x else rect.x
        y = self.y if self.y < rect.y else rect.y
        s = self.x+self.width
        r = rect.x+rect.width
        w = (s if s > r else r) - x
        s = self.y+self.height
        r = rect.y+rect.height
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
        x2 = self.x+self.width
        y2 = self.y+self.height
        for r in rect_list:
            if r.x < x1:
                x1 = r.x
            if r.y < y1:
                y1 = r.y
            rx2 = r.x+r.width
            if rx2 > x2:
                x2 = rx2
            ry2 = r.y+r.height
            if ry2 > y2:
                y2 = ry2
        return Rect(x1,y1,x2-x1,y2-y1)

    def unionall_ip(self, rect_list):
        """
        Change this rect to represent the union of rect list and this rect.
        """
        x1 = self.x
        y1 = self.y
        x2 = self.x+self.width
        y2 = self.y+self.height
        for r in rect_list:
            if r.x < x1:
                x1 = r.x
            if r.y < y1:
                y1 = r.y
            rx2 = r.x+r.width
            if rx2 > x2:
                x2 = rx2
            ry2 = r.y+r.height
            if ry2 > y2:
                y2 = ry2
        self.x = x1
        self.y = y1
        self.width = x2-x1
        self.height = y2-y1
        return None

    def clamp(self, rect):
        """
        Return Rect of same dimension as this rect moved within rect.
        """
        if self.width < rect.width:
            if self.x < rect.x:
                x = rect.x
            elif self.x+self.width > rect.x+rect.width:
                x = rect.x+rect.width-self.width
            else:
                x = self.x
        else:
            x = rect.x-int((self.width-rect.width)/2)
        if self.height < rect.height:
            if self.y < rect.y:
                y = rect.y
            elif self.y+self.height > rect.y+rect.height:
                y = rect.y+rect.height-self.height
            else:
                y = self.y
        else:
            y = rect.y-int((self.height-rect.height)/2)
        return Rect(x, y, self.width, self.height)

    def clamp_ip(self, rect):
        """
        Move this rect within rect.
        """
        if self.width < rect.width:
            if self.x < rect.x:
                x = rect.x
            elif self.x+self.width > rect.x+rect.width:
                x = rect.x+rect.width-self.width
            else:
                x = self.x
        else:
            x = rect.x-int((self.width-rect.width)/2)
        if self.height < rect.height:
            if self.y < rect.y:
                y = rect.y
            elif self.y+self.height > rect.y+rect.height:
                y = rect.y+rect.height-self.height
            else:
                y = self.y
        else:
            y = rect.y-int((self.height-rect.height)/2)
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
            self.setLocation(arg[0], arg[1])
            self.setSize(arg[2], arg[3])
        elif ln == 2:
            self.setLocation(arg[0][0], arg[0][1])
            self.setSize(arg[1][0], arg[1][1])
        else:
            if hasattr(arg, 'rect'):
                arg = arg.rect
            self.setLocation(arg.x, arg.y)
            self.setSize(arg.width, arg.height)

    def collidepoint(self, *point):
        """
        Return True if point is in this rect.
        """
        if len(point) == 2:
            return (self.x <= point[0] < (self.x+self.width) and self.y <= point[1] < (self.y+self.height))
        else:
            return (self.x <= point[0][0] < (self.x+self.width) and self.y <= point[0][1] < (self.y+self.height))

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


if env.pyjs_mode.strict:
    Rect.setLocation = Rect._setLocation
    Rect.setSize = Rect._setSize


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

