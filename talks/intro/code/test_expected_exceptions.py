
import pytest

def divide(x, y):
    return x / y

def test_raises():
    with pytest.raises(ZeroDivisionError):
        divide(3, 0)

def test_exc_args():
    with pytest.raises(Exception) as exc:
        raise Exception(42, 'msg')
    assert exc.value.args == (42, 'msg')
    assert exc.type is Exception
    assert exc.tb