"""Testcases for in bitfount/federated/utils.py."""
import pytest

from bitfount.federated.utils import _keys_exist
from tests.utils.helper import unit_test


@unit_test
def test_keys_exist_works() -> None:
    """Tests that _keys_exists works as expected with correct input."""
    data = {
        "spam": {
            "egg": {
                "bacon": "Is good..",
                "sausages": "Spam egg sausages and spam",
                "spam": "does not have much spam in it",
            }
        }
    }
    assert _keys_exist(data, "spam") is True
    assert _keys_exist(data, "spam", "bacon") is False
    assert _keys_exist(data, "spam", "egg") is True
    assert _keys_exist(data, "spam", "egg", "bacon") is True


@unit_test
def test_keys_exist_error_dict() -> None:
    """Tests that _keys_exists works as expected with wrong dict input."""
    data = "spam"
    with pytest.raises(AttributeError):
        _keys_exist(data, "spam")  # type: ignore[arg-type] # Reason: we test wrong input here. # noqa: B950


@unit_test
def test_keys_exist_missing_keys() -> None:
    """Tests that _keys_exists works as expected with wrong keys input."""
    data = {
        "spam": {
            "egg": {
                "bacon": "Is good..",
                "sausages": "Spam egg sausages and spam",
                "spam": "does not have much spam in it",
            }
        }
    }
    with pytest.raises(AttributeError):
        _keys_exist(data)
