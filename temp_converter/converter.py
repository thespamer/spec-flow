from __future__ import annotations

def c_to_f(celsius: float) -> float:
    """REQ-002, REQ-004: Convert Celsius to Fahrenheit."""
    if celsius < -273.15:
        raise ValueError("Temperature below absolute zero (-273.15°C) is physically impossible.")
    return (celsius * 1.8) + 32.0

def f_to_c(fahrenheit: float) -> float:
    """REQ-003, REQ-005: Convert Fahrenheit to Celsius."""
    raise NotImplementedError()
