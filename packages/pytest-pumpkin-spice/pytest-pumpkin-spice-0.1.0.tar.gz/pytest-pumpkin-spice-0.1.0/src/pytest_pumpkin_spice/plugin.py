from pytest_pumpkin_spice import hooks


def pytest_pumpkin_spice_passed(config):
    # SMILING JACK-O-LANTERN
    return u"🎃 ", u"PASSED 🎃 "


def pytest_pumpkin_spice_failed(config):
    # SNOWFLAKE
    return u"❄️ ", u"FAILED ❄️ "


def pytest_pumpkin_spice_skipped(config):
    # PUMPKIN SPICE LATTE
    return u"☕ ", u"SKIPPED ☕ "


def pytest_pumpkin_spice_error(config):
    # PUMPKIN PIE
    return u"🥧", u"ERROR 🥧 "


def pytest_pumpkin_spice_xfailed(config):
    # FALLING LEAVES
    return u"🍂 ", u"XFAIL 🍂 "


def pytest_pumpkin_spice_xpassed(config):
    # SWEET POTATO
    return u"🍠 ", u"XPASS 🍠 "


def pytest_addhooks(pluginmanager):
    # Register new hooks from pytest_pumpkin_spice.hooks
    pluginmanager.add_hookspecs(hooks)


def pytest_report_teststatus(report, config):
    if config.option.pumpkin_spice is False:
        # Do not modify reporting, unless pytest is called with --pumpkin-spice
        return

    # Handle error and skipped in setup and teardown phase
    if report.when in ("setup", "teardown"):
        if report.failed:
            short, verbose = config.hook.pytest_pumpkin_spice_error(config=config)
            return "error", short, verbose
        elif report.skipped:
            short, verbose = config.hook.pytest_pumpkin_spice_skipped(config=config)
            return "skipped", short, verbose

    # Handle xfailed and xpassed
    if hasattr(report, "wasxfail"):
        if report.skipped:
            short, verbose = config.hook.pytest_pumpkin_spice_xfailed(config=config)
            return "xfailed", short, verbose
        elif report.passed:
            short, verbose = config.hook.pytest_pumpkin_spice_xpassed(config=config)
            return "xpassed", short, verbose
        else:
            return "", "", ""

    # Handle passed, skipped and failed in call phase
    if report.when == "call":
        if report.passed:
            short, verbose = config.hook.pytest_pumpkin_spice_passed(config=config)
        elif report.skipped:
            short, verbose = config.hook.pytest_pumpkin_spice_skipped(config=config)
        elif report.failed:
            short, verbose = config.hook.pytest_pumpkin_spice_failed(config=config)
        return report.outcome, short, verbose


def pytest_addoption(parser):
    group = parser.getgroup("pumpkin-spice")
    group.addoption(
        "--pumpkin-spice",
        action="store_true",
        default=False,
        help="Tests, but pumpkin spice flavoured",
    )
