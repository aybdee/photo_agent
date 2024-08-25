from environment import (
    Angle,
    Light,
    LightVariant,
    PhotoEnvironment,
    Position,
    SpeedLightConfig,
    StrobeConfig,
)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from models import LightModel, PositionModel


def get_photo_state_tool(environment: PhotoEnvironment):

    @tool
    def check_photo_state() -> str:
        """
        Use this tool to monitor and report the current
        state of your photograph setup, including lighting,
        subject positioning, and camera placement,
        to ensure everything is in the right place
        before proceeding with further adjustments.
        """
        return environment.get_english_description()

    return check_photo_state


def get_place_subject_tool(environment: PhotoEnvironment):
    @tool(args_schema=PositionModel)
    def place_subject(position: PositionModel) -> str:
        """
        Use this tool to position your subject in the scene
        """
        environment.place_subject(Position(position.x, position.y, position.z))
        return f"placed subject at ({position.x},{position.y},{position.z})"

    return place_subject


def get_add_light_tool(environment: PhotoEnvironment):
    @tool(args_schema=LightModel)
    def add_light(light: LightModel) -> str:
        """
        Use this tool to add a light to your setup
        """
        if light.type == "STROBE":
            config = StrobeConfig(light.power, light.intensity, light.speed)
            variant = LightVariant.STROBE
        else:
            config = SpeedLightConfig(light.power, light.intensity, light.speed)
            variant = LightVariant.SPEED_LIGHT
        environment.add_light(
            Light(
                variant=variant,
                config=config,
                position=Position(light.position.x, light.position.y, light.position.z),
                angle=Angle(light.angle),
            )
        )

        return f"added light"

    return add_light
