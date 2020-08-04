import pytest

from books.utils import verify_date


@pytest.mark.parametrize(
    "value, expected",
    [("2000", "2000-01-01"), ("1990-06", "1990-06-01"), ("1854-10-12", "1854-10-12")],
)
def test_verify_date(value, expected):
    assert verify_date(value) == expected
