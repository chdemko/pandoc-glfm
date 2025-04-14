from unittest import TestCase

from panflute import convert_text, Para, Image, Figure

import pandoc_glfm


class AlertsTest(TestCase):
    @classmethod
    def conversion(cls, markdown, fmt="markdown"):
        doc = convert_text(markdown, standalone=True)
        doc.format = fmt
        pandoc_glfm.main(doc)
        return doc

    def test_blockquote_empty(self):
        doc = AlertsTest.conversion(
            """
> [!note]
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
:::: note
::: title
Note
:::
::::
            """.strip()
        )

    def test_blockquote_rest(self):
        doc = AlertsTest.conversion(
            """
> [!note]
> **rest**
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
:::: note
::: title
Note
:::

**rest**
::::
            """.strip()
        )

    def test_blockquote_newline(self):
        doc = AlertsTest.conversion(
            """
> [!note]
>
> **rest**
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
:::: note
::: title
Note
:::

**rest**
::::
            """.strip()
        )


    def test_blockquote_empty_title(self):
        doc = AlertsTest.conversion(
            """
> [!note] My title
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
:::: note
::: title
My title
:::
::::
            """.strip()
        )

    def test_blockquote_rest_title(self):
        doc = AlertsTest.conversion(
            """
> [!note] My title
> **rest**
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
:::: note
::: title
My title
:::

**rest**
::::
            """.strip()
        )

    def test_blockquote_newline_title(self):
        doc = AlertsTest.conversion(
            """
> [!note] My title
>
> **rest**
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
:::: note
::: title
My title
:::

**rest**
::::
            """.strip()
        )


class TakssTest(TestCase):
    @classmethod
    def conversion(cls, markdown, fmt="markdown"):
        doc = convert_text(markdown, standalone=True)
        doc.format = fmt
        pandoc_glfm.main(doc)
        return doc

    def test_tasks_simple(self):
        doc = AlertsTest.conversion(
            """
* [ ] Task 1
* [x] Task 2
* [~] Task 3

            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
-   [ ] Task 1
-   [x] Task 2
-   [ ] ~~Task 3~~
            """.strip()
        )

    def test_tasks_softbreak(self):
        doc = AlertsTest.conversion(
            """
* [ ] Task 1
* [x] Task 2
* [~] Task 3
  rest
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
-   [ ] Task 1
-   [x] Task 2
-   [ ] ~~Task 3 rest~~
            """.strip()
        )

    def test_tasks_linebreak(self):
        doc = AlertsTest.conversion(
            """
* [ ] Task 1
* [x] Task 2
* [~] Task 3

  rest
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
-   [ ] Task 1

-   [x] Task 2

-   [ ] ~~Task 3~~

    ~~rest~~
            """.strip()
        )

    def test_tasks_strikeout(self):
        doc = AlertsTest.conversion(
            """
* [ ] Task 1
* [x] Task 2
* [~] ~~Task 3~~
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        self.assertEqual(
            text,
            """
-   [ ] Task 1
-   [x] Task 2
-   [ ] ~~Task 3~~
            """.strip()
        )
