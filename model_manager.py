from direct.showbase.ShowBase import ShowBase
from panda3d.core import PandaNode, NodePath, CardMaker, TransformState, Vec3, Point3
from panda3d.bullet import (
    BulletRigidBodyNode,
    BulletBoxShape,
    BulletWorld,
)
from direct.interval.IntervalGlobal import Sequence
from direct.actor.Actor import Actor

PATH_ROAD_TEXTURE = "textures/asphalt.jpg"
PATH_TUNNEL_TEXTURE = "textures/tunnel.jpg"
PATH_CAR = "models/car.glb"
PATH_TUNNLE = "models/tunnel"
# プレイヤーのパスを設定
PATH_PLAYER = "models/player.glb"


# プレイヤー
class Player(NodePath):
    def __init__(self):
        super().__init__(BulletRigidBodyNode("player"))
        self.reparentTo(base.render)
        self.actor = Actor(PATH_PLAYER)
        self.actor.setName("playerModel")
        self.actor.setScale(1)

        # 向きと位置を設定

        self.actor.reparentTo(self)
        self.actor.loop("running")

        # リジッドボディの設定
        end, tip = self.actor.getTightBounds()
        size = tip - end
        half = size / 2
        center = tip - half
        self.node().addShape(BulletBoxShape(half), TransformState.makePos(center))

        # プレイヤーの座標

        # プレイヤーの速度

    # プレイヤーのジャンプ
    def jump(self):
        sec = Sequence(
            self.posInterval(0, Point3(self.getX(), self.getY(), 0)),
            self.posInterval(1, Point3(self.getX(), self.getY() + self.v_y, 5)),
            self.posInterval(0.5, Point3(self.getX(), self.getY() + self.v_y, 0)),
        )
        sec.start()

    # プレイヤーの初期化処理
    def cleanup(self):
        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None
        self.removeNode()


# トンネル
class Tunnel(NodePath):
    def __init__(self):
        super().__init__(PandaNode("tunnel"))
        self.reparentTo(base.render)
        self.model = base.loader.loadModel(PATH_TUNNLE)
        self.model.setName("tunnelModel")
        self.model.setScale(0.8)
        self.model.setHpr(0, 90, 0)
        tex = base.loader.loadTexture(PATH_TUNNEL_TEXTURE)
        self.model.setTexture(tex)
        self.model.reparentTo(self)


# 車の障害物
class Car(NodePath):
    def __init__(self):
        super().__init__(BulletRigidBodyNode("car"))
        self.reparentTo(base.render)
        self.model = base.loader.loadModel(PATH_CAR)
        self.model.setName("carModel")
        self.model.setScale(0.1)
        self.model.reparentTo(self)

        # リジッドボディの設定
        end, tip = self.model.getTightBounds()
        size = tip - end
        half = size / 2
        center = tip - half
        self.node().addShape(BulletBoxShape(half), TransformState.makePos(center))

        # 車の速度
        self.velocity = -0.4

    # 車の初期化処理
    def cleanup(self):
        self.model.removeNode()
        self.removeNode()


# グラウンド
class Ground(NodePath):
    def __init__(self):
        super().__init__(PandaNode("ground"))
        self.reparentTo(base.render)
        self.model = NodePath(PandaNode("groundModel"))
        card = CardMaker("card")
        size = 6
        card.setFrame(-size, size, -size, size)
        max_card = 50
        for y in range(max_card):
            for x in [-12, 12]:
                g = self.model.attachNewNode(card.generate())
                g.setP(-90)
                g.setPos(x, y * size * 2, 0)
        self.model.setColor(0.15, 0.15, 0.15)
        self.model.flattenStrong()
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(self)


# 道
class Road(NodePath):
    def __init__(self):
        super().__init__(PandaNode("road"))
        self.reparentTo(base.render)
        self.model = NodePath(PandaNode("roadModel"))
        card = CardMaker("card")
        size = 6
        card.setFrame(-size, size, -size, size)
        max_card = 50
        for y in range(max_card):
            r = self.model.attachNewNode(card.generate())
            r.setP(-90)
            r.setPos(0, y * size * 2, 0.1)
        tex = base.loader.loadTexture(PATH_ROAD_TEXTURE)
        self.model.setTexture(tex)
        self.model.flattenStrong()
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(self)


# ゲームシーン
class Scene:
    def __init__(self):
        # 背景色の設定
        base.setBackgroundColor(0, 0, 0)

        # 物理ワールドの設定
        self.physical_world = BulletWorld()

        # グラウンドをインスタンス化する
        self.ground = Ground()

        # 道をインスタンス化する
        self.road = Road()

        for y in range(15):
            self.tunnel = Tunnel()
            self.tunnel.setPos(0, y * 40, 0)


if __name__ == "__main__":
    base = ShowBase()
