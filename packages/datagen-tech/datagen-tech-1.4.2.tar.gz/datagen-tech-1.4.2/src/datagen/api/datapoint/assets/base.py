import abc

import rich
from rich.pretty import Pretty

from datagen.explain_ import HTMLExplanation, ExplainableModelMeta

from dataclasses import dataclass
from pathlib import Path
from typing import Union, Generator, Dict, List

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel
from pydantic.main import partial

soup = partial(BeautifulSoup, features="html.parser")


@dataclass
class PropExtraDetails(abc.ABC):
    @property
    @abc.abstractmethod
    def new_line(self) -> bool:
        ...

    @property
    def inline(self) -> bool:
        return not self.new_line

    @property
    @abc.abstractmethod
    def soup(self) -> BeautifulSoup:
        ...


@dataclass
class EnumPropExtraDetails(PropExtraDetails):
    values: List[str]

    @property
    def new_line(self) -> bool:
        return False

    @property
    def soup(self) -> BeautifulSoup:
        return soup("(Enumeration)<br/>Possible Values: " + ", ".join(v.upper() for v in self.values))


@dataclass
class NumericPropExtraDetails(PropExtraDetails):
    minimum: Union[int, float] = None
    maximum: Union[int, float] = None
    default: Union[int, float] = None

    @property
    def new_line(self) -> bool:
        return True

    def _get_formatted_dict(self) -> Generator:
        for k, v in {"Min val.": self.minimum, "Max val.": self.maximum, "Default": self.default}.items():
            if v is not None:
                yield k, str(v)

    @property
    def soup(self) -> BeautifulSoup:
        return soup(", ".join(" ".join([k, v]) for k, v in self._get_formatted_dict()))


class DatapointRequestAsset(BaseModel, metaclass=ExplainableModelMeta):
    @classmethod
    def get_explanation(cls) -> HTMLExplanation:
        return HTMLExplanation(cls._read_explanation())

    @classmethod
    def _read_explanation(cls) -> str:
        asset_soup = cls._get_soup()
        html_tags, extra_details = cls._get_html_tags(asset_soup), cls._get_extra_details()
        for asset_prop_name, prop_html_tag in html_tags.items():
            cls._replace_ambiguous_types(prop_html_tag)
            prop_extra_details = extra_details.get(asset_prop_name)
            if prop_extra_details:
                cls._add_extra_details(prop_html_tag, prop_extra_details)
        return str(asset_soup)

    @classmethod
    def _get_soup(cls) -> BeautifulSoup:
        asset_explanation_html_path = Path(__file__).parent.joinpath("explanations", f"{cls.__name__}.html")
        return soup(asset_explanation_html_path.read_text())

    @classmethod
    def _replace_ambiguous_types(cls, html_tag: Tag) -> None:
        html_tag.contents[0].replace_with(soup(html_tag.contents[0].text.replace("BigDecimal", "Float")))

    @classmethod
    def _get_html_tags(cls, asset_soup: BeautifulSoup) -> Dict[str, Tag]:
        asset_property_name_to_tag = {}
        for tag in asset_soup.find_all("li"):
            property_name = tag.text.strip().split(" : ")[0]
            asset_property_name_to_tag[property_name] = cls._cleanup_content(tag)
        return asset_property_name_to_tag

    @classmethod
    def _cleanup_content(cls, tag: Tag) -> Tag:
        tag.contents = list(filter(lambda c: c.name == "br" or c.text.strip(), tag.contents))
        return tag

    @classmethod
    def _get_extra_details(cls) -> Dict[str, PropExtraDetails]:
        extra_details = {}
        asset_schema = cls.schema()
        for prop_name, prop_details in asset_schema["properties"].items():
            if prop_details.get("type") in ["number", "integer"]:
                extra_details[prop_name] = NumericPropExtraDetails(
                    prop_details.get("minimum"), prop_details.get("maximum"), prop_details.get("default")
                )
            else:
                enum_values = cls._get_enum_values(prop_name, asset_schema)
                if enum_values:
                    extra_details[prop_name] = EnumPropExtraDetails(enum_values)
        return extra_details

    @classmethod
    def _get_enum_values(cls, prop_name: str, asset_schema: dict) -> Union[list, None]:
        ref = asset_schema["properties"][prop_name].get("$ref")
        if ref:
            definition = ref.split("/")[-1]
            return asset_schema["definitions"][definition].get("enum")

    @classmethod
    def _add_extra_details(cls, html_tag: Tag, extra_details: PropExtraDetails) -> None:
        if extra_details.new_line and html_tag.contents[-1].name != "br":
            html_tag.contents.append(soup("<br/>"))
        elif extra_details.inline and html_tag.contents[-1].name == "br":
            html_tag.contents.pop()
        html_tag.contents.append(extra_details.soup)
