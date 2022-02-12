#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.rect import rectPool
from pyjsdl import mask
import sys

if sys.version_info < (3,):
    from pyjsdl.util import _range as range
    from pyjsdl.util import _dict as dict
    from pyjsdl.util import _next as next

__docformat__ = 'restructuredtext'


def id(obj):
    return obj._identity


class Sprite(object):
    """
    **pyjsdl.sprite.Sprite**
    
    * Sprite.add
    * Sprite.remove
    * Sprite.kill
    * Sprite.alive
    * Sprite.groups
    * Sprite.update
    """

    _identity = 0

    def __init__(self, *groups):
        """
        Return Sprite.
        Optional argument inludes group(s) to place sprite.
        Sprite require image and rect attributes for some functionality.
        """
        self._identity = Sprite._identity
        Sprite._identity += 1
        self._groups = dict()
        if groups:
            self.add(*groups)

    def __str__(self):
        s = '<%s(in %d groups)>'
        return s % (self.__class__.__name__, len(self._groups))

    def __repr__(self):
        return self.__str__()

    def add(self, *groups):
        """
        Add sprite to group(s).
        """
        for group in groups:
            if hasattr(group, '_sprites'):
                group.add(self)
            else:
                self.add(*group)
        return None

    def remove(self, *groups):
        """
        Remove sprite from group(s).
        """
        for group in groups:
            if hasattr(group, '_sprites'):
                group.remove(self)
            else:
                self.remove(*group)
        return None

    def kill(self):
        """
        Remove sprite from all member groups.
        """
        for group in list(self._groups.values()):
            group.remove(self)
        return None

    def alive(self):
        """
        Return True if sprite is member of any groups.
        """
        if self._groups:
            return True
        else:
            return False

    def groups(self):
        """
        Return list of groups that sprite is a member.
        """
        return list(self._groups.values())

    def update(self, *args):
        """
        Method to place sprite update statements that is called by group update.
        """
        pass


class DirtySprite(Sprite):
    """
    **pyjsdl.sprite.Sprite**
    
    * Sprite subclass
    * subclass not implemented
    """

    def __init__(self, *groups):
        """
        Return Sprite.
        """
        Sprite.__init__(self, *groups)


class Group(object):
    """
    **pyjsdl.sprite.Group**
    
    * Group.sprites
    * Group.copy
    * Group.add
    * Group.remove
    * Group.has
    * Group.draw
    * Group.clear
    * Group.empty
    * Group.update
    """

    _identity = 0

    def __init__(self, *sprites):
        """
        Return Group.
        Can optionally be called with sprite(s) to add.
        """
        self._identity = Group._identity
        Group._identity += 1
        self._sprites = dict()
        if sprites:
            self.add(*sprites)
        self._clear_active = False
        self._sprites_drawn = dict()

    def __str__(self):
        s = '<%s(%d sprites)>'
        return s % (self.__class__.__name__, len(self._sprites))

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self._sprites.values())

    def __contains__(self, sprite):
        return id(sprite) in self._sprites

    def __len__(self):
        return len(self._sprites)

    def sprites(self):
        """
        Return list of sprites in the group.
        """
        return list(self._sprites.values())

    def copy(self):
        """
        Return copy of group.
        """
        newgroup = self.__class__()
        newgroup._sprites = self._sprites.copy()
        return newgroup

    def add(self, *sprites):
        """
        Add sprite(s) to group.
        """
        for sprite in sprites:
            if hasattr(sprite, '_groups'):
                spriteID = id(sprite)
                if spriteID not in self._sprites:
                    self._sprites[spriteID] = sprite
                    sprite._groups[id(self)] = self
            else:
                self.add(*sprite)
        return None

    def remove(self, *sprites):
        """
        Remove sprite(s) from group.
        """
        for sprite in sprites:
            if hasattr(sprite, '_groups'):
                spriteID = id(sprite)
                if spriteID in self._sprites:
                    del self._sprites[spriteID]
                    del sprite._groups[id(self)]
            else:
                self.remove(*sprite)
        return None

    def has(self, *sprites):
        """
        Check if all sprite(s) in group.
        """
        for sprite in sprites:
            if hasattr(sprite, '_groups'):
                if id(sprite) not in self._sprites:
                    return False
            else:
                if not self.has(*sprite):
                    return False
        return True

    def draw(self, surface):
        """
        Draw sprite on surface.
        """
        surface._blits([(sprite.image,sprite.rect) for sprite in self])
        if self._clear_active:
            rectPool.extend(list(self._sprites_drawn.values()))
            self._sprites_drawn.clear()
            for sprite in self._sprites:
                self._sprites_drawn[sprite] = rectPool.copy(
                                 self._sprites[sprite].rect)
        return None

    def clear(self, surface, background):
        """
        Clear previous sprite draw to surface using a background surface.
        The background argument can be a callback function.
        """
        self._clear_active = True
        if hasattr(background, 'width'):
            surface._blit_clear(background, self._sprites_drawn.values())
        else:
            for sprite in self._sprites_drawn:
                background(surface, self._sprites_drawn[sprite])

    def empty(self):
        """
        Empty group.
        """
        for sprite in self._sprites.values():
            del sprite._groups[id(self)]
        self._sprites.clear()
        return None

    def update(self, *args):
        """
        Update sprites in group by calling sprite.update.
        """
        for sprite in list(self._sprites.values()):
            sprite.update(*args)
        return None


