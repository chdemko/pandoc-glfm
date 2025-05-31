#!/usr/bin/env python

"""
Pandoc filter for adding glfm features to pandoc.
"""

from panflute import (
    Div,
    Doc,
    Element,
    Para,
    Plain,
    Str,
    Strikeout,
    convert_text,
    run_filters,
)


# pylint: disable=inconsistent-return-statements,unused-argument
def alert(elem: Element, doc: Doc) -> Element | None:
    """
    Transform some blockquote elements to alerts.

    Arguments
    ---------
    elem
        The current element
    doc
        The pandoc document

    Returns
    -------
    Element | None
        The modified element or None
    """
    if (
        elem.tag == "BlockQuote"
        and elem.content
        and elem.content[0].tag == "Para"
        and elem.content[0].content
        and elem.content[0].content[0].tag == "Str"
    ):

        def extract_first_lines(
            first: list[Element],
            rest: list[Element],
        ) -> list[Element]:
            result = []
            for item in first:
                if item.tag == "Str":
                    result.append(item.text)
                elif item.tag == "SoftBreak":
                    result.append("\n")
                elif item.tag == "Space":
                    result.append(" ")
                else:
                    result.append(
                        convert_text(
                            Plain(item),
                            input_format="panflute",
                            output_format="markdown",
                        ),
                    )
            for item in rest:
                result.extend(
                    [
                        "\n",
                        convert_text(
                            item,
                            input_format="panflute",
                            output_format="markdown",
                        ),
                    ]
                )

            return convert_text("".join(result))

        text = elem.content[0].content[0].text.lower()
        if text in ("[!note]", "[!tip]", "[!important]", "[!caution]", "[!warning]"):
            # Case
            #
            # > [!tip]
            #
            # and
            #
            # > [!tip]
            # >
            # > Rest of text
            if len(elem.content[0].content) == 1:
                title = Div(Para(Str(text[2:-1].capitalize())), classes=["title"])
                content = [*elem.content[1:]]
            # Case
            #
            # > [!tip]
            # > Rest of text
            elif elem.content[0].content[1].tag == "SoftBreak":
                title = Div(Para(Str(text[2:-1].capitalize())), classes=["title"])
                content = extract_first_lines(
                    elem.content[0].content[2:],
                    elem.content[1:],
                )
            # Case
            #
            # > [!tip] title
            # > Rest of text
            #
            # and
            #
            # > [!tip] title
            # >
            # > Rest of text
            else:
                alternate = []
                for index in range(2, len(elem.content[0].content)):
                    if elem.content[0].content[index].tag == "SoftBreak":
                        title = Div(Para(*alternate), classes=["title"])
                        content = extract_first_lines(
                            elem.content[0].content[index:],
                            elem.content[1:],
                        )
                        break
                    alternate.append(elem.content[0].content[index])
                else:
                    title = Div(Para(*alternate), classes=["title"])
                    content = [*elem.content[1:]]

            return convert_text(
                convert_text(
                    Div(title, *content, classes=[text[2:-1]]),
                    input_format="panflute",
                    output_format="markdown",
                )
            )
    return None


def task(elem: Element, doc: Doc) -> None:
    """
    Deal with glfm task lists.

    Arguments
    ---------
    elem
        The current element
    doc
        The pandoc document
    """
    if elem.tag in ("BulletList", "OrderedList"):
        for item in elem.content:
            if (
                item.content[0].tag in ("Plain", "Para")
                and item.content[0].content
                and item.content[0].content[0].tag == "Str"
                and item.content[0].content[0].text == "[~]"
                and len(item.content[0].content) >= 3
            ):
                item.content[0].content[0].text = "☐"
                item.content[0].content[2] = Strikeout(
                    *remove_strikeout(item.content[0].content[2:]),
                )
                item.content[0].content[3:] = []
                for block in item.content[1:]:
                    if block.tag in ("Plain", "Para"):
                        block.content[0] = Strikeout(*remove_strikeout(block.content))
                        block.content[1:] = []


def remove_strikeout(elems: list[Element]) -> list[Element]:
    """
    Remove Strikeout from elements.

    Parameters
    ----------
    elems
        Elements from which Strikeout must be removed

    Returns
    -------
    list[Element]
        The elements without the Strikeout.
    """
    result = []
    for elem in elems:
        if elem.tag == "Strikeout":
            result.extend(elem.content)
        else:
            result.append(elem)
    return result


def cell(elem: Element, doc: Doc) -> None:
    """
    Transfom cell elements that contain <br />.

    Parameters
    ----------
    elem
        The current element
    doc
        The pandoc document

    """
    if elem.tag == "TableCell":
        convert = False
        for index, item in enumerate(elem.content[0].content):
            if (
                item.tag == "RawInline"
                and item.format == "html"
                and item.text in ("<br>", "<br/>", "<br />")
            ):
                convert = True
                elem.content[0].content[index] = Str("\n")

        if convert:
            text = convert_text(
                elem.content[0],
                input_format="panflute",
                output_format="markdown",
            )
            elem.content = convert_text(text)


def main(doc: Doc | None = None) -> Doc:
    """
    Convert the pandoc document.

    Arguments
    ---------
    doc
        The pandoc document

    Returns
    -------
    Doc
        The modified pandoc document
    """
    return run_filters([alert, task, cell], doc=doc)


if __name__ == "__main__":
    main()
