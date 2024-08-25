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

    @classmethod
    def from_config(cls, config):
        position = Position(
            config["position"]["x"], config["position"]["y"], config["position"]["z"]
        )
        iso = ISO(config["iso"])
        shutter_speed = ShutterSpeed(config["shutter_speed"])
        aperture = Aperture(config["aperture"])
        return cls(position, iso, aperture, shutter_speed)


class Subject:
    def __init__(self, position=Position(0, 5, 5)):
        self.position = position

    @classmethod
    def from_config(cls, config):
        position = Position(
            config["position"]["x"], config["position"]["y"], config["position"]["z"]
        )
        return cls(position)


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

    @classmethod
    def from_config(cls, config):
        position = Position(
            config["position"]["x"], config["position"]["y"], config["position"]["z"]
        )
        angle = Angle(config["angle"])
        if config["variant"] == "STROBE":
            variant = LightVariant.STROBE
            light_config = StrobeConfig(
                config["config"]["power"],
                config["config"]["intensity"],
                config["config"]["speed"],
            )
        elif config["variant"] == "SPEED_LIGHT":
            variant = LightVariant.SPEED_LIGHT
            light_config = SpeedLightConfig(
                config["config"]["power"],
                config["config"]["intensity"],
                config["config"]["speed"],
            )
        else:
            raise ValueError("Invalid light variant")

        light = cls(light_config, variant, position, angle)

        if "modifier" in config:
            light.modifier = Modifier.from_config(config["modifier"])
        if "filters" in config:
            for filter_config in config["filters"]:
                light.filters.append(Filter.from_config(filter_config))
        return light


class ModifierVariant(Enum):
    SOFTBOX = 1
    UMBRELLA = 2
    REFLECTOR = 3
    PARABOLIC = 4
    BEAUTYDISH = 5
    SNOOT = 6


class SoftBoxConfig:
    def __init__(self, height=10, width=30):
        if height < 10 or height > 80:
            raise ValueError("Height must be between 10 and 80")
        if width < 30 or width > 80:
            raise ValueError("Width must be between 30 and 80")
        self.height = height
        self.width = width


class UmbrellaConfig:
    def __init__(self, radius=30):
        if radius < 30 or radius > 120:
            raise ValueError("Radius must be between 30 and 120")
        self.radius = radius


class ReflectorConfig:
    def __init__(self, color="gold", radius=30):
        if radius < 30 or radius > 1000:
            raise ValueError("Radius must be between 30 and 1000")
        if color not in ["gold", "silver", "white", "black"]:
            raise ValueError("Color must be gold, silver, white or black")
        self.color = color
        self.radius = radius


class ParabolicConfig:
    def __init__(self, radius=30):
        if radius < 30 or radius > 120:
            raise ValueError("Radius must be between 30 and 120")
        self.radius = radius


class BeautyDishConfig:
    def __init__(self, radius=10):
        if radius < 10 or radius > 30:
            raise ValueError("Radius must be between 10 and 30")
        self.radius = radius


class SnootConfig:
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

    @classmethod
    def from_config(cls, config):
        if config["variant"] == "SOFTBOX":
            variant = ModifierVariant.SOFTBOX
            modifier_config = SoftBoxConfig(
                config["config"]["height"],
                config["config"]["width"],
            )
        elif config["variant"] == "UMBRELLA":
            variant = ModifierVariant.UMBRELLA
            modifier_config = UmbrellaConfig(
                config["config"]["radius"],
            )
        elif config["variant"] == "REFLECTOR":
            variant = ModifierVariant.REFLECTOR
            modifier_config = ReflectorConfig(
                config["config"]["color"],
                config["config"]["radius"],
            )
        elif config["variant"] == "PARABOLIC":
            variant = ModifierVariant.PARABOLIC
            modifier_config = ParabolicConfig(
                config["config"]["radius"],
            )
        elif config["variant"] == "BEAUTYDISH":
            variant = ModifierVariant.BEAUTYDISH
            modifier_config = BeautyDishConfig(
                config["config"]["radius"],
            )
        elif config["variant"] == "SNOOT":
            variant = ModifierVariant.SNOOT
            modifier_config = SnootConfig(
                config["config"]["aperture"],
            )
        else:
            raise ValueError("Invalid modifier variant")
        return cls(variant, modifier_config)


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