class RenderPlain(Group):
    """
    **pyjsdl.sprite.RenderPlain**

    Same as sprite.Group.
    """
    pass


class RenderClear(Group):
    """
    **pyjsdl.sprite.RenderClear**

    Same as sprite.Group.
    """
    pass


class GroupSingle(Group):
    """
    **pyjsdl.sprite.GroupSingle**
    
    * Group subclass
    """

    def __init__(self, sprite=None):
        """
        Return GroupSingle, a Group subclass that holds a single sprite.
        Can optionally be called with sprite to add.
        """
        if sprite:
            Group.__init__(self, sprite)
        else:
            Group.__init__(self)

    def __getattr__(self, attr):
        if attr == 'sprite':
            if self._sprites:
                return list(self._sprites.values())[0]
            else:
                return None

    def add(self, sprite):
        """
        Add sprite to group, replacing existing sprite.
        """
        self.empty()
        self._sprites[id(sprite)] = sprite
        sprite._groups[id(self)] = self
        return None

    def update(self, *args):
        """
        Update sprite by calling Sprite.update.
        """
        if self._sprites:
            list(self._sprites.values())[0].update(*args)
        return None


class RenderUpdates(Group):
    """
    **pyjsdl.sprite.RenderUpdates**
    
    * Group subclass
    """

    def __init__(self, *sprites):
        """
        Return RenderUpdates, a Group subsclass that provides dirty draw functions.
        Can optionally be called with sprite(s) to add.
        """
        Group.__init__(self, *sprites)
        self.changed_areas = []

    def draw(self, surface):
        """
        Draw sprite on surface.
        Returns list of Rect of sprites updated, which can be passed to display.update.
        """
        surface._blits([(sprite.image,sprite.rect) for sprite in self])
        if self._clear_active:
            rectPool.extend(self.changed_areas)
            self.changed_areas[:] = []
            for sprite in self._sprites:
                if sprite in self._sprites_drawn:
                    if self._sprites_drawn[sprite].intersects(
                                   self._sprites[sprite].rect):
                        self._sprites_drawn[sprite].union_ip(
                                  self._sprites[sprite].rect)
                    else:
                        self.changed_areas.append(
                            rectPool.copy(self._sprites[sprite].rect))
                else:
                    self.changed_areas.append(
                        rectPool.copy(self._sprites[sprite].rect))
            self.changed_areas.extend(list(self._sprites_drawn.values()))
            self._sprites_drawn.clear()
            for sprite in self._sprites:
                self._sprites_drawn[sprite] = rectPool.copy(
                                 self._sprites[sprite].rect)
        else:
            rectPool.extend(self.changed_areas)
            self.changed_areas[:] = []
            self.changed_areas.extend([rectPool.copy(sprite.rect)
                                       for sprite in self._sprites.values()])
        return self.changed_areas


