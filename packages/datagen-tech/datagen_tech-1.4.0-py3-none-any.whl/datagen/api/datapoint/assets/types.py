from datagen.descriptive_enum import DescriptiveEnum


class ExpressionName(str, DescriptiveEnum):
    NEUTRAL = "none"
    HAPPINESS = "happiness"
    SADNESS = "sadness"
    SURPRISE = "surprise"
    FEAR = "fear"
    ANGER = "anger"
    DISGUST = "disgust"
    CONTEMPT = "contempt"
    MOUTH_OPEN = "mouth_open"


class LensColor(str, DescriptiveEnum):
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    RED = "red"


class FrameColor(str, DescriptiveEnum):
    BLACK = "black"
    WHITE = "white"
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    GRAY = "gray"
    SILVER = "silver"
    GOLD = "gold"


class MaskColor(str, DescriptiveEnum):
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    RED = "red"


class Color(str, DescriptiveEnum):
    BLACK = "black"
    WHITE = "white"
    LIGHT_BLUE = "light_blue"
    BLUE = "blue"
    RED = "red"
    LIGHT_RED = "light_red"
    PINK = "pink"
    GREEN = "green"
    APPLE_GREEN = "apple_green"
    DARK_GREEN = "dark_green"
    YELLOW = "yellow"
    LIGHT_YELLOW = "light_yellow"
    ORANGE = "orange"
    ORANGE_RED = "orange_red"
    GRAY = "gray"
    WHEAT = "wheat"
    BROWN = "brown"
    SILVER = "silver"
    ROSE_GOLD = "rose_gold"
    ICE_BLUE = "ice_blue"
    PURPLE = "purple"
    GOLD = "gold"
    ROSE_RED = "rose_red"


class MaskPosition(str, DescriptiveEnum):
    ON_NOSE = "on_nose"
    ON_MOUTH = "on_mouth"
    ON_CHIN = "on_chin"


class GlassesPosition(str, DescriptiveEnum):
    ON_NOSE = "on_nose"


class MaskTexture(str, DescriptiveEnum):
    CLOTH = "cloth"
    DIAMOND_PATTERN = "diamond_pattern"
    WOVEN = "woven"


class Projection(str, DescriptiveEnum):
    PERSPECTIVE = "perspective"
    PANORAMIC = "panoramic"
    ORTHOGRAPHIC = "orthographic"


class Wavelength(str, DescriptiveEnum):
    VISIBLE = "visible"
    NIR = "nir"


class LightType(str, DescriptiveEnum):
    NIR = "nir"
