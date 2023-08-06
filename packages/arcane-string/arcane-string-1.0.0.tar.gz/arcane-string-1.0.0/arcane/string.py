import re
import unicodedata


def strip_accents(text: str) -> str:
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")


def handle_pascal_case_match(match: re.Match) -> str:
    if match.group(1) is not None:
        if len(match.group(1)) == 0:
            return ''
        elif len(match.group(1)) == 1 and re.match(r'\w', match.group(1)):
            return match.group(1).upper()
        else:
            first_letter = ''
            if re.match(r'\w', match.group(1)[0]):
                first_letter = match.group(1)[0].upper()
            return first_letter + match.group(1)[1:].lower()
    else:
        return ''


def to_pascal_case(text: str) -> str:
    if text == '':
        return ''
    text_stripped = strip_accents(text)
    return re.sub(
        r"(?:^|_|\W)+([^_\W]*)",
        handle_pascal_case_match,
        text_stripped
    )


def to_camel_case(text: str) -> str:
    pascal_text = to_pascal_case(text)
    if len(pascal_text) > 1:
        return pascal_text[0].lower() + pascal_text[1:]
    else:
        return pascal_text.lower()


def to_snake_case(text: str) -> str:
    camel_text = to_pascal_case(text)
    return re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", camel_text).lower()
