from pydantic import Field

from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.config.config import settings

hair = settings.assets.hair


class HairColor(DatapointRequestAsset):
    melanin: float = Field(
        title="Melanin",
        description="The higher the value, the darker the hair strands are",
        default=hair.melanin.default,
        ge=hair.melanin.min,
        le=hair.melanin.max,
    )
    redness: float = Field(
        title="Pheomelanin",
        description="The higher the value, the redder the hair strands are",
        default=hair.redness.default,
        ge=hair.redness.min,
        le=hair.redness.max,
    )
    whiteness: float = Field(
        title="Whiteness",
        description="Random variation of white strands",
        default=hair.whiteness.default,
        ge=hair.whiteness.min,
        le=hair.whiteness.max,
    )
    roughness: float = Field(
        title="Roughness",
        description="The higher the value, the more matte and less reflective the hair strands are",
        default=hair.roughness.default,
        ge=hair.roughness.min,
        le=hair.roughness.max,
    )
    index_of_refraction: float = Field(
        title="Hair index of refraction",
        description="The higher the value, the more reflective are the hair strands",
        default=hair.index_of_refraction.default,
        ge=hair.index_of_refraction.min,
        le=hair.index_of_refraction.max,
    )


class Hair(DatapointRequestAsset):
    """
    Melanin – The pigmentation component that gives the hair strand its main color.
        The higher the value assigned, the higher the concentration of melanin and the darker the hair strands are.
    Pheomelanin – The redness of the hair strand as fraction to all eumelanin.
        1.0 makes the hair redder. The ratio of melanin to pheomelanin determines how red the hair is.
        The Pheomelanin value will have no effect if the Melanin is set to 0.
    Whiteness - Percentage of random white hair strands.
    Roughness - Roughness of the hair strands. Lower values provide reflective hair, while high values yield matte look.
    Index of refraction - Defines how much light rays change direction after hitting the object.
        At 1.0 rays pass straight through like in a transparent material; higher values give more refraction.
    """

    id: str = Field(title="Hair ID", description="Alphanumeric ID of the hair")
    color_settings: HairColor = Field(default_factory=HairColor)
