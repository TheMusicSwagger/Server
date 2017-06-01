import time, pymysql, boxes as bxs
from communicator.communicator import Communicator
from sounds import SoundPlayer
from serv_config import Config as cfg


class DataCenter(object):
    """
    Center that saves last sent data to be able to retrieve it.
    """
    devices = {}

    # dict of available devices
    # {cuid:[channels...]}
    def __init__(self):
        super(DataCenter, self).__init__()

    def get(self, cuid, channel):
        value = 0
        if cuid in self.devices:
            value = self.devices[cuid][channel]
        return value

    def update(self, cuid, values):
        cfg.log(str(cuid) + " gave new data !")
        self.devices[cuid] = values


class ServerBrain(object):
    """
    The part of the server that have a control over communication and sound generation
    """
    communicator = None
    database = None
    # sql database for config
    last_update = None
    tree = None
    # the current tree
    output = None
    # the sound output of the current tree
    player = None
    # the sound player that allows to play sounds
    datacenter = None

    # the datacenter where all last device values are stores
    def __init__(self, data_center):
        try:
            self.database = pymysql.connect(host=cfg.DB_IP, user=cfg.DB_USER, password=cfg.DB_PASS, db=cfg.DB_NAME,
                                            charset=cfg.DB_CHARSET)
        except pymysql.err.Error:
            cfg.warn("Database setup error !")
        self.communicator = Communicator(True, data_callback=lambda a, b: data_center.update(a, b))
        self.player = SoundPlayer()
        self.datacenter = datacenter

    def stop(self):
        self.player.kill()
        self.communicator.stop()

    def db_query(self, query, args=()):
        cursor = self.database.cursor()
        cursor.execute(query, args)
        dat = cursor.fetchall()
        cursor.close()
        self.database.commit()
        return dat

    def update_tree(self):
        """
        Generate a tree of boxes from the cfg.
        """
        boxes = {}
        rboxes = self.db_query("SELECT * FROM " + cfg.TB_BOXES)
        for box in rboxes:
            # ID(0) TYPE(1) BOX_ID(2) SPEC_PARAM(3)
            if box[1] == "DEVICE":
                boxes[box[2]] = bxs.boxes_identifiers[box[1]](self.datacenter, box[3])
            else:
                boxes[box[2]] = bxs.boxes_identifiers[box[1]](box[3])
        rlinks = self.db_query("SELECT * FROM " + cfg.TB_LINKS)
        for link in rlinks:
            # ID(0) FROM_B(1) TO_B(2) WHERE_L(3)
            boxes[link[2]].set_parent(link[3], boxes[link[1]])
        self.tree = boxes
        self.output = self.tree[0]

    def check_update(self):
        very_last_update = self.db_query("SELECT ID FROM " + cfg.TB_UPDATE_NUMBER)[0]
        if self.last_update:
            if self.last_update < very_last_update:
                self.update_tree()
                self.last_update = very_last_update
        else:
            self.last_update = very_last_update
            self.update_tree()

    def make_sound(self):
        beginning_time = time.time()
        self.check_update()
        # generate sound from tree
        # feed the player
        sound = None
        try:
            sound = self.output.get()
        except Exception as e:
            print("Configuration error : ", e)
            self.player.pause()
        if sound is not None:
            self.player.play(sound)
        while time.time() - beginning_time < cfg.SOUND_PROCESS_LENGTH / 1000:
            pass
            # wait to make an other sound


if __name__ == "__main__":
    device = brain = None
    try:
        datacenter = DataCenter()
        brain = ServerBrain(datacenter)
        while True:
            brain.make_sound()
    except KeyboardInterrupt as e:
        print("<Ctrl-c> = user quit")
    finally:
        print("Exiting...")
        if brain:
            brain.stop()
