def test_pumpkin_spice_disabled_by_default_verbose(testdir, pumpkin_spice_tests):
    # create a temporary pytest test module
    testdir.makepyfile(pumpkin_spice_tests)

    # run pytest with the following cmd args
    result = testdir.runpytest("-v", "-o", "console_output_style=classic")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_passed PASSED",
            "*::test_failed FAILED",
            "*::test_xfailed XFAIL",
            "*::test_xpassed XPASS",
            "*::test_skipped SKIPPED",
            "*::test_error ERROR",
        ]
    )

    # make sure that that we get a '1' exit code
    # as we have at least one failure
    assert result.ret == 1


def test_pumpkin_spice_enabled_verbose(testdir, pumpkin_spice_tests):
    # create a temporary pytest test module
    testdir.makepyfile(pumpkin_spice_tests)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        "-v", "--pumpkin_spice", "-o", "console_output_style=classic"
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_passed PASSED 🎃 ",
            "*::test_failed FAILED ❄️ ",
            "*::test_xfailed XFAIL 🍂 ",
            "*::test_xpassed XPASS 🍠 ",
            "*::test_skipped SKIPPED ☕ ",
            "*::test_error ERROR 🥧 *",
        ]
    )

    # make sure that that we get a '1' exit code
    # as we have at least one failure
    assert result.ret == 1

def test_pumpkin_spice_disabled_by_default_non_verbose(testdir, pumpkin_spice_tests):
    # create a temporary pytest test module
    testdir.makepyfile(pumpkin_spice_tests)

    # run pytest with the following cmd args
    result = testdir.runpytest("-o", "console_output_style=classic")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["* .FxXsE"])

    # make sure that that we get a '1' exit code
    # as we have at least one failure
    assert result.ret == 1


def test_pumpkin_spice_enabled_non_verbose(testdir, pumpkin_spice_tests):
    # create a temporary pytest test module
    testdir.makepyfile(pumpkin_spice_tests)

    # run pytest with the following cmd args
    result = testdir.runpytest("--pumpkin_spice", "-o", "console_output_style=classic")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["* 🎃 🍠 🥧 ☕ 🍂 ❄️ "])

    # make sure that that we get a '1' exit code
    # as we have at least one failure
    assert result.ret == 1
