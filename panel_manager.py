from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *

PATH_BOLD_FONT = "fonts/PixelMplus10-Bold.ttf"
PATH_REGULAR_FONT = "fonts/PixelMplus10-Regular.ttf"


class GameStartScene:
    def __init__(self):
        # fontの設定
        self.font = base.loader.loadFont(PATH_BOLD_FONT)
        self.title_menu_backdrop = DirectFrame(
            frameColor=(0, 0, 0, 1), frameSize=(-0.7, 0.7, -0.7, 0.7)
        )
        self.title_menu = DirectFrame(frameColor=(1, 1, 1, 0))
        title = DirectLabel(
            text="Be-En RUN",
            scale=0.2,
            pos=(0, 0, 0.4),
            parent=self.title_menu,
            relief=None,
            text_font=self.font,
            text_fg=(1, 1, 1, 1),
        )
        sub_title = DirectLabel(
            text="Endless Run Game",
            scale=0.1,
            pos=(0, 0, 0),
            parent=self.title_menu,
            relief=None,
            text_font=self.font,
            text_fg=(1, 1, 1, 1),
        )
        self.start_btn = DirectButton(
            text="Start Game",
            command="",
            pos=(0, 0, -0.2),
            parent=self.title_menu,
            scale=0.1,
            text_font=self.font,
            frameSize=(-4, 4, -1, 1),
            text_scale=0.75,
            relief=DGG.FLAT,
            text_pos=(0, -0.2),
        )
        self.start_btn.setTransparency(True)


class GameOverScene:
    def __init__(self):
        # fontの設定
        self.font = base.loader.loadFont(PATH_BOLD_FONT)
        self.game_over_screen = DirectDialog(
            frameSize=(-2, 2, -1, 1), pos=(0, 0, 0), 
        )
        label = DirectLabel(
            text="Game Over!",
            parent=self.game_over_screen,
            scale=0.2,
            pos=(0, 0, 0.55),
            text_font=self.font,
        )

        self.final_score_label = DirectLabel(
            text="",
            parent=self.game_over_screen,
            scale=0.1,
            pos=(0, 0, 0),
            text_font=self.font,
        )
        self.restart_btn = DirectButton(
            text="Restart",
            command="",
            pos=(-0.3, 0, -0.2),
            parent=self.game_over_screen,
            text_font=self.font,
            scale=0.07,
        )
        self.quit_btn = DirectButton(
            text="Quit",
            command="",
            pos=(0.3, 0, -0.2),
            parent=self.game_over_screen,
            text_font=self.font,
            scale=0.07,
        )


if __name__ == "__main__":
    base = ShowBase()
