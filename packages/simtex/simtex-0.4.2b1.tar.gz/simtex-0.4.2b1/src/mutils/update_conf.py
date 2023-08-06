from difflib import SequenceMatcher as SeqMatch
from typing import Any

from src.configs.config import Config
from src.mutils.prompts import prompt
from src.utils.logger import Logger


def update_conf(
        log: Logger, config: Config, args: Any, assume_yes: bool
    ) -> None:
    """Update the overrides of the program.

    Args:
        log -- for logging.
        config -- configuration of the document metadata, which includes,
            formatting, packages to use among others, refer to simtex.json.
        args -- overrides received from arguments.
        assume_yes -- whether to assume yes or not.
    """

    if args.compiler is not None and args.compiler not in (
            compilers := ["xetex", "pdflatex", "luatex"]
        ): # if compiler is not in options
        pos_compilers: list[float] = [
                SeqMatch(
                    args.compiler, option
                ).ratio() for option in compilers
            ]
        compiler: str = compilers[
                pos_compilers.index(max(pos_compilers))
            ]

        if prompt(
                f"\033[1mINPT\033[0m\t Did you mean {compiler}? [y/n] ",
                assume_yes
            ):
            args.compiler = compiler
        else:
            args.compiler = "pdflatex"
            log.logger(
                "e", "Compiler option not recognized, using pdflatex."
            )

    if args.outputfolder is None:
        BASE_OUT_FOLDER: str = "/".join(args.input.split("/")[:-1])
        args.outputfolder = f"{BASE_OUT_FOLDER}/{config.output_folder}"

        if not args.outputfolder.startswith(("./", ".")):
            args.outputfolder = f"./{args.outputfolder}"

    PARAMETERS: dict[str, Any] = {
            "output_folder": args.outputfolder,
            "author": args.author,
            "date": args.date,
            "doc_font": args.font,
            "font_size": args.fontsize,
            "paper_size": args.papersize,
            "margin": args.margin,
            "indent_size": args.indent,
            "doc_font": args.font,
            "compiler": args.compiler,
            "encode": args.encoding,
            "replace": args.replace
        }

    key_: str; param: Any
    for key_, param in PARAMETERS.items(): # for overrides
        if param is not None and config.__getattribute__(key_) != param:
            log.logger(
                "I",
                (
                    f"Overriding default {key_}: "
                    f"{config.__getattribute__(key_)}"
                    f" -> {param} ..."
                )
            )
            config.__setattr__(key_, param)