class OrderedUpdates(RenderUpdates):
    """
    **pyjsdl.sprite.OrderedUpdates**
    
    * RenderUpdates subclass
    """

    def __init__(self, *sprites):
        """
        Return OrderedUpdates, a RenderUpdates subclass that maintains order of sprites.
        Can optionally be called with sprite(s) to add.
        """
        self._orderedsprites = []
        RenderUpdates.__init__(self, *sprites)

    def __iter__(self):
        return iter(self._orderedsprites)

    def sprites(self):
        """
        Return ordered list of sprites in the group.
        """
        return self._orderedsprites[:]

    def copy(self):
        """
        Return copy of group.
        """
        newgroup = RenderUpdates.copy(self)
        newgroup._orderedsprites = self._orderedsprites[:]
        return newgroup

    def add(self, *sprites):
        """
        Add sprite(s) to group, maintaining order of addition.
        """
        for sprite in sprites:
            if hasattr(sprite, '_groups'):
                spriteID = id(sprite)
                if spriteID not in self._sprites:
                    self._sprites[spriteID] = sprite
                    sprite._groups[id(self)] = self
                    self._orderedsprites.append(sprite)
            else:
                self.add(*sprite)
        return None

    def remove(self, *sprites):
        """
        Remove sprite(s) from group.
        """
        for sprite in sprites:
            if hasattr(sprite, '_groups'):
                spriteID = id(sprite)
                if spriteID in self._sprites:
                    del self._sprites[spriteID]
                    del sprite._groups[id(self)]
                    self._orderedsprites.remove(sprite)
            else:
                self.remove(*sprite)
        return None

    def empty(self):
        """
        Empty group.
        """
        self._orderedsprites[:] = []
        RenderUpdates.empty(self)


