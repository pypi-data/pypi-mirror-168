from pydantic import BaseModel, Field


class Vector(BaseModel):
    x: float = Field(title="X direction", ge=-5.0, le=5.0)
    y: float = Field(title="Y direction", ge=-5.0, le=5.0)
    z: float = Field(title="Z direction", ge=-5.0, le=5.0)
