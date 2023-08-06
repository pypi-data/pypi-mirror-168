from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float = Field(title="X location", ge=-5.0, le=5.0)
    y: float = Field(title="Y location", ge=-5.0, le=5.0)
    z: float = Field(title="Z location", ge=-5.0, le=5.0)
