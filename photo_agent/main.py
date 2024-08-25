from enum import Enum
from typing import Union


class Position:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class Angle:
    def __init__(self, value=0):
        if value < 0 or value > 360:
            raise ValueError("Angle value must be between 0 and 360")
        self.value = value


class ISO:
    def __init__(self, value=1500):
        if value < 100 or value > 128000:
            raise ValueError("ISO value must be between 100 and 128000")
        self.value = value


class Aperture:
    def __init__(self, value=5.6):
        if value < 1.4 or value > 22:
            raise ValueError("Aperture value must be between 1.4 and 22")
        self.value = value


class ShutterSpeed:
    def __init__(self, value=1 / 100):
        if value < 1 / 800000 or value > 30:
            raise ValueError("Shutter speed value must be between 1/800000 and 30")
        self.value = value


class Camera:
    def __init__(
        self,
        position=Position(5, 5, 5),
        iso=ISO(),
        aperture=Aperture(),
        shutter_speed=ShutterSpeed(),
    ):
        self.position = position
        self.iso = iso
        self.shutter_speed = shutter_speed
        self.aperture = aperture

    def init_from_config(self, config):
        self.position = Position(
            config["position"]["x"], config["position"]["y"], config["position"]["z"]
        )
        self.iso = ISO(config["iso"])
        self.shutter_speed = ShutterSpeed(config["shutter_speed"])
        self.aperture = Aperture(config["aperture"])


class Subject:
    def __init__(self, position=Position(0, 5, 5)):
        self.position = position

    def init_from_config(self, config):
        self.position = Position(
            config["position"]["x"], config["position"]["y"], config["position"]["z"]
        )


class LightVariant(Enum):
    STROBE = 1
    SPEED_LIGHT = 2


class StrobeConfig:
    def __init__(self, power=100, intensity=1, speed=1 / 800):
        # validate fields
        if power < 100 or power > 1500:
            raise ValueError("Power must be between 100 and 1500")
        if intensity < 1 / 64 or intensity > 1:
            raise ValueError("Intensity must be between 1 / 64 and 1")
        if speed < 1 / 10000 or speed > 1 / 800:
            raise ValueError("Speed must be between 1/ 10000 and 1/800 ")
        self.power = power
        self.intensity = intensity
        self.speed = speed


class SpeedLightConfig:
    def __init__(self, power=60, intensity=1, speed=1 / 1000):
        # validate fields
        if power < 100 or power > 1500:
            raise ValueError("Power must be between 100 and 1500")
        if intensity < 1 / 128 or intensity > 1:
            raise ValueError("Intensity must be between 1 / 64 and 1")
        if speed < 1 / 30000 or speed > 1 / 1000:
            raise ValueError("Speed must be between 1/30000 and 1/1000")
        self.power = power
        self.intensity = intensity
        self.speed = speed


class Light:
    def __init__(
        self,
        config: Union[StrobeConfig, SpeedLightConfig],
        variant: LightVariant,
        position: Position,
        angle: Angle,
    ):
        self.variant = variant
        self.config = config
        self.position = position
        self.angle = angle
        self.modifier = None
        self.filters = []

    def set_modifier(self, modifier):
        self.modifier = modifier

    def add_filter(self, filter):
        self.filters.append(filter)

    def init_from_config(self, config):
        self.position = Position(
            config["position"]["x"], config["position"]["y"], config["position"]["z"]
        )
        self.angle = Angle(config["angle"])
        if config["variant"] == "STROBE":
            self.variant = LightVariant.STROBE
            self.config = StrobeConfig(
                config["config"]["power"],
                config["config"]["intensity"],
                config["config"]["speed"],
            )
        elif config["variant"] == "SPEED_LIGHT":
            self.variant = LightVariant.SPEED_LIGHT
            self.config = SpeedLightConfig(
                config["config"]["power"],
                config["config"]["intensity"],
                config["config"]["speed"],
            )
        else:
            raise ValueError("Invalid light variant")


