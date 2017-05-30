import time
class Config:
    SOUND_PROCESS_LENGTH=50
    SOUND_DEFAULT_SAMPLERATE=22000
    # sound constants

    DB_IP = "localhost"
    DB_USER = "notroot"
    DB_PASS = ""
    DB_NAME = "themusicswagger_db"
    DB_CHARSET = "utf8"
    # database infos to connect
    TB_UPDATE_NUMBER="update_number"
    TB_BOXES="boxes"
    TB_LINKS="links"
    ################################################
    # Logging functions                            #
    ################################################
    DEBUG_MODE = True
    RAISE_ERROR = False
    def log(text):
        if Config.DEBUG_MODE:
            print("[---] [" + str(time.time()) + ")]", text)


    def warn(text):
        if Config.RAISE_ERROR:
            raise Exception(text)
        else:
            print("[!!!] [" + str(time.time()) + ")]", text)