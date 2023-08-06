import string
import unicodedata
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Vietnamese:
    ambiguous_chars = {
        "a": "aáảãàạâấẩẫầậăắẳẵằặ",
        "d": "dđ",
        "e": "eéẻẽèẹêếểễềệ",
        "i": "iíỉĩìị",
        "o": "oóỏõòôọôốổỗồộơớởỡờợ",
        "u": "uúủũùụưứửữừự",
        "y": "yýỷỹỳỵ",
    }
    for k, v in ambiguous_chars.items():
        ambiguous_chars[k] = unicodedata.normalize("NFC", v)
    lowers = "".join(ambiguous_chars.values()) + string.ascii_lowercase
    uppers = lowers.upper()
    lowers = set(lowers)
    uppers = set(uppers)
    chars = lowers.union(uppers)
    puncs = ",.!?_()[]-'\": \t\n"
    puncs = unicodedata.normalize("NFC", puncs)
    puncs = set(puncs)

    @staticmethod
    def is_foreign(string):
        string = string.strip()
        if string == "":
            print("empty string!!!")
            return False

        string = unicodedata.normalize("NFC", string)
        char_set = set(string)
        intersection = char_set.intersection(Vietnamese.chars | Vietnamese.puncs)
        return len(intersection) < len(char_set)