class LayeredUpdates(OrderedUpdates):
    """
    **pyjsdl.sprite.LayeredUpdates**
    
    * OrderedUpdates subclass
    * subclass not implemented
    """

    def __init__(self, *sprites, **kwargs):
        """
        Return LayeredUpdates
        Optional argument sprites to add to group.
        If sprite has a _layer attribute, it will be added to that layer,
        otherwise it will be added to the default layer.
        If provided a default_layer keyword argument, this will be used
        as default, otherwise default_layer will be 0.
        If provided a layer keyword argument, then sprites will be
        added to that layer regardless of the sprite _layer attribute.
        """
        self._layer = {}
        self._layers = []
        if 'default_layer' not in kwargs:
            self._default_layer = 0
        else:
            self._default_layer = kwargs['default_layer']
        if 'layer' not in kwargs:
            self._override_layer = None
        else:
            self._override_layer = kwargs['layer']
        OrderedUpdates.__init__(self, *sprites)

    def copy(self):
        """
        Return copy of group.
        """
        newgroup = OrderedUpdates.copy(self)
        for layer in self._layer:
            layer_data = {}
            layer_data['sprite'] = set()
            for spriteID in self._layer[layer]['sprite']:
                layer_data['sprite'].add(spriteID)
            layer_data['index'] = self._layer[layer]['index'][:]
            newgroup._layer[layer] = layer_data
        newgroup._layers = self._layers[:]
        newgroup._default_layer = self._default_layer
        return newgroup

    def add(self, *sprites, **kwargs):
        """
        Add sprite(s) to group, maintaining order based on layer of sprite,
        derived from sprite _layer attribute or if absent default layer.
        If layer keyword argument is provided it is used.
        """
        if 'layer' in kwargs:
            self._override_layer = kwargs['layer']
        for sprite in sprites:
            if hasattr(sprite, '_groups'):
                spriteID = id(sprite)
                if spriteID not in self._sprites:
                    self._sprites[spriteID] = sprite
                    sprite._groups[id(self)] = self
                    if self._override_layer is not None:
                        layer = self._override_layer
                    elif hasattr(sprite, '_layer'):
                        layer = sprite._layer
                    else:
                        layer = self._default_layer
                    if layer not in self._layer:
                        self._add_layer(layer)
                    self._layer[layer]['sprite'].add(spriteID)
                    i = self._layer[layer]['index'][1]
                    self._layer[layer]['index'][1] += 1
                    index = self._layers.index(layer)
                    if self._layers[index:]:
                        for _layer in self._layers[index+1:]:
                            self._layer[_layer]['index'][0] += 1
                            self._layer[_layer]['index'][1] += 1
                    self._orderedsprites.insert(i, sprite)
            else:
                if self._override_layer is not None:
                    kwargs['layer'] = self._override_layer
                self.add(*sprite, **kwargs)
        self._override_layer = None
        return None

    def _add_layer(self, layer):
        self._layers.append(layer)
        self._layers.sort()
        index = self._layers.index(layer)
        if self._layers[:index]:
            prelayer = self._layers[index-1]
            i = self._layer[prelayer]['index'][1]
        else:
            i = 0
        self._layer[layer] = {'sprite':set(), 'index':[i,i]}

    def remove(self, *sprites):
        """
        Remove sprite(s) from group.
        """
        for sprite in sprites:
            if hasattr(sprite, '_groups'):
                spriteID = id(sprite)
                if spriteID in self._sprites:
                    del self._sprites[spriteID]
                    del sprite._groups[id(self)]
                    for layer in self._layers:
                        if str(spriteID) in self._layer[layer]['sprite']:
                            break
                    self._layer[layer]['sprite'].remove(spriteID)
                    i = self._layer[layer]['index'][1]
                    self._layer[layer]['index'][1] -= 1
                    index = self._layers.index(layer)
                    if self._layers[index:]:
                        for _layer in self._layers[index+1:]:
                            self._layer[_layer]['index'][0] -= 1
                            self._layer[_layer]['index'][1] -= 1
                    if (self._layer[layer]['index'][0]
                            == self._layer[layer]['index'][1]):
                        del self._layer[layer]
                        self._layers.remove(layer)
                    self._orderedsprites.remove(sprite)
            else:
                self.remove(*sprite)
        return None

    def empty(self):
        """
        Empty group.
        """
        self._layers[:] = []
        self._layer.clear()
        OrderedUpdates.empty(self)

    def get_sprites_at(self, position):
        """
        Return sprites at position.
        """
        colliding_sprites = []
        for sprite in self._orderedsprites:
            if sprite.rect.collidepoint(position):
                colliding_sprites.append(sprite)
        return colliding_sprites

    def get_sprite(self, index):
        """
        Return sprite at sprites index.
        """
        return self._orderedsprites[index]

    def remove_sprites_of_layer(self, layer):
        """
        Return sprites removed from layer.
        """
        i,j = self._layer[layer]['index']
        sprites = self._orderedsprites[i:j]
        for sprite in sprites:
            self.remove(sprite)
        return sprites

    def layers(self):
        """
        Return list of group layers.
        """
        return self._layers[:]

    def change_layer(self, sprite, new_layer):
        """
        Move sprite to new layer.
        """
        self.remove(sprite)
        self.add(sprite, layer=new_layer)
        return None

    def get_layer_of_sprite(self, sprite):
        """
        Return layer of sprite.
        """
        for layer in self._layers:
            if str(id(sprite)) in self._layer[layer]['sprite']:
                return layer

    def get_top_layer(self):
        """
        Return top layer of group.
        """
        return self._layers[-1]

    def get_bottom_layer(self):
        """
        Return bottom layer of group.
        """
        return self._layers[0]

    def move_to_front(self, sprite):
        """
        Move sprite to top layer.
        """
        self.remove(sprite)
        self.add(sprite, layer=self._layers[-1])
        return None

    def move_to_back(self, sprite):
        """
        Move sprite to layer under bottom layer.
        """
        new_layer = self._layers[0]-1
        self.remove(sprite)
        self.add(sprite, layer=new_layer)
        return None

    def get_top_sprite(self):
        """
        Return sprite at top.
        """
        return self._orderedsprites[-1]

    def get_sprites_from_layer(self, layer):
        """
        Return sprites on layer.
        """
        i,j = self._layer[layer]['index']
        return self._orderedsprites[i:j]

    def switch_layer(self, layer1, layer2):
        """
        Move sprites to new layer.
        """
        sprites1 = self.remove_sprites_of_layer(layer1)
        sprites2 = self.remove_sprites_of_layer(layer2)
        self.add(sprites1, layer=layer2)
        self.add(sprites2, layer=layer1)


