import enum

from bs4 import BeautifulSoup

from datagen.explain_ import ExplainableMeta, Explanation


class DescriptiveEnumMeta(enum.EnumMeta, ExplainableMeta):
    def get_explanation(cls) -> Explanation:
        return cls

    def __repr__(cls):
        space = " " * 3
        delimiter = ",\n" + space
        sorted_members = sorted(cls._member_names_)
        return f"<{cls.__name__}(\n{space}{delimiter.join(sorted_members)}\n)>"

    @property
    def soup(cls) -> BeautifulSoup:
        return BeautifulSoup(
            "<ul>" + "".join([f"<li>{m}</li>" for m in sorted(cls._member_names_)]) + "</ul>"
        )


class DescriptiveEnum(enum.Enum, metaclass=DescriptiveEnumMeta):
    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
