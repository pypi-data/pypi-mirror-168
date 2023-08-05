import textwrap
import pytest

pytest_plugins = "pytester"


@pytest.fixture(name="pumpkin_spice_tests")
def fixture_pumpkin_spice_tests():
    return textwrap.dedent(
        """\
        import pytest

        def test_passed():
            assert "emoji" == "emoji"

        def test_failed():
            assert "emoji" == "hello world"

        @pytest.mark.xfail
        def test_xfailed():
            assert 1234 == 100

        @pytest.mark.xfail
        def test_xpassed():
            assert 1234 == 1234

        @pytest.mark.skipif(True, reason="don't run this test")
        def test_skipped():
            assert "emoji" == "emoji"

        @pytest.fixture
        def name():
            raise RuntimeError

        @pytest.mark.hello
        def test_error(name):
            assert name == "hello"
        """
    )
