from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, LVector3, PointLight, Spotlight
from direct.actor.Actor import Actor
from direct.task import Task
from panda3d.core import PerspectiveLens
import simplepbr

class AnimatedCharacter(ShowBase):
    def __init__(self):
        super().__init__()

        # Enable SimplePBR for realistic lighting and PBR materials
        simplepbr.init()

        # Load model with BOTH animations
        self.character = Actor(
            "lady.glb",  # Main model
            {
                "running": "lady.glb",    # Running animation
                "standing": "standing.glb"  # Standing animation
            }
        )
        self.character.reparentTo(self.render)
        self.character.setPos(0, 10, 0)

        # Start standing animation by default
        self.character.loop("standing")

        # Key states for movement
        self.keys = {"left": False, "right": False, "forward": False, "backward": False}
        self.is_moving = False  # To track if moving or standing

        # Keybindings (WASD only)
        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])

        # Add update loop
        self.taskMgr.add(self.update, "update")

        # Lights setup
        self.setup_lights()

        # Camera setup: Follow the character from behind
        self.camera_distance = 15
        self.camera_height = 5
        self.camera_offset = LVector3(0, -self.camera_distance, self.camera_height)

    def set_key(self, key, value):
        self.keys[key] = value

    def update(self, task):
        dt = globalClock.getDt()
        speed = 8 * dt  # Movement speed

        moving = False  # Temporary flag for this frame

        # Character movement (no up/down)
        if self.keys["left"]:
            self.character.setX(self.character, -speed)
            moving = True
        if self.keys["right"]:
            self.character.setX(self.character, speed)
            moving = True
        if self.keys["forward"]:
            self.character.setY(self.character, speed)
            moving = True
        if self.keys["backward"]:
            self.character.setY(self.character, -speed)
            moving = True

        # Handle animation
        if moving and not self.is_moving:
            self.character.loop("running")
            self.is_moving = True
        elif not moving and self.is_moving:
            self.character.loop("standing")
            self.is_moving = False

        # Character rotation (face the movement direction)
        if self.keys["left"]:
            self.character.lookAt(self.character.getPos() + LVector3(1, 0, 0))
        elif self.keys["right"]:
            self.character.lookAt(self.character.getPos() + LVector3(-1, 0, 0))
        elif self.keys["forward"]:
            self.character.lookAt(self.character.getPos() + LVector3(0, -1, 0))
        elif self.keys["backward"]:
            self.character.lookAt(self.character.getPos() + LVector3(0, 1, 0))

        # Make the camera follow the character
        self.camera.setPos(self.character.getPos() + self.camera_offset)
        self.camera.lookAt(self.character.getPos())

        return Task.cont

    def setup_lights(self):
        # Ambient light
        ambient = AmbientLight("ambient")
        ambient.setColor((1, 1, 1, 1))
        self.render.setLight(self.render.attachNewNode(ambient))

        # Directional light (like sun)
        directional = DirectionalLight("directional")
        directional.setDirection(LVector3(-1, -1, -1))
        directional.setColor((1, 1, 1, 1))
        directional_np = self.render.attachNewNode(directional)
        directional_np.setPos(0, 0, 20)
        self.render.setLight(directional_np)

        # Spotlight focused on the character
        spotlight = Spotlight("spotlight")
        spotlight.setColor((1, 1, 1, 1))
        spotlight.setLens(PerspectiveLens())
        spotlight_np = self.render.attachNewNode(spotlight)
        spotlight_np.setPos(0, 10, 10)
        spotlight_np.lookAt(self.character)
        self.render.setLight(spotlight_np)

        # Point light near the character
        point_light = PointLight("point_light")
        point_light.setColor((1, 0.9, 0.8, 1))  # Warm light
        point_light_np = self.render.attachNewNode(point_light)
        point_light_np.setPos(0, 5, 0)
        self.render.setLight(point_light_np)

# Run the app
app = AnimatedCharacter()
app.run()