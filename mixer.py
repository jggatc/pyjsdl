#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from pyjsdl.pyjsobj import Audio
from pyjsdl.time import Time

__docformat__ = 'restructuredtext'


class Mixer:
    """
    **pyjsdl.mixer**
    
    * pyjsdl.mixer.init
    * pyjsdl.mixer.quit
    * pyjsdl.mixer.get_init
    * pyjsdl.mixer.stop
    * pyjsdl.mixer.pause
    * pyjsdl.mixer.unpause
    * pyjsdl.mixer.set_num_channels
    * pyjsdl.mixer.get_num_channels
    * pyjsdl.mixer.set_reserved
    * pyjsdl.mixer.find_channel
    * pyjsdl.mixer.get_busy
    * pyjsdl.mixer.Sound
    * pyjsdl.mixer.Channel
    """

    def __init__(self):
        Sound._mixer = self
        Channel._mixer = self
        self.Sound = Sound
        self.Channel = Channel
        self._channel_max = 8
        self._channels = {}
        self._sounds = {}
        self._channel_reserved = []
        self._channel_paused = []
        self._channel_reserves = [id for id in range(self._channel_max-1,-1,-1)]
        self._channel_pool = []
        self._lines = {}
        self._line_num = 0
        self._initialized = True
        self._nonimplemented_methods()

    def init(self, *args, **kwargs):
        """
        Mixer initialization.
        """
        if not self._initialized:
            self._initialized = True
        return None

    def pre_init(self,  *args, **kwargs):
        """
        Mixer initialization.
        """
        self.init()
        return None

    def quit(self):
        """
        Stop mixer processing and release resources.
        """
        self.stop()
        self._initialized = False

    def get_init(self):
        """
        Get the audio format initialized.
        """
        if self._initialized:
            return self._initialized
        else:
            return None

    def stop(self):
        """
        Stop mixer channels.
        """
        for id in self._channel_pool:
            self._channels[id].stop()
        return None

    def pause(self):
        """
        Pause mixer channels.
        """
        for id in self._channel_pool:
            try:
                if self._channels[id]._active:
                    self._channel_paused.append(id)
                    self._channels[id].pause()
            except AttributeError:
                continue
        return None

    def unpause(self):
        """
        Unpause mixer channels.
        """
        for id in self._channel_paused:
            self._channels[id].unpause()
        self.channel_paused = []
        return None

    def set_num_channels(self, count):
        """
        Set maximum mixer channels.
        Argument channel count.
        """
        if count >= self._channel_max:
            for id in range(self._channel_max, count):
                self._channels[id] = None
            self._channel_max = count
        elif count >= 0:
                for id in range(count, self._channel_max):
                    self._channels[id].stop()
                    del self._channels[id]
                self._channel_max = count
        return None

    def get_num_channels(self):
        """
        Get maximum mixer channels.
        """
        return self._channel_max

    def set_reserved(self, count):
        """
        Reserve channel.
        Argument reserved channel count.
        """
        if count > self._channel_max:
            count = self._channel_max
        reserved_len = len(self._channel_reserved)
        if reserved_len:
            if reserved_len >= count:
                for i in range(reserved_len-count):
                    id = self._channel_reserved.pop()
                    self._channels[id]._reserved = False
                    self._channel_pool.append(id)
                count = 0
            else:
                count -= len(self._channel_reserved)
        for id in range(reserved_len, count+reserved_len):
            try:
                self._channels[id]._reserved = True
            except AttributeError:
                self._channels[id] = Channel(id)
            try:
                self._channel_pool.remove(id)
            except ValueError:
                pass
            self._channel_reserved.append(id)
        return None

    def find_channel(self, force=False):
        """
        Get an inactive mixer channel.
        Optional force attribute return longest running channel if all active.
        """
        if self._channel_reserves:
            channel = self._channel_reserves.pop()
            if channel in self._channels:
                return self._channels[channel]
            else:
                channel = Channel(channel)
                return channel
        else:
            for id in self._channel_pool:
                if not self._channels[id]._active:
                    return self._channels[id]
            else:
                if force:
                    channel = None
                    longest = 0
                    for id in self._channel_pool:
                        if self._channels[id]._sound and not self._channels[id].isPaused():
                            duration = self._channels[id]._sound._sound_object.getCurrentTime()
                            if duration > longest:
                                longest = duration
                                channel = self._channels[id]
                        else:
                            channel = self._channels[id]
                            break
                    if channel:
                        channel.stop()
                        return channel
                    else:
                        return None
                else:
                    return None

    def get_busy(self):
        """
        Check if mixer channels are actively processing.
        """
        for id in self._channel_pool:
            try:
                if self._channels[id]._active:
                    return True
            except AttributeError:
                continue
        return False

    def _register_channel(self, channel):
        id = channel._id
        if id < self._channel_max:
            try:
                if self._channels[id]._sound:
                    channel._sound = self._channels[id]._sound
                    self._channels[id] = channel
            except KeyError:
                self._channels[id] = channel
                self._channel_pool.append(id)
        else:
            raise AttributeError("Channel not available.")

    def _register_sound(self, sound):
        self._sounds[sound._id] = sound

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.fadeout = lambda *arg: None


