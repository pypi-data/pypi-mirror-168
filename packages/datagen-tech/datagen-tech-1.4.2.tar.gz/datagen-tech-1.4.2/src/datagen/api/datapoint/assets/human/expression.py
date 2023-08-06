from pydantic import Field

from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.api.datapoint.assets.types import ExpressionName
from datagen.config.config import settings

expression = settings.assets.head.expression


class Expression(DatapointRequestAsset):
    name: ExpressionName = Field(default=ExpressionName[expression.default])
    intensity: float = Field(
        title="Expression intensity",
        description="The higher the value, the more intense the expression is. "
        "A 0.0 value is impossible and 'neutral' expression should be used instead.",
        default=expression.intensity.default,
        ge=expression.intensity.min,
        le=expression.intensity.max,
    )
