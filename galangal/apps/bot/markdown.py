from abc import ABC
from dataclasses import dataclass
from typing import List, Union

import bot.constants


class MarkdownComponentCustom(ABC):
    pass


MarkdownComponent = Union[str, MarkdownComponentCustom]


@dataclass
class MarkdownTextComponent(MarkdownComponentCustom):
    text: str


@dataclass
class MarkdownImportantTextComponent(MarkdownComponentCustom):
    text: str


@dataclass
class Action:
    action_type: bot.constants.ActionType
    params: dict


@dataclass
class MarkdownActionComponent(MarkdownComponentCustom):
    text: str
    action: Action


@dataclass
class MarkdownChoiceComponent(MarkdownComponentCustom):
    text: str


@dataclass
class MarkdownDocument:
    components: List[MarkdownComponent]
