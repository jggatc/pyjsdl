#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division

__docformat__ = 'restructuredtext'


class Rect(object):
    """
    **pyjsdl.Rect**
    
    * Rect.copy
    * Rect.move
    * Rect.move_ip
    * Rect.inflate
    * Rect.inflate_ip
    * Rect.union
    * Rect.union_ip
    * Rect.unionall
    * Rect.unionall_ip
    * Rect.clip
    * Rect.collidepoint
    * Rect.colliderect
    * Rect.collidelist
    """

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
          }    #// > /    #int
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
          }    #// > /    #int

    def __init__(self, *arg):
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
        def unpack(arg, lst=[]):
            for x in arg:
                if not isinstance(x, tuple):
                    lst.append(x)
                else:
                    lst = unpack(x, lst)
            return lst
        try:
            x,y,w,h = arg[0], arg[1], arg[2], arg[3]
        except IndexError:
            try:
                x,y,w,h = arg[0][0], arg[0][1], arg[0][2], arg[0][3]
            except (IndexError, TypeError, AttributeError):
                arg = unpack(arg)
                try:
                    x,y,w,h = arg[0], arg[1], arg[2], arg[3]
                except IndexError:
                    if hasattr(arg[0], 'rect'):
                        arg[0] = arg[0].rect
                    x,y,w,h = arg[0].x, arg[0].y, arg[0].width, arg[0].height
        super(Rect, self).__setattr__('x', int(x))
        super(Rect, self).__setattr__('y', int(y))
        super(Rect, self).__setattr__('width', int(w))
        super(Rect, self).__setattr__('height', int(h))

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
        try:
            return Rect._at[attr](self)
        except KeyError:
            raise AttributeError

    def __setattr__(self, attr, val):   #not implemented in pyjs -O
        """
        Set Rect attributes.
        """
        try:
            Rect._xy[attr](self, val)
        except TypeError:
            try:
                Rect._xy[attr](self, int(val))
            except TypeError:
                Rect._xy[attr](self, (int(val[0]), int(val[1])))
        return None

    def __getitem__(self, key):
        """
        Get Rect [x,y,width,height] attributes by index.
        """
        return [self.x, self.y, self.width, self.height][key]

    def __setitem__(self, key, val):
        """
        Set Rect [x,y,width,height] attributes by index.
        """
        val = int(val)
        [lambda val: self.__setattr__("x", val), lambda val: self.__setattr__("y", val), lambda val: self.__setattr__("width", val), lambda val: self.__setattr__("height", val)][key](val)

    def __nonzero__(self):
        """
        Rect nonzero check.
        """
        if self.width and self.height:
            return True
        else:
            return False

    def __eq__(self, other):
        """
        Rects equality check.
        """
        try:
            return self.x==other.x and self.y==other.y and self.width==other.width and self.height==other.height
        except AttributeError:  #pyjs compares rect==tuple not __eq__
            return self.x==other[0] and self.y==other[1] and self.width==other[2] and self.height==other[3]

    def __ne__(self, other):
        """
        Rects equality check.
        """
        try:
            return self.x!=other.x or self.y!=other.y or self.width!=other.width or self.height!=other.height
        except AttributeError:  #pyjs compares rect==tuple not __eq__
            return self.x!=other[0] or self.y!=other[1] or self.width!=other[2] or self.height!=other[3]

    def setLocation(self, x, y):
        super(Rect, self).__setattr__('x', int(x))
        super(Rect, self).__setattr__('y', int(y))
        return None

    def setSize(self, w, h):
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
        try:
            x, y = pos
        except ValueError:
            x, y = pos[0]
        try:
            self.setLocation(self.x+x, self.y+y)
        except TypeError:
            self.setLocation(self.x+int(x), self.y+int(y))
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
            x = max(self.x, rect.x)
            y = max(self.y, rect.y)
            w = min(self.x+self.width, rect.x+rect.width) - x
            h = min(self.y+self.height, rect.y+rect.height) - y
            return Rect(x, y, w, h)

    def intersection(self, rect):
        return self.clip(rect)

    def contains(self, x, y):
        return (self.x < x and x < (self.x+self.width) and self.y < y and y < (self.y+self.height))

    def intersects(self, rect):
        return (self.x < (rect.x+rect.width) and rect.x < (self.x+self.width) and self.y < (rect.y+rect.height) and rect.y < (self.y+self.height))

    def union(self, rect):
        """
        Return Rect representing the union of rect and this rect.
        """
        return Rect(min(self.x,rect.x), min(self.y,rect.y), max(self.x+self.width,rect.x+rect.width), max(self.y+self.height,rect.y+rect.height))

    def union_ip(self, rect):
        """
        Change this rect to represent the union of rect and this rect.
        """
        self.setSize(max(self.x+self.width,rect.x+rect.width), max(self.y+self.height,rect.y+rect.height))
        self.setLocation(min(self.x,rect.x), min(self.y,rect.y))
        return None

    def unionall(self, rect_list):
        """
        Return Rect representing the union of rect list and this rect.
        """
        return Rect(min(self.x,min(r.x for r in rect_list)), min(self.y,min(r.y for r in rect_list)), max(self.x+self.width,max(r.x+r.width for r in rect_list)), max(self.y+self.height,max(r.y+r.height for r in rect_list)))

    def unionall_ip(self, rect_list):
        """
        Change this rect to represent the union of rect list and this rect.
        """
        self.setSize(max(self.x+self.width,max(r.x+r.width for r in rect_list)), max(self.y+self.height,max(r.y+r.height for r in rect_list)))
        self.setLocation(min(self.x,min(r.x for r in rect_list)), min(self.y,min(r.y for r in rect_list)))
        return None

    def collidepoint(self, *point):
        """
        Return True if point is in this rect.
        """
        try:
            x, y = point[0], point[1]
        except IndexError:
            x, y = point[0]
        return self.contains(x,y)

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
        try:
            rect = self.pop()
            rect.x, rect.y, rect.width, rect.height = x, y, width, height
            return rect
        except IndexError:
            return Rect(x,y,width,height)

    def copy(self, r):
        """
        Return a Rect with x,y,width,height attributes of the Rect argument.
        """
        try:
            rect = self.pop()
            rect.x, rect.y, rect.width, rect.height = r.x, r.y, r.width, r.height
            return rect
        except IndexError:
            return Rect(r.x, r.y, r.width, r.height)

rectPool = RectPool()