class LayeredDirty(LayeredUpdates):
    """
    **pyjsdl.sprite.LayeredDirty**
    
    * LayeredUpdates subclass
    * subclass not implemented
    """

    def __init__(self, *sprites):
        """
        Return LayeredUpdates - subclass not implemented.
        """
        LayeredUpdates(self, *sprites)


def spritecollide(sprite, group, dokill, collided=None):
    """
    **pyjsdl.sprite.spritecollide**
    
    Return list of sprites in group that intersect with sprite.
    The dokill argument is a bool, True removes sprites that collide from all groups.
    An optional collided is a callback function taking two sprites and return bool collision.
    """
    collide = []
    collision = False
    for _sprite in group:
        if sprite.rect.intersects(_sprite.rect):
            if collided:
                if not collided(sprite,_sprite):
                    continue
            collide.append(_sprite)
            collision = True
    if collision and dokill:
        for _sprite in collide:
            _sprite.kill()
    return collide


def collide_rect(sprite1, sprite2):
    """
    **pyjsdl.sprite.collide_rect**
    
    Check if the rects of the two sprites intersect.
    Can be used as spritecollide callback function.
    """
    return sprite1.rect.intersects(sprite2.rect)


def collide_rect_ratio(ratio):
    """
    **pyjsdl.sprite.collide_rect_ratio**
    
    Return a callable that checks if the rects of the two sprites intersect.
    The ratio attribute will determine scaling of the rect, where 1.0 is same size.
    Can be used as spritecollide callback function.
    """
    obj = _collide_rect_ratio(ratio)
    return lambda sprite1,sprite2: obj.__call__(sprite1,sprite2)


class _collide_rect_ratio(object):

    __slots__ = ['ratio']

    def __init__(self, ratio):
        self.ratio = ratio

    def __call__(self, sprite1, sprite2):   #__call__ not implemented in pyjs
        r = sprite1.rect
        x = (r.width * self.ratio) - r.width
        y = (r.height * self.ratio) - r.height
        r1 = rectPool.get(r.x - int(x*0.5), r.y - int(y*0.5),
                          r.width + int(x), r.height + int(y))
        r = sprite2.rect
        x = (r.width * self.ratio) - r.width
        y = (r.height * self.ratio) - r.height
        r2 = rectPool.get(r.x - int(x*0.5), r.y - int(y*0.5),
                          r.width + int(x), r.height + int(y))
        collide = r1.intersects(r2)
        rectPool.append(r1)
        rectPool.append(r2)
        return collide


def collide_circle(sprite1, sprite2):
    """
    **pyjsdl.sprite.collide_circle**
    
    Check two sprites intersect by checking by intersection of circle around their centers.
    Will use sprite radius attribute or circle will encompass rect attribute.
    Can be used as spritecollide callback function.
    """
    if hasattr(sprite1, 'radius'):
        radius1 = sprite1.radius
    else:
        radius1 = (((((sprite1.rect.width)**2)
                   + ((sprite1.rect.height)**2))**0.5) * 0.5)
    if hasattr(sprite2, 'radius'):
        radius2 = sprite2.radius
    else:
        radius2 = (((((sprite2.rect.width)**2)
                   + ((sprite2.rect.height)**2))**0.5) * 0.5)
    sx1 = (sprite1.rect.x + int(sprite1.rect.width * 0.5))
    sy1 = (sprite1.rect.y + int(sprite1.rect.height * 0.5))
    sx2 = (sprite2.rect.x + int(sprite2.rect.width * 0.5))
    sy2 = (sprite2.rect.y + int(sprite2.rect.height * 0.5))
    return (((sx1 - sx2)**2 + (sy1 - sy2)**2)) < (radius1**2 + radius2**2)


