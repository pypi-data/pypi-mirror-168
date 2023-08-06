from json import dump
from typing import Any, IO


def conf_gen(PATH: str) -> dict[
        str | list[str | list[str]] | str | int | bool | float
    ]:
    """Generate the default config file.

    Args:
        PATH -- where the default config will be placed.
    """

    CONF: dict[
            str | list[str | list[str]] | str | int | bool | float
        ] = {
            "DOC_CLASS": "article",
            "DEF_FONT": "lmodern",
            "FONT_SIZE": 12,
            "MARGIN": 1,
            "PAPER_SIZE": "a4paper",
            "INDENT_SIZE": 24,
            "SLOPPY": True,
            "CODE_FONT": "DejaVuSansMono",
            "CFONT_SCALE": 0.9,
            "CODE_CONF": "<HOME>/.config/simtex/code_conf.txt",
            "PACKAGES": [
                ["geometry", "margin=<MARGIN>, <PAPER_SIZE>"],
                "indentfirst",
                "amsmath",
                "mathtools",
                "sectsty",
                "footmisc",
                "gensymb",
                "xcolor",
                "listings",
                "caption",
                "csquotes",
                ["ulem", "normalem"],
                ["hyperref", "colorlinks, allcolors=<LINK_COLORS>"]
            ],
            "FOOTNOTE": "footnote",
            "SECTION_SIZES": {
                "main": "<DEF>",
                "sub": "<DEF>",
                "subsub": "<DEF>"
            },
            "LINKS": True,
            "LINK_COLOR": "blue",
            "AUTHOR": "John Doe",
            "DATE": "<NOW>",
            "MAKE_TITLE": True,
            "OUTPUT_FOLDER": "out",
            "COMPILER": "pdflatex",
            "ENCODE": "UTF8",
            "REPLACE": False,
            "TWOCOLS": False,
            "ASSUME_YES": False,
            "AUTOCORRECT": False,
            "AUTOCORRECT_LANG": "ENGLISH"
        }

    conf: IO[Any]
    with open(PATH, "w", encoding="utf-8") as conf:

