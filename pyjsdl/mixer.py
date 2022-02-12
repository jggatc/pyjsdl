#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.pyjsobj import Audio
from pyjsdl.time import Time
from pyjsdl import env
from pyjsdl import constants as Const

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
    * pyjsdl.mixer.fadeout
    * pyjsdl.mixer.set_num_channels
    * pyjsdl.mixer.get_num_channels
    * pyjsdl.mixer.set_reserved
    * pyjsdl.mixer.find_channel
    * pyjsdl.mixer.get_busy
    * pyjsdl.mixer.Sound
    * pyjsdl.mixer.Channel
    * pyjsdl.mixer.music
    """

    def __init__(self):
        Sound._mixer = self
        Channel._mixer = self
        self.Sound = Sound
        self.Channel = self._get_channel
        self._channel_max = 8
        self._channels = {}
        self._channel_available = [id for id in
                                   range(self._channel_max-1,-1,-1)]
        self._channel_active = []
        self._channel_reserved = []
        self._channel_reserved_num = 0
        self._channel_process = set()
        self._channel_process_end = set()
        for id in range(self._channel_max):
            self._get_channel(id)
        self.music = Music()
        self._time = Time()
        self._timerid = 0
        self._processing = False
        self._active = False
        self._initialized = True

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
        self.music._channel.stop()
        self._initialized = False
        return None

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
        for id in self._channel_active:
            if id > -1:
                self._channels[id].stop()
        return None

    def fadeout(self, time):
        """
        Fadeout mixer channels in given time.
        """
        for id in self._channel_active:
            if id > -1:
                self._channels[id].fadeout(time)
        return None

    def pause(self):
        """
        Pause mixer channels.
        """
        for id in self._channel_active:
            if id > -1:
                self._channels[id].pause()
        return None

    def unpause(self):
        """
        Unpause mixer channels.
        """
        for id in self._channel_active:
            if id > -1:
                self._channels[id].unpause()
        return None

    def set_num_channels(self, count):
        """
        Set maximum mixer channels.
        Argument channel count.
        """
        if count >= self._channel_max:
            for id in range(self._channel_max, count):
                self._get_channel(id)
                self._channel_available.insert(0, id)
            self._channel_max = count
        elif count >= 0:
            for id in range(count, self._channel_max):
                if id in self._channels:
                    if self._channels[id] is not None:
                        self._channels[id].stop()
                    del self._channels[id]
                if id in self._channel_available:
                    self._channel_available.remove(id)
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
        elif count < 0:
            count = 0
        self._channel_reserved_num = count
        self._channel_reserved = []
        for id in range(self._channel_reserved_num):
            self._channel_reserved.append(id)
            if id in self._channel_available:
                self._channel_available.remove(id)
        return None

    def find_channel(self, force=False):
        """
        Get an inactive mixer channel.
        Optional force attribute return longest running channel if all active.
        """
        if self._channel_available:
            id = self._channel_available.pop()
            self._channel_available.insert(0, id)
            return self._channels[id]
        if self._channel_reserved_num:
            if self._channel_reserved:
                id = self._channel_reserved.pop()
                self._channel_reserved.insert(0, id)
                return self._channels[id]
        if not force:
            return None
        longest = None
        longest_reserved = None
        for id in self._channel_active:
            if id > self._channel_reserved_num-1:
                longest = id
                break
            elif id > -1:
                if longest_reserved is None:
                    longest_reserved = id
        if longest is not None:
            channel = longest
        else:
            if longest_reserved is not None:
                channel = longest_reserved
            else:
                channel = 0
        return self._channels[channel]

    def get_busy(self):
        """
        Check if mixer channels are actively processing.
        """
        for id in self._channel_active:
            if id > -1:
                if self._channels[id]._active:
                    return True
        return False

    def _process(self, id):
        self._channel_process.add(id)
        if not self._processing:
            self._processing = True
            self._timerid = self._time.set_interval(self, 10)

    def run(self):
        if self._active:
            for id in self._channel_process:
                complete = self._channels[id]._process()
                if complete:
                    self._channel_process_end.add(id)
            if self._channel_process_end:
                for i in range(len(self._channel_process_end)):
                    id = self._channel_process_end.pop()
                    self._channel_process.discard(id)
                if not self._channel_process:
                    self._processing = False
                    self._time.clear_interval(self._timerid)
        else:
            if self._channel_process:
                for i in range(len(self._channel_process)):
                    self._channel_process.pop()
            self._processing = False
            self._time.clear_interval(self._timerid)

    def _activate_channel(self, id):
        if id > self._channel_reserved_num-1:
            self._channel_available.remove(id)
        elif id > -1:
            self._channel_reserved.remove(id)
        self._channel_active.append(id)
        self._active = True

    def _deactivate_channel(self, id):
        self._channel_active.remove(id)
        if not self._channel_active:
            self._active = False

    def _restore_channel(self, id):
        if id > self._channel_reserved_num-1:
            self._channel_available.append(id)
        elif id > -1:
            self._channel_reserved.append(id)

    def _retrieve_channel(self):
        if self._channel_available:
            id = self._channel_available.pop()
            self._channel_active.append(id)
            self._active = True
            return self._channels[id]
        else:
            return None

    def _get_channel(self, id):
        if id in self._channels:
            return self._channels[id]
        else:
            return Channel(id)

    def _register_channel(self, channel):
        id = channel._id
        if id < self._channel_max:
            self._channels[id] = channel
        else:
            raise AttributeError("Channel not available.")


class Sound(object):
    """
    **pyjsdl.mixer.Sound**
    
    * Sound.play
    * Sound.stop
    * Sound.fadeout
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
        else:
            self._id = id
        if isinstance(sound_file, str):
            self._sound_object = Audio(sound_file.replace('\\','/'))
        else:
            self._sound_object = sound_file
        self._sound_objects = []
        self._sound_objects.append(self._sound_object)
        self._channel = None
        self._volume = 1.0

    def play(self, loops=0, maxtime=0, fade_ms=0):
        """
        Play sound on mixer channel.
        Argument loops is repeat number or -1 for continuous,
        maxtime is maximum play time, and fade_ms is fade-in time.
        """
        self._channel = self._mixer._retrieve_channel()
        if self._channel:
            self._channel._play(self, loops, maxtime, fade_ms)
        return self._channel

    def stop(self):
        """
        Stop sound on active channels.
        """
        channels = self._mixer._channels
        for id in self._mixer._channel_active:
            if id > -1:
                try:
                    if channels[id]._sound._id == self._id:
                        channels[id].stop()
                except AttributeError:
                    continue
        return None

    def fadeout(self, time):
        """
        Fadeout sound on active channels in given time.
        """
        channels = self._mixer._channels
        for id in self._mixer._channel_active:
            if id > -1:
                try:
                    if channels[id]._sound._id == self._id:
                        channels[id].fadeout(time)
                except AttributeError:
                    continue
        return None

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
        channels = self._mixer._channels
        channel = 0
        for id in self._mixer._channel_active:
            if id > -1:
                try:
                    if channels[id]._sound._id == self._id:
                        channel += 1
                except AttributeError:
                    continue
        return channel

    def get_length(self):
        """
        Get length of sound sample.
        """
        return self._sound_object.getDuration()

    def get_sound_object(self):
        if self._sound_objects:
            sound_object = self._sound_objects.pop()
        else:
            sound_object = Audio(self._sound_object.getSrc())
        return sound_object


