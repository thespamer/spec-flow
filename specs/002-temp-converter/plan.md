# Plan: Temperature Converter (002-temp-converter)

- **Status:** approved
- **Spec:** ./spec.md

## Approach
A simple module containing two utility functions for temperature conversion, with validation logic inline using Python's standard `ValueError`.

## Components
| Component | New/changed | Responsibility | Serves REQs |
|-----------|-------------|----------------|-------------|
| `temp_converter/converter.py` | new | Provides `c_to_f` and `f_to_c` with input validation. | REQ-002, REQ-003, REQ-004, REQ-005 |

## Data flow
The consumer calls the converter functions with float or integer temperature values. The system either returns the converted float value or raises a `ValueError` for out-of-bounds inputs.

```
Consumer -> c_to_f(celsius) -> returns float or raises ValueError
Consumer -> f_to_c(fahrenheit) -> returns float or raises ValueError
```

## Contracts / interfaces
```python
def c_to_f(celsius: float) -> float:
    """Converts Celsius to Fahrenheit. Raises ValueError if celsius < -273.15."""
    ...

def f_to_c(fahrenheit: float) -> float:
    """Converts Fahrenheit to Celsius. Raises ValueError if fahrenheit < -459.67."""
    ...
```

## Decisions (ADR-style)
### D1 — Python Functions instead of Class
- **Alternatives:** Creating a `Temperature` class that holds state.
- **Chosen because:** Pure utility functions are simpler and align best with the requirement for simple conversions without state management.

### D2 — Exception Type for Invalid Values
- **Alternatives:** Raising a custom exception class (e.g. `AbsoluteZeroError`).
- **Chosen because:** `ValueError` is standard in Python for values outside acceptable domain limits, keeping the API simple and standard.

## Risks & rollback
- **Precision errors:** Float math in Python can have minor precision drift.
  - *Mitigation:* Use standard float comparisons with tolerance in assertions, or round result if necessary. We will use `pytest.approx` in tests.

## Test strategy
- **Unit tests:** Create `tests/test_temp_converter.py` covering:
  - Exact conversions (0°C, 100°C, 32°F, 212°F).
  - Validation checks for temperatures exactly at absolute zero, slightly above, and below.
- **Traceability:** Tag tests with `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005` in docstrings/comments.

## Requirement coverage
| REQ | Covered by component(s) |
|-----|-------------------------|
| REQ-002 | `temp_converter/converter.py` |
| REQ-003 | `temp_converter/converter.py` |
| REQ-004 | `temp_converter/converter.py` |
| REQ-005 | `temp_converter/converter.py` |
