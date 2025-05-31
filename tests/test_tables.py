from unittest import TestCase

from panflute import convert_text
import pandoc_glfm


class TableTest(TestCase):
    @classmethod
    def conversion(cls, markdown, fmt="markdown"):
        doc = convert_text(markdown, standalone=True)
        doc.format = fmt
        pandoc_glfm.main(doc)
        return doc

    def test_blockquote_empty(self):
        doc = TableTest.conversion(
            """
| Name | Details |
| ---  | ---     |
| Item1 | This text is on one line |
| Item2 | This item has:<br><br>- Multiple items<br>- That we want listed separately |
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
+-----------------------------------+-----------------------------------+
| Name                              | Details                           |
+===================================+===================================+
| Item1                             | This text is on one line          |
+-----------------------------------+-----------------------------------+
| Item2                             | This item has:                    |
|                                   |                                   |
|                                   | - Multiple items                  |
|                                   | - That we want listed separately  |
+-----------------------------------+-----------------------------------+
              """.strip()
        )

