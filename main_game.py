from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panel_manager import GameStartScene, GameOverScene
from model_manager import Scene,Player, Car
from sound_manager import SE, BGM
import random

MOVE_RIGHT = "move_right"
MOVE_LEFT = "move_left"
MOVE_UP = "move_up"


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        # プレイヤーの変数
        self.player = None

        # ゲームフラグ設定
        self.is_game = False

        # キーボード入力設定

        # 車の設定
        self.spawn_x = [-2.5, 2.5]
        self.cars = []
        self.max_cars = 5

        # 車を発生させる時間
        self.spawn_car_time = 0
        self.spawn_car_interval = 5

        # 当たり判定の設定
        self.result = None
        self.is_contact = False

        # サウンドの設定
        self.bgm = BGM()
        self.se = SE()
        self.bgm.sound_bgm.play()

        # 毎フレーム読み込まれる処理を登録
        self.taskMgr.add(self.update, "update")

        # シーンの設定
        self.scene = Scene()

        # カメラの初期設定
        self.disableMouse()
        self.camera.setPos(0, -8, 3)
        self.camera.setHpr(0, -10, 0)

        # ゲームスタートシーンの読み込み
        self.game_start_scene = GameStartScene()
        self.game_start_scene.start_btn["command"] = self.start

        # ゲームオーバーシーンの読み込み
        self.game_over_scene = GameOverScene()
        self.game_over_scene.restart_btn["command"] = self.start
        self.game_over_scene.quit_btn["command"] = self.quit

        # 初期設定ではゲームオーバーシーンは非表示
        self.game_over_scene.game_over_screen.hide()


    # スタート画面でスタートが押された時にメインに移る関数
    def start(self):
        # ゲームスタート時には画面を非表示にする
        self.game_over_scene.game_over_screen.hide()
        self.game_start_scene.title_menu.hide()
        self.game_start_scene.title_menu_backdrop.hide()

        # プレイヤーの初期化処理
        if self.player != None:
            self.player.cleanup()

        # 効果音の切り替え
        self.bgm.sound_bgm.stop()
        self.se.sound_foot.play()

        # ゲームフラグをオンにする
        self.is_game = True

        # プレイヤーのインスタンス化
        self.player = Player()
        # カメラを追随する

        # プレイヤーが初期位置のときに車を発生させる
        self.spawn_car(p_y=0)

        # プレイヤーを物理ワールドにアタッチする
        self.scene.physical_world.attachRigidBody(self.player.node())

    # 初期化する関数
    def cleanup(self):
        self.is_contact = False
        self.is_game = False
        self.scene.physical_world.removeRigidBody(self.player.node())
        for car in self.cars:
            self.scene.physical_world.removeRigidBody(car.node())
            car.cleanup()
        self.cars = []

    # ゲームオーバー画面でやめるが押された時にメインにスタート画面に移る関数
    def quit(self):
        # ゲームオーバー画面を非表示にしてスタート画面を表示する
        self.game_start_scene.title_menu.show()
        self.game_start_scene.title_menu_backdrop.show()
        self.game_over_scene.game_over_screen.hide()

        # 効果音を切り替える
        self.se.sound_explosion.stop()
        self.bgm.sound_bgm.play()
        self.game_over_scene.game_over_screen.hide()
        # 初期化処理
        if self.player != None:
            self.player.cleanup()
            self.camera.reparentTo(base.render)

    # 車を出現させる関数
    def spawn_car(self, p_y):
        if len(self.cars) < self.max_cars:
            c_x = random.choice(self.spawn_x)
            car = Car()
            # 常にプレイヤーの前方から発生する
            c_y = p_y + 100
            car.setPos(c_x, c_y, 0)
            self.cars.append(car)
            # 物理ワールドにリジッドボディをアタッチする
            for car in self.cars:
                self.scene.physical_world.attachRigidBody(car.node())

    # 毎フレーム行う処理
    def update(self, task):
        if self.is_game:
            # フレーム間の間隔を取得
            dt = globalClock.getDt()

            # プレイヤーの横移動の速度を0に更新する処理

            # プレイヤーの座標を取得する

            # 矢印キーが入力された時のプレイヤーの処理

            # プレイヤーの位置を更新する処理

            # 距離によって車が出現する頻度を変える
            self.spawn_car_interval = 10 - self.player.p_y / 20

            # 一定時間経過したら車を出現させる処理
            self.spawn_car_time += dt
            if self.spawn_car_time > self.spawn_car_interval:
                self.spawn_car(p_y=self.player.p_y)
                self.spawn_car_time = 0

            cars = []
            for car in self.cars:
                # 車を走らせる処理
                car.setY(car, car.velocity)
                # 通り過ぎた車を消去する処理
                if car.getY() < self.player.p_y:
                    # 車のリジッドボディを削除する
                    self.scene.physical_world.removeRigidBody(car.node())
                    car.cleanup()
                else:
                    cars.append(car)
            self.cars = cars

            # 当たり判定の処理
            self.scene.physical_world.doPhysics(dt)
            if not self.is_contact:
                self.result = self.scene.physical_world.contactTest(self.player.node())
                if self.result.getNumContacts() > 0:
                    self.is_contact = True
                    if self.game_over_scene.game_over_screen.isHidden():
                        # 効果音の切り替え
                        self.se.sound_foot.stop()
                        self.se.sound_explosion.play()
                        # 画面の表示
                        self.game_over_scene.final_score_label["text"] = "%s(m)" % (
                            format(self.player.p_y, ".2f")
                        )
                        self.game_over_scene.game_over_screen.show()
                    self.cleanup()

        return task.cont


app = Main()
app.run()
