#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl import env
from math import sqrt, sin, cos, atan2, pi, floor


class Vector2(object):
    """
    Vector2 - 2-dimensional vector.

    Build in --optimized mode (-O) lack type enforcement
    with attribute assignment, so ensure use of floats.
    To enable type enforcement use --enable-descriptor-proto,
    however doing so has a moderate performance impact.
    To enable arithmetic operation functionality, use
    --enable-operator-funcs with minimal performance impact.
    """

    __slots__ = ['x', 'y']

    def __init__(self, *args, **kwargs):
        l = len(args)
        if l == 2:
            self.x = float(args[0])
            self.y = float(args[1])
        elif l == 1:
            if isinstance(args[0], (int, float)):
                self.x = float(args[0])
                self.y = float(args[0])
            else:
                self.x = float(args[0][0])
                self.y = float(args[0][1])
        else:
            if kwargs:
                if 'x' in kwargs and 'y' in kwargs:
                    self.x = float(kwargs['x'])
                    self.y = float(kwargs['y'])
                elif 'x' in kwargs:
                    self.x = float(kwargs['x'])
                    self.y = float(kwargs['x'])
                else:
                    self.x = float(kwargs['y'])
                    self.y = float(kwargs['y'])
            else:
                self.x = 0.0
                self.y = 0.0

    def __str__(self):
        return '[%g, %g]' % (self.x, self.y)

    def __repr__(self):
        return '<%s(%g, %g)>' % (self.__class__.__name__,
                                 self.x, self.y)

    def __getitem__(self, index):
        if index in (0, -2):
            return self.x
        elif index in (1, -1):
            return self.y
        elif isinstance(index, slice):
            return [self.x, self.y][index]
        else:
            raise IndexError

    def __setitem__(self, index, val):
        if index == 0:
            try:
                self.x = float(val)
            except ValueError:
                raise TypeError
        elif index == 1:
            try:
                self.y = float(val)
            except ValueError:
                raise TypeError
        elif isinstance(index, slice):
            l = [self.x, self.y]
            l[index] = val
            if len(l) != 2:
                raise ValueError
            self.x = float(l[0])
            self.y = float(l[1])
        else:
            raise IndexError

    def __delitem__(self, index):
        raise TypeError(
            'Deletion of vector components is not supported')

    def __getslice__(self, start, stop):
        return [self.x, self.y][start:stop]

    def __setslice__(self, lower, upper, val):
        l = [self.x, self.y]
        l[lower:upper] = val
        if len(l) != 2:
            raise ValueError
        self.x = float(l[0])
        self.y = float(l[1])

    def __iter__(self):
        for val in (self.x, self.y):
            yield val

    def __len__(self):
        return 2

    def __bool__(self):
        return bool(self.x or self.y)

    def __nonzero__(self):
        return bool(self.x or self.y)

    def dot(self, vector):
        """
        Return dot product with other vector.
        """
        return (self.x * vector[0]) + (self.y * vector[1])

    def cross(self, vector):
        """
        Return cross product with other vector.
        """
        return (self.x * vector[1]) - (self.y * vector[0])

    def magnitude(self):
        """
        Return magnitude of vector.
        """
        return sqrt((self.x**2) + (self.y**2))

    def magnitude_squared(self):
        """
        Return squared magnitude of vector.
        """
        return ((self.x**2) + (self.y**2))

    def length(self):
        #js keyword, use magnitude.
        """
        Return length of vector.
        """
        return sqrt((self.x**2) + (self.y**2))

    def length_squared(self):
        """
        Return squared length of vector.
        """
        return ((self.x**2) + (self.y**2))

    def normalize(self):
        """
        Return normalized vector.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError('Cannot normalize vector of zero length')
        return Vector2(self.x / mag, self.y / mag)

    def normalize_ip(self):
        """
        Normalized this vector.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError('Cannot normalize vector of zero length')
        self.x /= mag
        self.y /= mag
        return None

    def is_normalized(self):
        """
        Check whether vector is normalized.
        """
        return self.magnitude() == 1

    def scale_to_length(self, length):
        """
        Scale vector to length.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError('Cannot scale vector of zero length')
        self.x = (self.x / mag) * length
        self.y = (self.y / mag) * length
        return None

    def reflect(self, vector):
        """
        Return reflected vector at given vector.
        """
        vn = (self.x * vector[0]) + (self.y * vector[1])
        nn = (vector[0] * vector[0]) + (vector[1] * vector[1])
        if nn == 0:
            raise ValueError('Cannot reflect from normal of zero length')
        c = 2 * vn / nn
        return Vector2(self.x - (vector[0] * c),
                       self.y - (vector[1] * c))

    def reflect_ip(self, vector):
        """
        Derive reflected vector at given vector in place.
        """
        vn = (self.x * vector[0]) + (self.y * vector[1])
        nn = (vector[0] * vector[0]) + (vector[1] * vector[1])
        if nn == 0:
            raise ValueError('Cannot reflect from normal of zero length')
        c = 2 * vn / nn
        self.x -= (vector[0] * c)
        self.y -= (vector[1] * c)
        return None

    def distance_to(self, vector):
        """
        Return distance to given vector.
        """
        return sqrt((self.x - vector[0])**2
                  + (self.y - vector[1])**2)

    def distance_squared_to(self, vector):
        """
        Return squared distance to given vector.
        """
        return ((self.x - vector[0])**2
              + (self.y - vector[1])**2)

    def lerp(self, vector, t):
        """
        Return vector linear interpolated by t to the given vector.
        """
        if t < 0.0 or t > 1.0:
            raise ValueError('Argument t must be in range 0 to 1')
        return Vector2(self.x * (1-t) + vector[0] * t,
                       self.y * (1-t) + vector[1] * t)

    def slerp(self, vector, t):
        """
        Return vector spherical interpolated by t to the given vector.
        """
        if t < -1.0 or t > 1.0:
            raise ValueError('Argument t must be in range -1 to 1')
        if not hasattr(vector, '__len__') or len(vector) != 2:
            raise TypeError('The first argument must be a vector')
        smag = sqrt((self.x**2) + (self.y**2))
        vmag = sqrt((vector[0]**2) + (vector[1]**2))
        if smag==0 or vmag==0:
            raise ValueError('Cannot use slerp with zero-vector')
        sx = self.x / smag
        sy = self.y / smag
        vx = vector[0] / vmag
        vy = vector[1] / vmag
        theta = atan2(vy, vx) - atan2(sy, sx)
        _theta = abs(theta)
        if _theta-pi > 0.000001:
            theta -= (2*pi) * (theta / _theta)
        elif -0.000001 < _theta-pi < 0.000001:
            raise ValueError('Cannot use slerp on 180 degrees')
        if t < 0.0:
            t = -t
            theta -= (2*pi) * (theta / abs(theta))
        sin_theta = sin(theta)
        if sin_theta:
            a = sin((1.0-t) * theta) / sin_theta
            b = sin(t * theta) / sin_theta
        else:
            a = 1.0
            b = 0.0
        v = Vector2((sx * a) + (vx * b),
                    (sy * a) + (vy * b))
        smag = ((1.0-t) * smag) + (t * vmag)
        v.x *= smag
        v.y *= smag
        return v

    def elementwise(self):
        """
        Elementwice operation.
        """
        return VectorElementwiseProxy(self.x, self.y)

    def rotate(self, angle):
        """
        Return vector rotated by angle in degrees.
        """
        rad = angle / 180.0 * pi
        c = round(cos(rad), 6)
        s = round(sin(rad), 6)
        return Vector2((c * self.x) - (s * self.y),
                       (s * self.x) + (c * self.y))

    def rotate_rad(self, angle):
        """
        Return vector rotated by angle in radians.
        """
        c = cos(angle)
        s = sin(angle)
        return Vector2((c * self.x) - (s * self.y),
                       (s * self.x) + (c * self.y))

    def rotate_ip(self, angle):
        """
        Rotate vector by angle in degrees.
        """
        r = angle / 180.0 * pi
        c = round(cos(r), 6)
        s = round(sin(r), 6)
        x = self.x
        y = self.y
        self.x = (c * x) - (s * y)
        self.y = (s * x) + (c * y)
        return None

    def rotate_ip_rad(self, angle):
        """
        Rotate vector by angle in radians.
        """
        c = cos(angle)
        s = sin(angle)
        x = self.x
        y = self.y
        self.x = (c * x) - (s * y)
        self.y = (s * x) + (c * y)
        return None

    def angle_to(self, vector):
        """
        Return angle to given vector.
        """
        return (atan2(vector[1], vector[0])
                - atan2(self.y, self.x)) * (180.0 / pi)

    def as_polar(self):
        """
        Return radial distance and azimuthal angle.
        """
        r = self.magnitude()
        phi = atan2(self.y, self.x) * (180.0 / pi)
        return (r, phi)

    def from_polar(self, coordinate):
        """
        Set vector with polar coordinate tuple.
        """
        if len(coordinate) != 2:
            raise TypeError('coodinate must be of length 2')
        r = coordinate[0]
        phi = coordinate[1] * (pi / 180.0)
        self.x = round(r * cos(phi), 6)
        self.y = round(r * sin(phi), 6)
        return None

    def update(self, *args, **kwargs):
        """
        Update vector.
        """
        l = len(args)
        if l == 2:
            self.x = float(args[0])
            self.y = float(args[1])
        elif l == 1:
            if isinstance(args[0], (int, float)):
                self.x = float(args[0])
                self.y = float(args[0])
            else:
                self.x = float(args[0][0])
                self.y = float(args[0][1])
        else:
            if kwargs:
                if 'x' in kwargs and 'y' in kwargs:
                    self.x = float(kwargs['x'])
                    self.y = float(kwargs['y'])
                elif 'x' in kwargs:
                    self.x = float(kwargs['x'])
                    self.y = float(kwargs['x'])
                else:
                    self.x = float(kwargs['y'])
                    self.y = float(kwargs['y'])
            else:
                self.x = 0.0
                self.y = 0.0

    def __pos__(self):
        return Vector2(self.x, self.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self.x + other[0], self.y + other[1])
        else:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self.x - other[0], self.y - other[1])
        else:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if hasattr(other, '__iter__'):
            if not isinstance(other, VectorElementwiseProxy):
                return (self.x * other[0]) + (self.y * other[1])
            else:
                return Vector2(self.x * other[0], self.y * other[1])
        else:
            return Vector2(self.x * other, self.y * other)

    def __div__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self.x / other[0], self.y / other[1])
        else:
            return Vector2(self.x / other, self.y / other)

    def __truediv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self.x / other[0], self.y / other[1])
        else:
            return Vector2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(floor(self.x/other[0]), floor(self.y/other[1]))
        else:
            return Vector2(floor(self.x/other), floor(self.y/other))

    def __eq__(self, other):
        if hasattr(other, '__iter__'):
            if len(other) == 2:
                return ( abs(self.x - other[0]) < 0.000001 and
                         abs(self.y - other[1]) < 0.000001 )
            else:
                return False
        else:
            return ( abs(self.x - other) < 0.000001 and
                     abs(self.y - other) < 0.000001 )

    def __ne__(self, other):
        if hasattr(other, '__iter__'):
            if len(other) == 2:
                return ( abs(self.x - other[0]) > 0.000001 or
                         abs(self.y - other[1]) > 0.000001 )
            else:
                return True
        else:
            return ( abs(self.x - other) > 0.000001 or
                     abs(self.y - other) > 0.000001 )

    def __gt__(self, other):
        if not isinstance(other, VectorElementwiseProxy):
            msg = 'This operation is not supported by vectors'
            raise TypeError(msg)
        return NotImplemented

    def __ge__(self, other):
        if not isinstance(other, VectorElementwiseProxy):
            msg = 'This operation is not supported by vectors'
            raise TypeError(msg)
        return NotImplemented

    def __lt__(self, other):
        if not isinstance(other, VectorElementwiseProxy):
            msg = 'This operation is not supported by vectors'
            raise TypeError(msg)
        return NotImplemented

    def __le__(self, other):
        if not isinstance(other, VectorElementwiseProxy):
            msg = 'This operation is not supported by vectors'
            raise TypeError(msg)
        return NotImplemented

    def __radd__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self.x + other[0], self.y + other[1])
        else:
            return Vector2(self.x + other, self.y + other)

    def __rsub__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(other[0] - self.x, other[1] - self.y)
        else:
            return Vector2(other - self.x, other - self.y)

    def __rmul__(self, other):
        if hasattr(other, '__iter__'):
            if not isinstance(other, VectorElementwiseProxy):
                return (self.x * other[0]) + (self.y * other[1])
            else:
                return Vector2(self.x * other[0], self.y * other[1])
        else:
            return Vector2(self.x * other, self.y * other)

    def __rdiv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(other[0] / self.x, other[1] / self.y)
        else:
            return Vector2(other / self.x, other / self.y)

    def __rtruediv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(other[0] / self.x, other[1] / self.y)
        else:
            return Vector2(other / self.x, other / self.y)

    def __rfloordiv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(floor(other[0]/self.x), floor(other[1]/self.y))
        else:
            return Vector2(floor(other/self.x), floor(other/self.y))

    def __iadd__(self, other):
        if hasattr(other, '__iter__'):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    def __isub__(self, other):
        if hasattr(other, '__iter__'):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    def __imul__(self, other):
        if hasattr(other, '__iter__'):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    def __idiv__(self, other):
        if hasattr(other, '__iter__'):
            self.x /= other[0]
            self.y /= other[1]
        else:
            self.x /= other
            self.y /= other
        return self

    def __itruediv__(self, other):
        if hasattr(other, '__iter__'):
            self.x /= other[0]
            self.y /= other[1]
        else:
            self.x /= other
            self.y /= other
        return self

    def __ifloordiv__(self, other):
        if hasattr(other, '__iter__'):
            self.x = float(floor(self.x / other[0]))
            self.y = float(floor(self.y / other[1]))
        else:
            self.x = float(floor(self.x / other))
            self.y = float(floor(self.y / other))
        return self


class _Vector2(Vector2):
    """
    Vector2 - 2-dimensional vector.
    """

    __slots__ = ['_x', '_y']

    def __init__(self, *args, **kwargs):
        l = len(args)
        if l == 2:
            self._x = float(args[0])
            self._y = float(args[1])
        elif l == 1:
            if isinstance(args[0], (int, float)):
                self._x = float(args[0])
                self._y = float(args[0])
            else:
                self._x = float(args[0][0])
                self._y = float(args[0][1])
        else:
            if kwargs:
                if 'x' in kwargs and 'y' in kwargs:
                    self._x = float(kwargs['x'])
                    self._y = float(kwargs['y'])
                elif 'x' in kwargs:
                    self._x = float(kwargs['x'])
                    self._y = float(kwargs['x'])
                else:
                    self._x = float(kwargs['y'])
                    self._y = float(kwargs['y'])
            else:
                self._x = 0.0
                self._y = 0.0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        try:
            self._x = float(val)
        except ValueError:
            raise TypeError('float is required')

    @x.deleter
    def x(self):
        raise TypeError('Cannot delete the x attribute')

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        try:
            self._y = float(val)
        except ValueError:
            raise TypeError('float is required')

    @y.deleter
    def y(self):
        raise TypeError('Cannot delete the y attribute')

    def __repr__(self):
        return '<%s(%g, %g)>' % (self.__class__.__name__[1:],
                                 self.x, self.y)


if env.pyjs_mode.test_getattr():
    #-S mode or -O --enable-descriptor-proto mode.
    Vector2 = _Vector2


class VectorElementwiseProxy(object):

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __getitem__(self, index):
        if index in (0, -2):
            return self._x
        elif index in (1, -1):
            return self._y

    def __iter__(self):
        for val in (self._x, self._y):
            yield val

    def __len__(self):
        return 2

    def __bool__(self):
        return bool(self._x or self._y)

    def __nonzero__(self):
        return bool(self._x or self._y)

    def __pos__(self):
        return Vector2(self._x, self._y)

    def __neg__(self):
        return Vector2(-self._x, -self._y)

    def __abs__(self):
        return (abs(self._x), abs(self._y))

    def __add__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self._x + other[0], self._y + other[1])
        else:
            return Vector2(self._x + other, self._y + other)

    def __sub__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self._x - other[0], self._y - other[1])
        else:
            return Vector2(self._x - other, self._y - other)

    def __mul__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self._x * other[0], self._y * other[1])
        else:
            return Vector2(self._x * other, self._y * other)

    def __div__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self._x / other[0], self._y / other[1])
        else:
            return Vector2(self._x / other, self._y / other)

    def __truediv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self._x / other[0], self._y / other[1])
        else:
            return Vector2(self._x / other, self._y / other)

    def __floordiv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(floor(self._x/other[0]), floor(self._y/other[1]))
        else:
            return Vector2(floor(self._x/other), floor(self._y/other))

    def __pow__(self, other):
        if hasattr(other, '__iter__'):
            if (other[0]%1 and self._x<0) or (other[1]%1 and self._y<0):
                raise ValueError(
                    'negative number cannot be raised to a fractional power')
            return Vector2(self._x ** other[0], self._y ** other[1])
        else:
            if other%1 and (self._x<0 or self._y<0):
                raise ValueError(
                    'negative number cannot be raised to a fractional power')
            return Vector2(self._x ** other, self._y ** other)

    def __mod__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self._x % other[0], self._y % other[1])
        else:
            return Vector2(self._x % other, self._y % other)

    def __eq__(self, other):
        if hasattr(other, '__iter__'):
            if len(other) == 2:
                return ( abs(self._x - other[0]) < 0.000001 and
                         abs(self._y - other[1]) < 0.000001 )
            else:
                return False
        else:
            return ( abs(self._x - other) < 0.000001 and
                     abs(self._y - other) < 0.000001 )

    def __ne__(self, other):
        if hasattr(other, '__iter__'):
            if len(other) == 2:
                return ( abs(self._x - other[0]) > 0.000001 or
                         abs(self._y - other[1]) > 0.000001 )
            else:
                return True
        else:
            return ( abs(self._x - other) > 0.000001 or
                     abs(self._y - other) > 0.000001 )

    def __gt__(self, other):
        if hasattr(other, '__iter__'):
            return bool(self._x > other[0] and self._y > other[1])
        else:
            return bool(self._x > other and self._y > other)

    def __ge__(self, other):
        if hasattr(other, '__iter__'):
            return bool(self._x >= other[0] and self._y >= other[1])
        else:
            return bool(self._x >= other and self._y >= other)

    def __lt__(self, other):
        if hasattr(other, '__iter__'):
            return bool(self._x < other[0] and self._y < other[1])
        else:
            return bool(self._x < other and self._y < other)

    def __le__(self, other):
        if hasattr(other, '__iter__'):
            return bool(self._x <= other[0] and self._y <= other[1])
        else:
            return bool(self._x <= other and self._y <= other)

    def __radd__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self._x + other[0], self._y + other[1])
        else:
            return Vector2(self._x + other, self._y + other)

    def __rsub__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(other[0] - self._x, other[1] - self._y)
        else:
            return Vector2(other - self._x, other - self._y)

    def __rmul__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(self._x * other[0], self._y * other[1])
        else:
            return Vector2(self._x * other, self._y * other)

    def __rdiv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(other[0] / self._x, other[1] / self._y)
        else:
            return Vector2(other / self._x, other / self._y)

    def __rtruediv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(other[0] / self._x, other[1] / self._y)
        else:
            return Vector2(other / self._x, other / self._y)

    def __rfloordiv__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(floor(other[0]/self._x), floor(other[1]/self._y))
        else:
            return Vector2(floor(other/self._x), floor(other/self._y))

    def __rpow__(self, other):
        if hasattr(other, '__iter__'):
            if (other[0]<0 and self._x%1) or (other[1]<0 and self._y%1):
                raise ValueError(
                    'negative number cannot be raised to a fractional power')
            return Vector2(other[0] ** self._x, other[1] ** self._y)
        else:
            if other<0 and (self._x%1 or self._y%1):
                raise ValueError(
                    'negative number cannot be raised to a fractional power')
            return Vector2(other ** self._x, other ** self._y)

    def __rmod__(self, other):
        if hasattr(other, '__iter__'):
            return Vector2(other[0] % self._x, other[1] % self._y)
        else:
            return Vector2(other % self._x, other % self._y)

