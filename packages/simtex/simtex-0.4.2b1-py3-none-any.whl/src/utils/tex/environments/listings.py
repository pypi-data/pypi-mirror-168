from typing import TextIO


def listings(
        rule: str,
        line: str,
        start: int,
        source: list[str],
        out_file: TextIO
    ) -> int:
    """For formatting of code blocks.

    Args:
        rule -- rule that needs to be followed in translation.
        line -- line that will be analyzed and translated.
        start -- where the parser/translator would start.
        source -- where the other lines of equation would be found.
        out_file -- where the translated line will be written.
    """

    language: str = line.removeprefix("```").replace("\n", "").title()
    if language:
        out_file.write(
            "\n\\begin{lstlisting}"
            f"[language={language}]\n"
        )
    else:
        out_file.write(
            "\n\\begin{lstlisting}\n"
        )

    code: str; cur: int
    for cur, code in enumerate(source[start+1:]):
        if code.strip() == rule:
            out_file.write("\end{lstlisting}\n")
            break

        out_file.write(code)

    return cur+start+1
