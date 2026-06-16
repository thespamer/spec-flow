from __future__ import annotations
import pytest
from temp_converter.converter import c_to_f

def test_c_to_f_normal() -> None:
    """REQ-002: Test typical temperature conversions from Celsius to Fahrenheit."""
    assert c_to_f(0.0) == pytest.approx(32.0)
    assert c_to_f(100.0) == pytest.approx(212.0)
    assert c_to_f(37.0) == pytest.approx(98.6)

def test_c_to_f_absolute_zero_boundary() -> None:
    """REQ-002, REQ-004: Test conversion at exactly absolute zero."""
    assert c_to_f(-273.15) == pytest.approx(-459.67)

def test_c_to_f_below_absolute_zero() -> None:
    """REQ-004: Test values below absolute zero raise ValueError."""
    with pytest.raises(ValueError):
        c_to_f(-273.16)
    with pytest.raises(ValueError):
        c_to_f(-1000.0)
