import sounds
from serv_config import Config as cfg
import random


class SoundBox(object):
    """
    Sound Box interface : you must implement the get function.
    """
    parents = None
    # array of parents
    custom_buff = None

    # buffer for custom value

    def __init__(self, custom_buff=None):
        super(SoundBox, self).__init__()
        self.custom_buff = custom_buff
        self.parents = {}

    def set_parent(self, n, parent):
        self.parents[n] = parent

    def get(self):
        raise NotImplementedError()


class PitchBox(SoundBox):
    """
    Change the pitch of a sound.

    Parents :
        0              , 1
        sound1         , value1
        sound to change, ratio of changing
    """

    def get(self):
        sound1 = self.parents[0].get()
        value1 = float(self.parents[1].get())
        new_sound = sounds.WaveSound(sound1.get_samplerate())
        for i in range(sound1.get_length()):
            point = sound1.get_value(i)
            if int(i % value1) == 0:
                new_sound.add_value(point)
        for i in range(sound1.get_length() - new_sound.get_length()):
            point = sound1.get_value(i)
            new_sound.add_value(point)
        return new_sound


"""
new_sound = sounds.WaveSound(self.parents[0].get().get_samplerate())
for i in range(self.parents[0].get_length()):
    point = self.parents[0].get_value(i)
    if point > 255 - int(self.parents[1].get()):
        new_sound.add_value(255 - int(self.parents[1].get()))
    elif point < self.parents[1].get():
        new_sound.add_value(self.parents[1].get())
    else:
        new_sound.add_value(point)
return new_sound"""


class AddBox(SoundBox):
    """
    Add two sound depending on a ratio.

    Parents :
        0          , 1           , 2
        sound1     , sound2      , value1
        first sound, second sound, ratio of each sound
    """

    def get(self):
        return self.parents[0].get().add(self.parents[1].get(), eval(str(self.parents[2].get())))


class ValueBox(SoundBox):
    """
    Return a fixed value.

    Custom Buffer :
        value to use
    """

    def get(self):
        return self.custom_buff


class MoreBox(SoundBox):
    """
    Compare if a value is bigger than another and set the return value depending on the result.

    Parents :
        0            , 1          , 2                  , 3
        value1       , value2     , value3/sound3      , value4/sound4
        value to test, test value , value/sound if true, value/sound if false
    """

    def get(self):
        return self.parents[2].get() if self.parents[0].get() > self.parents[1].get() else self.parents[3].get()


class LessBox(SoundBox):
    """
    Compare if a value is smaller than another and set the return value depending on the result.

    Parents :
        0            , 1          , 2                  , 3
        value1       , value2     , value3/sound3      , value4/sound4
        value to test, test value , value/sound if true, value/sound if false
    """

    def get(self):
        return self.parents[2].get() if self.parents[0].get() < self.parents[1].get() else self.parents[3].get()


class SinBox(SoundBox):
    """
    Generate a sine wave with a frequency depending on the value.

    Parents :
        0
        value1
        frequency of the sine wave

    """

    def get(self):
        return sounds.WaveGenerator().sinusoid(cfg.SOUND_PROCESS_LENGTH, cfg.SOUND_DEFAULT_SAMPLERATE,
                                               int(eval(str(self.parents[0].get()))))


class DeviceBox(SoundBox):
    """self.custom_buff.split(":")
    Get the last value in the data center for the give device/channel.

    Parents :
        0
        value1
        CUID:channel
    """
    datacenter = None

    def __init__(self, datacenter, custom_buff=None):
        super(DeviceBox, self).__init__(custom_buff)
        self.datacenter = datacenter

    def get(self):
        cuid, channel = self.parents[0].get().split(":")
        return self.datacenter.get(int(cuid), int(channel))


class RandomBox(SoundBox):
    """
    Give a random value
    """

    def get(self):
        return random.random()


class MultiplyBox(SoundBox):
    """
    Multiply a number with another.

    Parents :
        0            , 1
        value1       , value2
        first number , second number
    """

    def get(self):
        return eval(str(self.parents[0].get())) * eval(str(self.parents[1].get()))


