from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Optional, Callable

LANGUAGES = {}


class LanguageMeta(ABCMeta):
    def __init__(cls, name, bases, classdict):
        super().__init__(name, bases, classdict)
        LANGUAGES[cls.lang] = cls


class LanguageBuilder(metaclass=LanguageMeta):
    lang = "unknown"

    def __init__(self, input_dir: Path):
        self.input_dir = input_dir

    @abstractmethod
    def build(self, output_dir: Path):
        pass


def get_lang(language: str) -> Optional[Callable]:
    return LANGUAGES.get(language)


# fill LANGUAGES dict
from . import python
