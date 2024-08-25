from langchain.pydantic_v1 import BaseModel, Field


class PositionModel(BaseModel):
    x: int = Field(description="x co-ordinate between 0 and 10")
    y: int = Field(description="y co-ordinate between 0 and 10")
    z: int = Field(description="z co-ordinate between 0 and 10")


class LightModel(BaseModel):
    type: str = Field(description="either STROBE or SPEEDLIGHT")
    position: PositionModel = Field("position of light")
    power: int = Field(
        description="power of light, for strobe between 100 and 1500, for speedlight between 60 and 100"
    )
    intensity: int = Field(
        description="intensity of light, for strobe between 1/64 and 1, for speedlight between 1/128 and 1"
    )

    speed: int = Field(
        description="blinking speed of light, for strobe between 1/10000 and 1/800, for speedlight between 1/30000 and 1/1000 "
    )

    angle: int = Field(description="angle light is tilted to, between 0 and 360")
