from elvia import error


class TestElviaException(object):
    def test_formatting(self):
        err = error.UnexpectedError(
            "Something happened", 500, {}, "error, man"
        )
        assert str(err) == "Something happened 500 error, man"
