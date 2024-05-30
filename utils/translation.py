import os
from pathlib import Path
import gettext
import locale


_podir = os.path.join(
    Path(os.path.dirname(__file__)).parent.absolute(),
    "po"
)


TRANSLATIONS = {
    ("en_US", "UTF-8"): gettext.translation("all",
                                            _podir, fallback=True),
    ("ru_RU", "UTF-8"): gettext.NullTranslations(),
}


def _(text):
    return TRANSLATIONS[locale.getlocale(locale.LC_CTYPE)].gettext(text)
