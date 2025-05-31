from unittest import TestCase

from panflute import convert_text
from panflute.tools import PandocVersion
import pandoc_glfm

version = PandocVersion().version


class AlertsTest(TestCase):
    @classmethod
    def conversion(cls, markdown, fmt="markdown"):
        doc = convert_text(markdown, standalone=True)
        doc.format = fmt
        pandoc_glfm.main(doc)
        return doc

    def test_blockquote_empty(self):
        doc = self.conversion(
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
        doc = self.conversion(
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
        doc = self.conversion(
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
        doc = self.conversion(
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
        doc = self.conversion(
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

    def test_blockquote_bullet(self):
        doc = self.conversion(
            """
> [!note] My title
> * **a**
> * b
>
> * c
            """,
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="markdown",
        )
        if version < (3, 6, 4):
            self.assertEqual(
                text,
                """
:::: note
::: title
My title
:::

-   **a**
-   b
-   c
::::
                """.strip()
            )
        else:
            self.assertEqual(
                text,
                """
:::: note
::: title
My title
:::

- **a**
- b
- c
::::
                """.strip()
            )
