from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, LVector3, PointLight, Spotlight
from direct.actor.Actor import Actor
from direct.task import Task
from panda3d.core import PerspectiveLens

class AnimatedCharacter(ShowBase):
    def __init__(self):
        super().__init__()

        # Load model and animation
        self.character = Actor("beast3.glb", {"running": "beast3.glb"})
        self.character.reparentTo(self.render)
        self.character.setPos(0, 10, 0)

        # Flag to track animation
        self.keys = {"left": False, "right": False, "forward": False, "backward": False, "up": False, "down": False}
        self.is_moving = False  # To track animation state

        # Keybindings (WASD + Up/Down for 3D movement)
        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])
        self.accept("space", self.set_key, ["up", True])  # Jump or move up
        self.accept("space-up", self.set_key, ["up", False])
        self.accept("control", self.set_key, ["down", True])  # Move down
        self.accept("control-up", self.set_key, ["down", False])

        # Add update loop
        self.taskMgr.add(self.update, "update")

        # Lights: Improved lighting with stronger lights
        self.setup_lights()

        # Camera setup: Follow the character from behind
        self.camera_distance = 15
        self.camera_height = 5
        self.camera_offset = LVector3(0, -self.camera_distance, self.camera_height)

    def set_key(self, key, value):
        self.keys[key] = value

    def update(self, task):
        dt = globalClock.getDt()
        speed = 8 * dt  # Increased speed for more realistic movement

        moving = False  # Temporary flag for this frame

        # Character movement in 3D
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
        if self.keys["up"]:  # Move upwards (jumping)
            self.character.setZ(self.character, speed)
            moving = True
        if self.keys["down"]:  # Move downwards
            self.character.setZ(self.character, -speed)
            moving = True

        # Handle animation: play only if moving
        if moving and not self.is_moving:
            self.character.loop("running")
            self.is_moving = True
        elif not moving and self.is_moving:
            self.character.stop()
            self.is_moving = False

        # Rotate the character to face the direction of movement
        if self.keys["left"]:
            self.character.lookAt(self.character.getPos() + LVector3(-1, 0, 0))
        if self.keys["right"]:
            self.character.lookAt(self.character.getPos() + LVector3(1, 0, 0))
        if self.keys["forward"]:
            self.character.lookAt(self.character.getPos() + LVector3(0, 1, 0))
        if self.keys["backward"]:
            self.character.lookAt(self.character.getPos() + LVector3(0, -1, 0))

        # Make the camera follow the character
        camera.setPos(self.character.getPos() + self.camera_offset)
        camera.lookAt(self.character.getPos())

        return Task.cont

    def setup_lights(self):
        # Ambient light (global lighting)
        ambient = AmbientLight("ambient")
        ambient.setColor((1, 1, 1, 1))  # Full intensity white light
        self.render.setLight(self.render.attachNewNode(ambient))

        # Directional light (simulating sunlight)
        directional = DirectionalLight("directional")
        directional.setDirection(LVector3(-1, -1, -1))
        directional.setColor((1, 1, 1, 1))  # White light at full intensity
        directional_np = self.render.attachNewNode(directional)
        directional_np.setPos(0, 0, 20)  # Position the directional light above the scene
        self.render.setLight(directional_np)

        # Spotlight: To focus more on the character
        spotlight = Spotlight("spotlight")
        spotlight.setColor((1, 1, 1, 1))  # Full intensity white light
        spotlight.setLens(PerspectiveLens())  # A lens for the spotlight
        spotlight_np = self.render.attachNewNode(spotlight)
        spotlight_np.setPos(0, 10, 10)  # Position the spotlight above and in front of the character
        spotlight_np.lookAt(self.character)  # Point the spotlight at the character
        self.render.setLight(spotlight_np)

        # Point light (additional localized light near the character)
        point_light = PointLight("point_light")
        point_light.setColor((1, 0.9, 0.8, 1))  # Soft warm light
        point_light_np = self.render.attachNewNode(point_light)
        point_light_np.setPos(0, 5, 0)  # Positioning near the character
        self.render.setLight(point_light_np)

# Run the app
app = AnimatedCharacter()
app.run()