class Channel(object):
    """
    **pyjsdl.mixer.Channel**
    
    * Channel.play
    * Channel.stop
    * Channel.pause
    * Channel.unpause
    * Channel.fadeout
    * Channel.set_volume
    * Channel.get_volume
    * Channel.get_busy
    * Channel.get_sound
    * Channel.queue
    * Channel.get_queue
    * Channel.set_endevent
    * Channel.get_endevent
    """

    _mixer = None

    def __init__(self, id):
        self._id = id
        self._sound = None
        self._sound_object = None
        self._active = False
        self._pause = False
        self._loops = 0
        self._volume = 1.0
        self._lvolume = 1.0
        self._rvolume = 1.0
        self._queue = None
        self._endevent = None
        self._time = 0
        self._maxtime = 0
        self._fadein = 0
        self._fadeout = 0
        self._dvol = 1.0
        self._timerid = 0
        self._mixer._register_channel(self)
        self._ended_handler = lambda event: self._onended(event)

    def _set_sound(self, sound):
        self._sound = sound
        self._sound_object = self._sound.get_sound_object()
        self._sound_object.element.onended = self._ended_handler

    def _reset_sound(self):
        self._active = False
        restart = not self._pause
        if not self._sound:
            return
        self._sound_object.element.pause()
        self._sound_object.element.currentTime = 0
        if restart:
            self._sound_object.play()
        self._active = True

    def play(self, sound, loops=0, maxtime=0, fade_ms=0):
        """
        Play sound on channel.
        Argument sound to play, loops is repeat number or -1 for continuous,
        maxtime is maximum play time, and fade_ms is fade-in time.
        """
        if self._sound:
            volume = self._volume
            self.stop()
            self._volume = volume
        self._set_sound(sound)
        self._mixer._activate_channel(self._id)
        self._loops = loops
        if maxtime:
            self._maxtime = maxtime / 1000.0
            self._timerid = self._mixer._time.set_timeout(self, maxtime)
        if fade_ms:
            self._fadein = fade_ms / 1000.0
            self._mixer._process(self._id)
            self._sound_object.element.volume = 0.01
        else:
            self._sound_object.element.volume = (self._volume
                                                 * self._sound._volume)
        self._sound_object.element.play()
        if self._sound_object.element.paused:
            self.stop()
        else:
            self._active = True
        return None

    def _play(self, sound, loops, maxtime, fade_ms):
        self._set_sound(sound)
        self._loops = loops
        if maxtime:
            self._maxtime = maxtime / 1000.0
            self._timerid = self._mixer._time.set_timeout(self, maxtime)
        if fade_ms:
            self._fadein = fade_ms / 1000.0
            self._mixer._process(self._id)
            self._sound_object.element.volume = 0.01
        else:
            self._sound_object.element.volume = (self._volume
                                                 * self._sound._volume)
        self._sound_object.element.play()
        if self._sound_object.element.paused:
            self.stop()
        else:
            self._active = True
        return None

    def _replay(self):
        self._sound_object.element.volume = (self._volume
                                             * self._sound._volume)
        self._sound_object.element.play()
        if self._sound_object.element.paused:
            self.stop()
        else:
            self._active = True

    def _process(self):
        if self._active:
            complete = False
        else:
            complete = True
            return complete
        self._time = self._sound_object.element.currentTime
        complete = False
        if self._fadein:
            if self._time < self._fadein:
                self._dvol = self._time / self._fadein
                self._sound_object.element.volume = (self._volume
                                                     * self._sound._volume
                                                     * self._dvol)
            else:
                self._fadein = 0
                complete = True
                self._sound_object.element.volume = (self._volume
                                                     * self._sound._volume)
        elif self._fadeout:
            if self._time < self._fadeout:
                self._dvol = 1.0 - (self._time / self._fadeout)
                self._sound_object.element.volume = (self._volume
                                                     * self._sound._volume
                                                     * self._dvol)
            else:
                self._fadeout = 0
                complete = True
                self._dvol = 0.01
                self._sound_object.element.volume = (self._volume
                                                     * self._sound._volume
                                                     * self._dvol)
                self._loops = 0
                self._onended()
        return complete

    def run(self):
        time = self._sound_object.element.currentTime
        if self._maxtime:
            if time > self._maxtime:
                self._maxtime = 0
                self._loops = 0
                self.stop()
            else:
                self._timerid = self._mixer._time.set_timeout(self, 10)

    def _onended(self, event):
        if not self._loops:
            if not self._queue:
                self.stop()
            else:
                self.play(self._queue)
        else:
            if self._loops > 0:
                self._loops -= 1
            self._replay()

    def stop(self):
        """
        Stop sound on channel.
        """
        if self._sound:
            self._active = False
            self._mixer._deactivate_channel(self._id)
            self._sound_object.element.onended = None
            self._sound_object.element.pause()
            self._sound_object.element.currentTime = 0
            self._sound._sound_objects.append(self._sound_object)
            self._sound = None
            self._sound_object = None
            self._queue = None
            self._pause = False
            self._loops = 0
            if self._maxtime:
                self._mixer._time.clear_timeout(self._timerid)
                self._maxtime = 0
            self._fadein = 0
            self._fadeout = 0
            self._volume = 1.0
            self._lvolume = 1.0
            self._rvolume = 1.0
            self._mixer._restore_channel(self._id)
            if self._endevent is not None:
                env.event.post(self._endevent)
        return None

    def pause(self):
        """
        Pause sound on channel.
        """
        if self._sound:
            if not self._pause:
                self._sound_object.pause()
                self._pause = True
        return None

    def unpause(self):
        """
        Unpause sound on channel.
        """
        if self._sound:
            if self._pause:
                self._sound_object.play()
                self._pause = False
        return None

    def fadeout(self, time):
        """
        Stop sound after fade out time.
        """
        if self._sound:
            self._fadeout = (self._sound_object.element.currentTime
                             + (time/1000.0))
            self._mixer._process(self._id)
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
        if self._active:
            self._sound_object.element.volume = (self._volume
                                                 * self._sound._volume)
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

    def queue(self, sound):
        """
        Queue sound to play after current sound ends.
        """
        if not self._sound:
            self.play(sound)
        else:
            self._queue = sound

    def get_queue(self):
        """
        Return queue sound.
        """
        return self._queue

    def set_endevent(self, eventType=None):
        """
        Set endevent for sound channel.
        Argument eventType is event type (eg. USEREVENT+num).
        Without an argument resets endevent to NOEVENT type.
        """
        if eventType is not None:
            if ( self._endevent is None or
                 self._endevent.type != eventType ):
                self._endevent = env.event.Event(eventType)
        else:
            self._endevent = None

    def get_endevent(self):
        """
        Get endevent type for sound channel.
        """
        if self._endevent is not None:
            return self._endevent.type
        else:
            return Const.NOEVENT