def collide_circle_ratio(ratio):
    """
    **pyjsdl.sprite.collide_circle_ratio**
    
    Return a callable that checks two sprites intersect by checking by intersection of circle around their centers.
    The ratio attribute will determine scaling of the circle, where 1.0 is same size.
    Will use sprite radius attribute or circle will encompass rect attribute.
    Can be used as spritecollide callback function.
    """
    obj = _collide_circle_ratio(ratio)
    return lambda sprite1,sprite2: obj.__call__(sprite1,sprite2)


class _collide_circle_ratio(object):

    __slots__ = ['ratio']

    def __init__(self, ratio):
        self.ratio = ratio

    def __call__(self, sprite1, sprite2):   #__call__ not implemented in pyjs
        if hasattr(sprite1, 'radius'):
            radius1 = sprite1.radius * self.ratio
        else:
            radius1 = (((((sprite1.rect.width)**2)
                       + ((sprite1.rect.height)**2))**0.5) * 0.5 * self.ratio)
        if hasattr(sprite2, 'radius'):
            radius2 = sprite2.radius * self.ratio
        else:
            radius2 = (((((sprite2.rect.width)**2)
                       + ((sprite2.rect.height)**2))**0.5) * 0.5 * self.ratio)
        sx1 = (sprite1.rect.x + int(sprite1.rect.width * 0.5))
        sy1 = (sprite1.rect.y + int(sprite1.rect.height * 0.5))
        sx2 = (sprite2.rect.x + int(sprite2.rect.width * 0.5))
        sy2 = (sprite2.rect.y + int(sprite2.rect.height * 0.5))
        return ((sx1 - sx2)**2 + (sy1 - sy2)**2) < (radius1**2 + radius2**2)


def collide_mask(sprite1, sprite2):
    """
    **pyjsdl.sprite.collide_mask**
    
    Check if mask of sprites intersect.
    Will use sprite mask attribute or mask generated from image attribute.
    Can be used as spritecollide callback function.
    """
    if hasattr(sprite1, 'mask'):
        mask1 = sprite1.mask
    else:
        mask1 = mask.from_surface(sprite1.image)
    if hasattr(sprite2, 'mask'):
        mask2 = sprite2.mask
    else:
        mask2 = mask.from_surface(sprite2.image)
    if mask1.overlap(mask2,
        (sprite2.rect.x-sprite1.rect.x, sprite2.rect.y-sprite1.rect.y)):
        return True
    else:
        return False


def groupcollide(group1, group2, dokill1, dokill2):
    """
    **pyjsdl.sprite.groupcollide**
    
    Return dictionary of sprites in group1 with list of sprites in group2 that intersect.
    The dokill argument is a bool, True removes sprites that collide from all groups.
    """
    collide = {}
    collision = False
    for sprite1 in group1:
        for sprite2 in group2:
            if sprite1.rect.intersects(sprite2.rect):
                if sprite1 not in collide:
                    collide[sprite1] = []
                collide[sprite1].append(sprite2)
                collision = True
    if collision:
        if dokill1:
            for sprite1 in collide:
                sprite1.kill()
        if dokill2:
            for sprite1 in collide:
                for sprite2 in collide[sprite1]:
                    sprite2.kill()
    return collide


def spritecollideany(sprite, group):
    """
    **pyjsdl.sprite.spritecollideany**
    
    Check if sprite intersect with any sprites in group.
    """
    for _sprite in group:
        if sprite.rect.intersects(_sprite.rect):
            return True
    return False

