#!/usr/bin/env python

"""
Pandoc filter for adding glfm features to pandoc.
"""

from panflute import (
    Div,
    Doc,
    Element,
    Para,
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
        text = elem.content[0].content[0].text.lower()
        if text in ("[!note]", "[!tip]", "[!important]", "[!caution]", "[!warning]"):
            if len(elem.content[0].content) == 1:
                title = Div(Para(Str(text[2:-1].capitalize)), classes=["title"])
                content = [*elem.content[1:]]
            elif elem.content[0].content[1].tag == "SoftBreak":
                title = Div(Para(Str(text[2:-1].capitalize)), classes=["title"])
                content = [Para(*elem.content[0].content[2:]), *elem.content[1:]]
            else:
                alternate = []
                for index in range(2, len(elem.content[0].content)):
                    if elem.content[0].content[index].tag == "SoftBreak":
                        title = Div(Para(*alternate), classes=["title"])
                        content = [
                            Para(*elem.content[0].content[index:]),
                            *elem.content[1:],
                        ]
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
    return run_filters([alert, task], doc=doc)


if __name__ == "__main__":
    main()
