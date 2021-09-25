from dataclasses import dataclass


@dataclass
class PhraseContextEntity:
    source_language_phrase: str
    source_language_context: str
    target_language_phrase: str
    target_language_context: str
