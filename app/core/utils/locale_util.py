from typing import Any, List


def localize(locale: str, translations: List):
    for translation in translations:
        if "language" in translation and translation["language"] == locale:
            return translation
    else:
        return sorted(translations, key=sorter)[0]


def sorter(translation: Any):
    return translation.get("ordinal", None)
