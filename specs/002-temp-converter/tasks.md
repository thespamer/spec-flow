# Tasks: Temperature Converter (002-temp-converter)

- **Status:** approved
- **Plan:** ./plan.md

> Status legend: todo · doing · done · blocked · stale

| ID | Task | Serves | Component | depends_on | Tests | Status | Commit |
|----|------|--------|-----------|------------|-------|--------|--------|
| T-001 | Write failing unit tests for Celsius to Fahrenheit conversion, including absolute zero limit validation | REQ-002, REQ-004 | `temp_converter/converter.py` | — | `tests/test_temp_converter.py` | done | 98b5c2f |
| T-002 | Implement `c_to_f` to pass T-001 | REQ-002, REQ-004 | `temp_converter/converter.py` | T-001 | `tests/test_temp_converter.py` | done | 0f2f8a2 |
| T-003 | Write failing unit tests for Fahrenheit to Celsius conversion, including absolute zero limit validation | REQ-003, REQ-005 | `temp_converter/converter.py` | T-002 | `tests/test_temp_converter.py` | done | f297cdd |
| T-004 | Implement `f_to_c` to pass T-003 | REQ-003, REQ-005 | `temp_converter/converter.py` | T-003 | `tests/test_temp_converter.py` | done | f19b434 |
| T-005 | Verify: traceability matrix + full suite green | all | — | T-004 | full suite | done | — |

## Notes / blockers
- None so far.
