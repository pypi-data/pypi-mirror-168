# pytest-pumpkin-spice

Fall in the Canada and the US comes once a year, and you know what that means: Autumn colours, cooler temperatures and, of course, pumpkin spice.

Here's is a small pytest plugin to give your tests some pumpkin spice ☕.

This project was heavily inspired by [pytest-yuk](https://github.com/okken/pytest-yuk) and [pytest-emoji](https://pypi.org/project/pytest-emoji/), developed by [Brian Okken](https://github.com/okken) and [Raphael Pierzina](https://github.com/hackebrot), respectively.

## Installation

**pytest-pumpkin-spice** is available for Python 3. 🐍

You can install **pytest-pumpkin-spice** via [pip][pip] from [PyPI][PyPI]:

```text
$ pip install pytest-pumpkin-spice
```

This will automatically install **pytest** of version 4.2.1 or higher.

[pip]: https://pypi.python.org/pypi/pip/
[PyPI]: https://pypi.org/project/pytest-emoji/

## Features

This plugin adds a ``--pumpkin-spice`` CLI flag to pytest, which replaces the standard test result outputs with a warm blend of pumpkin-spiced emoji, both for *normal* and *verbose* mode.

- ``🎃 / PASSED 🎃`` for a passing test with a happy smile,
- ``❄️ / FAILED ❄️`` for a failed test with wintery reminder,
- ``🍂 / XFAIL 🍂`` for a xfailed test with some fallen leaves,
- ``🍠 / XPASS 🍠`` for a xpass with a sweet potato (almost pumpkin!),
- ``☕ / SKIPPED ☕`` for a skipped test with a pumpkin spiced hot bevarage, and
- ``🥧 / ERROR 🥧`` for an error with a nice big pumpkin pie.

Normal mode with just a sprinkle of pumpkin spice blend:

```text
$ pytest --pumpkin-spice
```

```text
tests/test_emoji.py 🎃❄️🍂🍠☕🥧
```

Verbose mode with some extra warmth and spice:

```text
$ pytest --verbose --pumpkin-spice
```

```text
test_passed PASSED 🎃 ",
test_failed FAILED ❄️ ",
test_xfailed XFAIL 🍂 ",
test_xpassed XPASS 🍠 ",
test_skipped SKIPPED ☕ ",
test_error ERROR 🥧 *",
```

## License

Distributed under the terms of the [MIT][mit] license, **pytest-pumpkin-spice** is
free and open source software

[mit]: http://opensource.org/licenses/MIT
