import os,config,uuid,time,pymysql
from communicator.communicator import Communicator
from sounds import SoundPlayer

class DataCenter(object):
    """
    Center that saves last sent data to be able to retrieve it.
    """
    devices={}
    # dict of available devices
    # {cuid:[channels...]}
    def __init__(self):
        super(DataCenter, self).__init__()

    def get(self,cuid,channel):
        value=0
        if cuid in self.devices:
            value=self.devices[cuid][channel]
        return value

    def update(self,cuid,values):
        self.devices[cuid]=values


class ServerBrain(object):
    """
    The part of the server that have a control over communication and sound generation
    """
    global_uid = None
    communicator = None
    database = None
    # sql database for config
    last_update=None
    output=None
    # the sound output of the current tree
    player=None
    # the sound player that allows to play sounds

    def __init__(self,data_center):
        if os.path.isfile(config.GUID_FILENAME):
            guidfile = open(config.GUID_FILENAME, "r")
            self.global_uid = guidfile.read()
            guidfile.close()
        else:
            guidfile = open(config.GUID_FILENAME, "w")
            self.global_uid = str(uuid.uuid4()).replace("-", "")
            guidfile.write(self.global_uid)
            guidfile.close()
        config.log(self.get_guid())
        try:
            self.database = pymysql.connect(host=config.DB_IP, user=config.DB_USER, password=config.DB_PASS, db=config.DB_NAME,
                                            charset=config.DB_CHARSET)
        except pymysql.err.Error:
            config.warn("Database setup error !")
        self.communicator = Communicator(True,self.get_guid(),lambda a,b:data_center.update(a,b))
        self.player=SoundPlayer()

    def get_guid(self):
        """
        :return: 'self.global_uid'
        """
        return self.global_uid

    def stop(self):
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
        Generate a tree of boxes from the configuration.
        """


    def check_update(self):
        very_last_update=self.db_query("SELECT ID FROM " + config.TB_UPDATE_NUMBER)[0]
        if self.last_update:
            if self.last_update<very_last_update:
                self.update_tree()
        else:
            self.last_update=very_last_update
            self.update_tree()

    def make_sound(self):
        beginning_time=time.time()
        self.check_update()
        sound=self.output.get()
        # generate sound from tree
        self.player.play(sound)
        # feed the player
        while time.time()-beginning_time<config.SOUND_PROCESS_LENGTH:
            pass
            # wait to make an other sound




if __name__ == "__main__":
    device=brain=None
    try:
        datacenter=DataCenter()
        brain = ServerBrain(datacenter)
        while True:
            brain.make_sound()
    except KeyboardInterrupt as e:
        print("<Ctrl-c> = user quit")
    finally:
        print("Exiting...")
        if brain:
            brain.stop()