class Music(object):
    """
    **pyjsdl.mixer.music**

    * music.load
    * music.unload
    * music.play
    * music.rewind
    * music.stop
    * music.pause
    * music.unpause
    * music.fadeout
    * music.set_volume
    * music.get_volume
    * music.get_busy
    * music.queue
    * music.set_endevent
    * music.get_endevent
    """

    def __init__(self):
        self._channel = Channel(-1)
        self._sound = None
        self._queue = None
        self._volume = 1.0

    def load(self, sound_file):
        """
        Load music file.
        """
        if self._channel.get_busy():
            self._channel.stop()
        self._sound = Sound(sound_file)
        return None

    def unload(self):
        """
        Unload music file.
        """
        self._channel.stop()
        self._sound = None
        return None

    def play(self, loops=0, maxtime=0, fade_ms=0):
        """
        Play music.
        Argument loops is repeat number or -1 for continuous,
        maxtime is maximum play time, and fade_ms is fade-in time.
        """
        self._channel.set_volume(self._volume)
        self._channel.play(self._sound, loops, maxtime, fade_ms)
        if self._queue:
            self._channel.queue(self._queue)
            self._sound = self._queue
            self._queue = None
        return None

    def rewind(self):
        """
        Rewind music.
        """
        if self._channel.get_busy():
            self._channel._reset_sound()

    def stop(self):
        """
        Stop music.
        """
        self._channel.stop()
        return None

    def pause(self):
        """
        Pause music.
        """
        self._channel.pause()
        return None

    def unpause(self):
        """
        Unpause music.
        """
        self._channel.unpause()
        return None

    def fadeout(self, time):
        """
        Stop music after fade out time.
        """
        self._channel.fadeout(time)
        return None

    def set_volume(self, volume):
        """
        Set music volume.
        Argument volume of value 0.0 to 1.0.
        """
        if volume < 0.0:
            volume = 0.0
        elif volume > 1.0:
            volume = 1.0
        self._volume = volume
        if self._channel.get_busy():
            self._channel.set_volume(volume)
        return None

    def get_volume(self):
        """
        Get volume for current music.
        """
        return self._volume

    def get_busy(self):
        """
        Check if music playing.
        """
        return self._channel.get_busy()

    def queue(self, sound_file):
        """
        Queue sound to play after current sound ends.
        """
        if not self._sound:
            return None
        if not self._channel.get_busy():
            self._queue = Sound(sound_file)
        else:
            self._sound = Sound(sound_file)
            self._channel.queue(self._sound)

    def set_endevent(self, eventType=None):
        """
        Set endevent for music channel.
        Argument eventType is event type (eg. USEREVENT+num).
        Without an argument resets endevent to NOEVENT type.
        """
        self._channel.set_endevent(eventType)
        return None

    def get_endevent(self):
        """
        Get endevent type for music channel.
        """
        return self._channel.get_endevent()