class SumBox(SoundBox):
    """
    Return the sum of two values

    Parents :
        0            , 1
        value1       , value2
        first number , second number
    """

    def get(self):
        return eval(str(self.parents[0].get())) + eval(str(self.parents[1].get()))


class OutBox(SoundBox):
    """
    Just represents the output of the system.

    Parents :
        0
        sound1
        the final sound to output
    """

    def get(self):
        return self.parents[0].get()


class DistortionBox(SoundBox):
    """
    Give a distortion effect to the sound.

    Parents :
        0              , 1
        sound1         , value1
        sound to change, ratio of changing
    """

    def get(self):
        sound1=self.parents[0].get()
        value1=self.parents[1].get()
        new_sound = sounds.WaveSound(sound1.get_samplerate(), sound1.get_bitpersample(), sound1.get_num_channels())
        for i in range(sound1.get_length()):
            point = sound1.get_value(i)
            if point > 255 - int(value1):
                new_sound.add_value(255 - int(value1))
            elif point < value1:
                new_sound.add_value(value1)
            else:
                new_sound.add_value(point)
        return new_sound


class AmpliBox(SoundBox):
    """
    Amplificate a sound.

    Parents :
        0              , 1
        sound1         , value1
        sound to change, ratio of changing
    """

    def get(self):
        sound1 = self.parents[0].get()
        value1 = self.parents[1].get()
        new_sound = sounds.WaveSound(sound1.get_samplerate(), sound1.get_bitpersample(), sound1.get_num_channels())
        for i in range(sound1.get_length()):
            point = sound1.get_value(i)
            np = max(0, min(255, ((point - 128) * value1) + 128))
            new_sound.add_value(np)
        return new_sound


class DopplerBox(SoundBox):
    """
    give a Doppler effect to a sound.

    Parents :
        0              , 1
        sound1         , value1
        sound to change, ratio of changing
    """

    def get(self):
        sound1 = self.parents[0].get()
        value1 = self.parents[1].get()
        new_sound = sounds.WaveSound(sound1.get_samplerate(), sound1.get_bitpersample(), sound1.get_num_channels())
        new_sound2 = new_sound.get_copy()
        new_sound3 = new_sound.get_copy()

        halfsoundlength = int(sound1.get_length() * 0.5)
        for i in range(halfsoundlength):
            point = sound1.get_value(i)

            if int(i % (1 + (value1 / 340))) == 0:
                new_sound.add_value(point)

        for i in range(halfsoundlength - new_sound.get_length()):
            point = new_sound.get_value(i)
            new_sound.add_value(point)
        for i in range(halfsoundlength):
            point = new_sound.get_value(i)
            a = i / halfsoundlength
            np = max(0, min(255, round((point - 128) * a + 128)))
            new_sound2.add_value(np)
        for i in range(halfsoundlength):
            point = sound1.get_value(i)
            if int(i % (1 - (value1 / 340))) == 0:
                new_sound3.add_value(point)

        for i in range(halfsoundlength - new_sound.get_length()):
            point = new_sound3.get_value(i)
            new_sound3.add_value(point)

        for i in range(halfsoundlength):
            point = new_sound3.get_value(i)
            a = (halfsoundlength - i) / halfsoundlength
            np = max(0, min(255, round((point - 128) * a + 128)))
            new_sound2.add_value(np)

        return new_sound2


boxes_identifiers = {
    "PITCH": PitchBox,
    "DEVICE": DeviceBox,
    "MORE": MoreBox,
    "ADD": AddBox,
    "LESS": LessBox,
    "SINE": SinBox,
    "VALUE": ValueBox,
    "OUT": OutBox,
    "MULTI": MultiplyBox,
    "RAND": RandomBox,
    "SUM": SumBox,
    "DIST":DistortionBox,
    "AMP": AmpliBox,
    "DOP": DopplerBox
}
