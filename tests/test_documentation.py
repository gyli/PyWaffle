#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Checks that the documentation still describes the code.

The suite covers the library; nothing covered what the docs tell people to type. These tests run
every Python snippet embedded in the docs and the README, and check the class docstring still lists
the real parameters with their real defaults.
"""

import pathlib
import re
import unittest
import warnings

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pywaffle.waffle import Waffle

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PYTHON_FENCE = re.compile(r"```(?:python|py)\n(.*?)```", re.DOTALL)

# Only the first documentation page shows the imports; later pages assume a reader has them
PREAMBLE = "import matplotlib.pyplot as plt\nfrom pywaffle import Waffle\n"

# Some snippets demonstrate pandas input. pandas is not a dependency of pywaffle, so a snippet
# needing it is skipped rather than failed when it is absent.
try:
    import pandas  # noqa: F401

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def documentation_pages():
    """Every page that carries runnable snippets, docs first then the README.

    Both levels of docs/: the topic pages under docs/examples/, and the pages beside them such as
    the quickstart, whose snippets are the first code most readers ever run.
    """
    docs = REPO_ROOT / "docs"
    return sorted(docs.glob("*.md")) + sorted((docs / "examples").glob("*.md")) + [REPO_ROOT / "README.md"]


class TestDocumentationSnippets(unittest.TestCase):
    """Every Python snippet in the documentation still runs."""

    @staticmethod
    def tearDown():
        """Close the figures a snippet leaves behind."""
        plt.close("all")

    def test_every_snippet_runs(self):
        """A renamed parameter or a stricter validation rule must not break the docs silently."""
        for page in documentation_pages():
            snippets = PYTHON_FENCE.findall(page.read_text())
            # Snippets on a page build on each other, so a later one can depend on a variable an
            # earlier one defined. Skipping just the snippet that needs pandas would leave the
            # next one undefined, so the whole page is skipped.
            if not HAS_PANDAS and any("pandas" in code for code in snippets):
                continue

            # They share one namespace, in order
            namespace = {"__name__": "__doc_snippet__"}
            exec(PREAMBLE, namespace)  # noqa: S102 - running the docs is the point
            for number, code in enumerate(snippets, 1):
                with self.subTest(page=page.name, snippet=number):
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            exec(compile(code, f"{page.name}#{number}", "exec"), namespace)  # noqa: S102
                    finally:
                        plt.close("all")

    def test_the_docs_actually_contain_snippets(self):
        """Guard against the extraction silently matching nothing and the test passing vacuously."""
        found = sum(len(PYTHON_FENCE.findall(p.read_text())) for p in documentation_pages())
        self.assertGreater(found, 30, "expected the documentation to carry many runnable snippets")

    def test_shell_commands_are_not_fenced_as_python(self):
        """A shell command in a python fence is syntax-highlighted as Python and cannot run."""
        offenders = []
        for page in documentation_pages():
            for number, code in enumerate(PYTHON_FENCE.findall(page.read_text()), 1):
                first = code.strip().splitlines()[0] if code.strip() else ""
                if first.startswith(("pip ", "$ ", "!pip", "conda ")):
                    offenders.append(f"{page.name}#{number}: {first}")
        self.assertEqual(offenders, [])


class TestDocstringMatchesTheCode(unittest.TestCase):
    """The class docstring is the API reference, so it has to track the parameters."""

    DOCUMENTED = set(re.findall(r":param (\w+):", Waffle.__doc__))

    def test_every_parameter_is_documented(self):
        """A new parameter that never reaches the docstring is undiscoverable."""
        self.assertEqual(sorted(set(Waffle._default_parameters) - self.DOCUMENTED), [])

    def test_no_documented_parameter_has_been_removed(self):
        """A docstring entry with no parameter behind it sends people down a dead end."""
        self.assertEqual(sorted(self.DOCUMENTED - set(Waffle._default_parameters)), [])

    def test_stated_defaults_match_the_real_ones(self):
        """[Default x] in the docstring is the most quietly wrong thing a docstring can say."""
        literals = {"None": None, "False": False, "True": True}
        for block in re.split(r"\n    :param ", Waffle.__doc__)[1:]:
            name = block.split(":")[0]
            stated = re.search(r"\[Default ([^\],]+)", block)
            if not stated or name not in Waffle._default_parameters:
                continue
            text = stated.group(1).strip()
            actual = Waffle._default_parameters[name]
            with self.subTest(parameter=name):
                if text in literals:
                    self.assertIs(actual, literals[text])
                elif isinstance(actual, str):
                    self.assertEqual(text.strip("'\""), actual)
                elif isinstance(actual, (int, float)) and not isinstance(actual, bool):
                    self.assertEqual(float(text), float(actual))


if __name__ == "__main__":
    unittest.main()
