from typing import Any, List


def localize(locale: str, translations: List):
    localized = None

    for translation in translations:
        if 'language' in translation and translation['language'] == locale:
            localized = translation

    if not localized:
        localized = sorted(translations, key=sorter)[0]

    return localized


def sorter(translation: Any):
    if 'ordinal' in translation:
        return translation['ordinal']

    return None
