from direct.showbase.ShowBase import ShowBase
from panda3d.core import AudioSound

PATH_BGM = "sounds/bgm/bgm.mp3"
PATH_FOOT = "sounds/se/run.mp3"
PATH_EXPLOSION = "sounds/se/explosion.mp3"


class BGM:
    def __init__(self):
        super().__init__()
        self.sound_bgm = base.loader.loadMusic(PATH_BGM)


class SE:
    def __init__(self):
        super().__init__()
        self.sound_foot = base.loader.loadMusic(PATH_FOOT)
        self.sound_foot.setLoop(True)
        self.sound_foot.setVolume(10)

        self.sound_explosion = base.loadMusic(PATH_EXPLOSION)


if __name__ == "__main__":
    base = ShowBase()