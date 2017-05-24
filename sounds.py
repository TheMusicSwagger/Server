import math, subprocess, threading, time


class WaveSound(object):
    raw_data = b""
    length = 0
    sample_rate = None
    bits_per_sample = None
    num_channels = None

    def __init__(self, sample_rate=22000, bits_per_sample=8, num_channels=1):
        super().__init__()
        self.sample_rate = sample_rate
        self.bits_per_sample = bits_per_sample
        self.num_channels = num_channels

    def add_value(self, val):
        assert type(val) == int
        self.raw_data += val.to_bytes(self.get_bitpersample() // 8, byteorder="big")
        self.length += 1
        return self

    def __add__(self, other):
        assert type(other) == WaveSound
        assert self.get_samplerate() == other.get_samplerate()
        assert self.get_bitpersample() == other.get_bitpersample()
        assert self.get_num_channels() == other.get_num_channels()
        return WaveSound(self.get_samplerate()).set_data(self.get_data() + other.get_data())

    def set_data(self, data):
        self.raw_data = data
        self.length = len(data)
        return self

    def set_num_channels(self, num_channels):
        self.num_channels = int(num_channels)
        return self

    def set_samplerate(self, sample_rate):
        self.sample_rate = int(sample_rate)
        return self

    def set_bitpersample(self, bits_per_sample):
        self.bits_per_sample = int(bits_per_sample)
        return self

    def get_num_channels(self):
        return self.num_channels

    def get_samplerate(self):
        return self.sample_rate

    def get_bitpersample(self):
        return self.bits_per_sample

    def get_data(self):
        return self.raw_data

    def get_value(self, i):
        return self.get_data()[i]

    def get_copy(self):
        """
        TO CHECK
        """
        return WaveSound(sample_rate=self.get_samplerate(), bits_per_sample=self.get_bitpersample(),
                         num_channels=self.get_num_channels()).set_data(self.get_data())

    def get_length(self):
        return self.length

    def get_time(self):
        return self.get_length() / self.get_samplerate()

    def open(self, filename):
        # TODO : implement open method
        pass

    def save(self, filename):
        wave_file = open(filename, 'wb')

        subchunk1_size = 16  # (PCM)
        subchunk2_size = int(self.get_length() * self.get_bitpersample() / 8)

        # RIFF Header
        wave_file.write(b"RIFF")
        wave_file.write((4 + (8 + subchunk1_size) + (8 + subchunk2_size)).to_bytes(4, byteorder='little'))
        wave_file.write(b"WAVE")

        # SubChunk1
        wave_file.write(b"fmt ")
        wave_file.write(subchunk1_size.to_bytes(4, byteorder="little"))
        wave_file.write((1).to_bytes(2, byteorder="little"))  # (No compression)
        wave_file.write((1).to_bytes(2, byteorder="little"))  # (Mono)
        wave_file.write(self.get_samplerate().to_bytes(4, byteorder="little"))  # (Sample rate)
        wave_file.write(
            int(self.get_samplerate() * self.get_bitpersample() / 8).to_bytes(4, byteorder="little"))  # (Bit rate)
        wave_file.write(int(self.get_bitpersample() / 8).to_bytes(2, byteorder="little"))  # (Block align)
        wave_file.write(self.get_bitpersample().to_bytes(2, byteorder="little"))  # (Bit per sample)

        # SubChunk2
        wave_file.write(b"data")
        wave_file.write(subchunk2_size.to_bytes(4, byteorder="little"))  # (Bit per sample)
        wave_file.write(self.get_data())

        wave_file.close()
        return self

    def get_data_as_int_array(self):
        return [e for e in self.get_data()]

    def add(self, sound, fac=0.5):
        return self.add_part(sound,0,fac)

    def add_part(self,sound,pos,fac=0.5):
        assert self.get_samplerate() == sound.get_samplerate()
        assert self.get_bitpersample() == sound.get_bitpersample()
        assert self.get_num_channels() == sound.get_num_channels()
        new_data = b''
        for i in range(pos):
            new_data += int(self.get_value(i).to_bytes(self.get_bitpersample() // 8, "big"))
        for i in range(pos,pos+sound.get_length()):
            if i>self.get_length():
                break
            new_data += int((self.get_value(i) * (1 - fac)) + (sound.get_value(i-pos) * (fac))).to_bytes(
                self.get_bitpersample() // 8, "big")
        for i in range(pos+sound.get_length(),self.get_length()):
            new_data += int(self.get_value(i).to_bytes(self.get_bitpersample() // 8, "big"))
        self.set_data(new_data)
        return self



class WaveGenerator():
    def sinusoid(self, time=1000, sample_rate=22000, freq=440):
        sound = WaveSound(sample_rate)
        for i in range(int(time * sample_rate / 1000)):
            v = math.sin(2 * math.pi * i * freq / sample_rate) * 127 + 127
            sound.add_value(int(v))
        return sound

    def advanced_sinusoid(self, periods=100, sample_rate=22000, freq=440):
        sound = WaveSound(sample_rate)
        period = WaveSound(sample_rate)
        for i in range(int(sample_rate / freq)):
            v = math.sin(2 * math.pi * (i / (sample_rate / freq))) * 127 + 127
            period.add_value(int(v))
        for i in range(periods):
            sound += period
        return sound

    def progressiv(self, time=1000, sample_rate=22000, freqa=440, freqb=880):
        sound = WaveSound(sample_rate)
        n = int(time * sample_rate / 1000)
        for i in range(n):
            v = math.sin(2 * math.pi * i * (freqa + (i * (freqb - freqa) / n)) / sample_rate) * 127 + 127
            sound.add_value(int(v))
        return sound

try:
    import ossaudiodev as ossa
    OSSAUDIO_AVAILABLE = True
except ImportError:
    print("ossaudiodev not found !")
try:
    import winaudio as wina
    WINAUDIO_AVAILABLE = True
except ImportError:
    print("winaudio not found !")


class SoundOutput():
    device = None
    # store the object to send the sound on
    type = None

    # 0: OSS, 1: WIN
    def __init__(self, device=None):
        if OSSAUDIO_AVAILABLE:
            self.type = 0
            devname = device
            if device is None:
                # finding device name
                (out, err) = subprocess.Popen(["ls /dev | grep dsp"], stdout=subprocess.PIPE, shell=True).communicate()
                devname = '/dev/' + out.decode("ascii")[:-1]
            # opening device
            dsp = None
            tries = 0
            while True:
                try:
                    tries += 1
                    dsp = ossa.open(devname, 'w')
                    break
                except Exception as e:
                    if tries >= 10:
                        print("Can't open device :", e)
                        break
                    else:
                        time.sleep(0.5)
            self.device = dsp
        elif WINAUDIO_AVAILABLE:
            self.type = 1
            # TODO : Windows support
            print("Currently not supporting Windows")
        else:
            print("No modules found !")

    def play(self, sound):
        if self.type == 0:
            self.device.setparameters(ossa.AFMT_MPEG, sound.get_num_channels(), sound.get_samplerate())
            self.device.write(sound.get_data())
        elif self.type == 1:
            # TODO : Windows support
            print("Currently not supporting Windows")
        else:
            print("Can't play sound !")

    def close(self):
        self.device.close()


class SoundPlayer(threading.Thread):
    is_running = None
    is_paused = None
    output = None
    last_sound = None
    # buffer to store the last played sound (play until new is received)
    to_be_played = None

    # list of sounds to be played (pop to last sound)
    def __init__(self):
        super(SoundPlayer, self).__init__()
        self.output = SoundOutput()
        self.is_running = True
        self.is_paused = True
        self.to_be_played = []
        self.daemon = True
        self.start()

    def play(self, sound):
        self.to_be_played.append(sound)
        self.is_paused = False

    def run(self):
        while self.is_running:
            if self.is_paused:
                time.sleep(0.01)
            else:
                if len(self.to_be_played) > 0:
                    self.last_sound = self.to_be_played.pop(0)
                self.output.play(self.last_sound)

    def kill(self, force=False):
        while not force and len(self.to_be_played) > 0:
            time.sleep(0.001)
        self.is_running = False
        self.output.close()
        self.join()

    def pause(self):
        self.is_paused = True