class Filter:
    def __init__(
        self,
        variant: FilterVariant,
        config: Union[GelConfig, NDConfig, GridConfig, DiffuserConfig],
    ):
        self.variant = variant
        self.config = config

    @classmethod
    def from_config(cls, config):
        if config["variant"] == "GEL":
            variant = FilterVariant.GEL
            filter_config = GelConfig(
                config["config"]["color"],
            )
        elif config["variant"] == "ND":
            variant = FilterVariant.ND
            filter_config = NDConfig(
                config["config"]["stops"],
            )
        elif config["variant"] == "GRID":
            variant = FilterVariant.GRID
            filter_config = GridConfig(
                config["config"]["type"],
            )
        elif config["variant"] == "DIFFUSER":
            variant = FilterVariant.DIFFUSER
            filter_config = DiffuserConfig(
                config["config"]["type"],
            )
        else:
            raise ValueError("Invalid filter variant")
        return cls(variant, filter_config)


class PhotoEnvironment:
    def __init__(self):
        self.camera = Camera()
        self.subject = Subject()
        self.lights = []

    @classmethod
    def from_config(cls, config):
        env = cls()
        env.camera = Camera.from_config(config["camera"])
        env.subject = Subject.from_config(config["subject"])
        for light_config in config["lights"]:
            env.lights.append(Light.from_config(light_config))
        return env

    def add_light(self, light):
        self.lights.append(light)

    def get_english_description(self):
        description = "The camera is at position ("
        description += f"{self.camera.position.x}, {self.camera.position.y}, {self.camera.position.z}) "
        description += (
            f"with ISO {self.camera.iso.value}, aperture {self.camera.aperture.value} "
        )
        description += f"and shutter speed {self.camera.shutter_speed.value}. "
        description += f"The subject is at position ("
        description += f"{self.subject.position.x}, {self.subject.position.y}, {self.subject.position.z}). "

        if len(self.lights) == 0:
            description += "There are no lights in the environment."
        else:
            description += f"There {'is' if len(self.lights) == 1 else 'are'} {len(self.lights)} light{'s' if len(self.lights) > 1 else ''} in the environment. "
            for i, light in enumerate(self.lights, start=1):
                description += f"Light {i} is a {light.variant.name.replace('_', ' ').title()} light at position "
                description += f"({light.position.x}, {light.position.y}, {light.position.z}) with angle {light.angle.value} degrees. "
                description += f"The light has power {light.config.power}, intensity {light.config.intensity}, and speed {light.config.speed}. "

                if light.modifier:
                    description += f"It has a {light.modifier.variant.name.replace('_', ' ').title()} modifier "
                    if light.modifier.variant == ModifierVariant.SOFTBOX:
                        description += f"with height {light.modifier.config.height} and width {light.modifier.config.width}. "
                    elif light.modifier.variant == ModifierVariant.UMBRELLA:
                        description += (
                            f"with a radius of {light.modifier.config.radius}. "
                        )
                    elif light.modifier.variant == ModifierVariant.REFLECTOR:
                        description += f"with color {light.modifier.config.color} and a radius of {light.modifier.config.radius}. "
                    elif light.modifier.variant == ModifierVariant.PARABOLIC:
                        description += (
                            f"with a radius of {light.modifier.config.radius}. "
                        )
                    elif light.modifier.variant == ModifierVariant.BEAUTYDISH:
                        description += (
                            f"with a radius of {light.modifier.config.radius}. "
                        )
                    elif light.modifier.variant == ModifierVariant.SNOOT:
                        description += (
                            f"with an aperture of {light.modifier.config.aperture}. "
                        )

                if light.filters:
                    description += "It has the following filters: "
                    for filter_config in light.filters:
                        if filter_config.variant == FilterVariant.GEL:
                            description += (
                                f"Gel filter of color {filter_config.config.color}. "
                            )
                        elif filter_config.variant == FilterVariant.ND:
                            description += (
                                f"ND filter with {filter_config.config.stops} stops. "
                            )
                        elif filter_config.variant == FilterVariant.GRID:
                            description += (
                                f"Grid filter of type {filter_config.config.type}. "
                            )
                        elif filter_config.variant == FilterVariant.DIFFUSER:
                            description += (
                                f"Diffuser filter of type {filter_config.config.type}. "
                            )

        return description