class ModifierVariant(Enum):
    SOFTBOX = 1
    UMBRELLA = 2
    REFLECTOR = 3
    PARABOLIC = 4
    BEAUTYDISH = 5
    SNOOT = 6


class SoftBoxConfig(Enum):
    def __init__(self, height=10, width=30):
        if height < 10 or height > 80:
            raise ValueError("Height must be between 10 and 80")
        if width < 30 or width > 80:
            raise ValueError("Width must be between 30 and 80")
        self.height = height
        self.width = width


class UmbrellaConfig(Enum):
    def __init__(self, radius=30):
        if radius < 30 or radius > 120:
            raise ValueError("Radius must be between 30 and 120")
        self.radius = radius


class ReflectorConfig(Enum):
    def __init__(self, color="gold", radius=30):
        if radius < 30 or radius > 1000:
            raise ValueError("Radius must be between 30 and 1000")
        if color not in ["gold", "silver", "white", "black"]:
            raise ValueError("Color must be gold, silver, white or black")
        self.color = color
        self.radius = radius


class ParabolicConfig(Enum):
    def __init__(self, radius=30):
        if radius < 30 or radius > 120:
            raise ValueError("Radius must be between 30 and 120")
        self.radius = radius


class BeautyDishConfig(Enum):
    def __init__(self, radius=10):
        if radius < 10 or radius > 30:
            raise ValueError("Radius must be between 10 and 30")
        self.radius = radius


class SnootConfig(Enum):
    def __init__(self, aperture=0):
        if aperture < 0 or aperture > 22:
            raise ValueError("Aperture must be between 0 and 22")
        self.aperture = aperture


class Modifier:
    def __init__(
        self,
        variant: ModifierVariant,
        config: Union[
            SoftBoxConfig,
            UmbrellaConfig,
            ReflectorConfig,
            ParabolicConfig,
            BeautyDishConfig,
            SnootConfig,
        ],
    ):
        self.variant = variant
        self.config = config

    def init_from_config(self, config):
        if config["variant"] == "SOFTBOX":
            self.variant = ModifierVariant.SOFTBOX
            self.config = SoftBoxConfig(
                config["config"]["height"],
                config["config"]["width"],
            )
        elif config["variant"] == "UMBRELLA":
            self.variant = ModifierVariant.UMBRELLA
            self.config = UmbrellaConfig(
                config["config"]["radius"],
            )
        elif config["variant"] == "REFLECTOR":
            self.variant = ModifierVariant.REFLECTOR
            self.config = ReflectorConfig(
                config["config"]["color"],
                config["config"]["radius"],
            )
        elif config["variant"] == "PARABOLIC":
            self.variant = ModifierVariant.PARABOLIC
            self.config = ParabolicConfig(
                config["config"]["radius"],
            )
        elif config["variant"] == "BEAUTYDISH":
            self.variant = ModifierVariant.BEAUTYDISH
            self.config = BeautyDishConfig(
                config["config"]["radius"],
            )
        elif config["variant"] == "SNOOT":
            self.variant = ModifierVariant.SNOOT
            self.config = SnootConfig(
                config["config"]["aperture"],
            )
        else:
            raise ValueError("Invalid modifier variant")


class FilterVariant(Enum):
    DIFFUSER = 1
    GEL = 2
    ND = 3
    GRID = 4


class GelConfig:
    def __init__(self, color: str):
        self.color = color


class NDConfig:
    def __init__(self, stops: int):
        if stops < 1 or stops > 10:
            raise ValueError("Stops must be between 1 and 10")
        self.stops = stops


class GridConfig:
    def __init__(self, type: str):
        if type not in ["honeycomb", "square"]:
            raise ValueError("Type must be honeycomb or square")
        self.type = type


class DiffuserConfig:
    def __init__(self, type: str):
        if type not in ["soft", "hard"]:
            raise ValueError("Type must be soft or hard")
        self.type = type


class PhotoEnvironment:
    def __init__(self):
        self.camera = Camera()
        self.subject = Subject()
        self.lights = []