class Sound:
    """
    **pyjsdl.mixer.Sound**
    
    * Sound.play
    * Sound.stop
    * Sound.set_volume
    * Sound.get_volume
    * Sound.get_num_channels
    * Sound.get_length
    """

    _id = 0
    _mixer = None

    def __init__(self, sound_file, id=None):
        if id is None:
            self._id = Sound._id
            Sound._id += 1
            self._mixer._register_sound(self)
        else:
            self._id = id
        if isinstance(sound_file, str):
            self._sound_object = Audio(sound_file.replace('\\','/'))
        else:
            self._sound_object = sound_file
        self._sound_objects = []
        self._channel = None
        self._ch = None
        self._volume = 1.0
        self._nonimplemented_methods()

    def play(self, loops=0, maxtime=0, fade_ms=0):
        """
        Play sound on mixer channel.
        Argument loops is number of repeats or -1 for continuous.
        """
        if not self._channel:
            self._channel = self._mixer.find_channel()
            if self._channel:
                self._channel._set_sound(self)
            else:
                return None
        if self._sound_object.isPaused():
            self._ch = self._channel
        else:
            self._ch = self._mixer.find_channel()
            if self._ch:
                sound = Sound(self._sound_object.getSrc(), self._id)
                self._ch._set_sound(sound)
            else:
                return None
        if not loops:
            self._ch._play()
        else:
            self._ch._play_repeat(loops)
        return self._ch

    def stop(self):
        """
        Stop sound on mixer channel.
        """
        if self._channel:
            self._channel.stop()

    def set_volume(self, volume):
        """
        Set sound volume.
        Argument volume of value 0.0 to 1.0.
        """
        if volume < 0.0:
            volume = 0.0
        elif volume > 1.0:
            volume = 1.0
        self._volume = volume
        self._sound_object.setVolume(self._volume)
        return None

    def get_volume(self):
        """
        Get sound volume.
        """
        return self._volume

    def get_num_channels(self):
        """
        Get number of channels sound is active.
        """
        channel = 0
        for id in self._mixer._channel_pool:
            try:
                if self._mixer._channels[id]._sound._id == self._id:
                    channel += 1
            except AttributeError:
                continue
        return channel

    def get_length(self):
        """
        Get length of sound sample.
        """
        return self._sound_object.getDuration()

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.fadeout = lambda *arg: None
        self.get_buffer = lambda *arg: None


class Channel:
    """
    **pyjsdl.mixer.Channel**
    
    * Channel.play
    * Channel.stop
    * Channel.pause
    * Channel.unpause
    * Channel.set_volume
    * Channel.get_volume
    * Channel.get_busy
    * Channel.get_sound
    """

    _mixer = None

    def __init__(self, id):
        self._id = id
        self._sound = None
        self._active = False
        self._pause = False
        self._loops = 0
        self._volume = 1.0
        self._lvolume = 1.0
        self._rvolume = 1.0
        self._mixer._register_channel(self)
        self._time = Time()
        self._nonimplemented_methods()

    def _set_sound(self, sound):
        if self._sound:
            self._sound._channel = None
        self._sound = sound

    def _play(self):
        self._volume = 1.0
        self._lvolume = 1.0
        self._rvolume = 1.0
        self._active = True
        self._sound._sound_object.play()
        self._time.timeout(self._sound._sound_object.getDuration()*1000, self)

    def _play_repeat(self, loops):
        if loops > 0:
            self._loops = loops
        else:
            self._loops = -1
        self._play()

    def play(self, sound, loops=0, maxtime=0, fade_ms=0):
        """
        Play sound on channel.
        Argument sound to play and loops is number of repeats or -1 for continuous.
        """
        if self._sound:
            self.stop()
        self._set_sound(sound)
        if not loops:
            self._play()
        else:
            self._play_repeat(loops)
        return None

    def run(self):
        if not self._loops:
            self._active = False
        else:
            if self._loops > 0:
                self._loops -= 1
            self._play()

    def stop(self):
        """
        Stop sound on channel.
        """
        if self._sound:
            self._sound._sound_object.pause()
            self._sound._sound_object.setCurrentTime(0)
            self._pause = False
            self._loops = 0
            self._active = False
        return None

    def pause(self):
        """
        Pause sound on channel.
        """
        if self._sound:
            if not self._pause:
                self._sound._sound_object.pause()
                self._pause = True
        return None

    def unpause(self):
        """
        Unpause sound on channel.
        """
        if self._sound:
            if self._pause:
                self._sound._sound_object.play()
                self._pause = False
        return None

    def set_volume(self, volume):
        """
        Set channel volume of sound playing.
        """
        if volume < 0.0:
            volume = 0.0
        elif volume > 1.0:
            volume = 1.0
        self._volume = volume
        if self._sound:
            self._sound._sound_object.setVolume(self._volume * self._sound._sound_object._volume)
        else:
            self._volume = 1.0
        return None

    def get_volume(self):
        """
        Get channel volume for current sound.
        """
        return self._volume

    def get_busy(self):
        """
        Check if channel is processing sound.
        """
        return self._active

    def get_sound(self):
        """
        Get sound open by channel.
        """
        return self._sound

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.fadeout = lambda *arg: None
        self.queue = lambda *arg: None
        self.get_queue = lambda *arg: None
        self.set_endevent = lambda *arg: None
        self.get_endevent = lambda *arg: 0

