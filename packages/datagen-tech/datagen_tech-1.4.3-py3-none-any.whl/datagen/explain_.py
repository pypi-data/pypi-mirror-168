import abc
from typing import TypeVar

from IPython.core.display import HTML
from pydantic.main import ModelMetaclass


class Explanation(abc.ABC):
    ...


Exp = TypeVar("Exp", bound=Explanation)


class HTMLExplanation(HTML, Explanation):
    ...


class ExplainableMeta(abc.ABCMeta):
    @abc.abstractmethod
    def get_explanation(cls) -> Explanation:
        ...


class ExplainableModelMeta(ModelMetaclass, ExplainableMeta, abc.ABC):
    ...


class Explainable(abc.ABC):
    @abc.abstractmethod
    def get_explanation(self) -> Explanation:
        ...
