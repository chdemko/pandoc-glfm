from unittest import TestCase

from panflute import convert_text
from panflute.tools import PandocVersion
import pandoc_glfm

version = PandocVersion().version


class TakssTest(TestCase):
    @classmethod
    def conversion(cls, markdown, fmt="markdown"):
        doc = convert_text(markdown, standalone=True)
        doc.format = fmt
        pandoc_glfm.main(doc)
        return doc

    def test_tasks_simple(self):
        doc = self.conversion(
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
        if version < (3, 6, 4):
            self.assertEqual(
                text,
                """
-   [ ] Task 1
-   [x] Task 2
-   [ ] ~~Task 3~~
                """.strip()
            )
        else:
            self.assertEqual(
                text,
                """
- [ ] Task 1
- [x] Task 2
- [ ] ~~Task 3~~
                """.strip()
            )

    def test_tasks_softbreak(self):
        doc = self.conversion(
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

        if version < (3, 6, 4):
            self.assertEqual(
                text,
                """
-   [ ] Task 1
-   [x] Task 2
-   [ ] ~~Task 3 rest~~
                """.strip()
            )
        else:
            self.assertEqual(
                text,
                """
- [ ] Task 1
- [x] Task 2
- [ ] ~~Task 3 rest~~
                """.strip()
        )

    def test_tasks_linebreak(self):
        doc = self.conversion(
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

        if version < (3, 6, 4):
            self.assertEqual(
                text,
                """
-   [ ] Task 1

-   [x] Task 2

-   [ ] ~~Task 3~~

    ~~rest~~
                """.strip()
            )
        else:
            self.assertEqual(
                text,
                """
- [ ] Task 1

- [x] Task 2

- [ ] ~~Task 3~~

  ~~rest~~
                """.strip()
        )

    def test_tasks_strikeout(self):
        doc = self.conversion(
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

        if PandocVersion().version < (3, 6, 4):
            self.assertEqual(
                text,
                """
-   [ ] Task 1
-   [x] Task 2
-   [ ] ~~Task 3~~
                """.strip()
            )
        else:
            self.assertEqual(
                text,
                """
- [ ] Task 1
- [x] Task 2
- [ ] ~~Task 3~~
                """.strip()
            )
