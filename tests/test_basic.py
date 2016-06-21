import nose
import nose.tools

class TestModule(object):
    """Nose test class."""

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def setup_class(cls):
        """Sets up the test."""

    @classmethod
    def teardown_class(cls):
        """Tears down the test."""
        pass

    def test_main(self):
        """Test call to main."""
        nose.tools.eq_(main(), None)
