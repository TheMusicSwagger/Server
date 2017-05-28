import sounds, config


class SoundBox(object):
    """
    Sound Box interface : you must implement the get function.
    """
    parents = None
    # array of parents
    custom_buff = None

    # buffer for custom value

    def __init__(self, *args, custom_buff=None):
        super(SoundBox, self).__init__()
        self.parents = args
        self.custom_buff = custom_buff

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
        value1 = self.parents[1].get()
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

    def process(self):
        return self.parents[0].get().add(self.parents[1].get(), self.parents[3].get())


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
        return sounds.WaveGenerator().sinusoid(config.SOUND_PROCESS_LENGTH, config.SOUND_DEFAULT_SAMPLERATE,
                                               self.parents[0].get())


class DeviceBox(SoundBox):
    """
    Get a value from a DeviceValue.

    Custom Buffer :
        DeviceValue object
    """

    def get(self):
        return self.custom_buff.get_value()


boxes_identifiers = {
    "PITCH": PitchBox,
    "DEVICE": DeviceBox,
    "MORE": MoreBox,
    "ADD": AddBox,
    "LESS": LessBox,
    "SINE": SinBox,
    "VALUE": ValueBox
}
