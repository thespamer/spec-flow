# Spec: Temperature Converter

- **Feature ID:** 002-temp-converter
- **Status:** approved
- **Author:** Antigravity
- **Date:** 2026-06-15

## Summary
A Python library/utility that provides functions to convert temperatures between Celsius and Fahrenheit, including input validation to prevent physically impossible temperatures (below absolute zero).

## Actors
- Developer/Consumer importing the module
- End user executing converter functions

## Requirements (EARS)
| ID | Type | Requirement | Acceptance criteria |
|----|------|-------------|---------------------|
| REQ-002 | event-driven | When a consumer requests to convert Celsius to Fahrenheit, the system shall return `(celsius * 1.8) + 32`. | Calling `c_to_f(0)` returns `32.0`, and `c_to_f(100)` returns `212.0`. |
| REQ-003 | event-driven | When a consumer requests to convert Fahrenheit to Celsius, the system shall return `(fahrenheit - 32) / 1.8`. | Calling `f_to_c(32)` returns `0.0`, and `f_to_c(212)` returns `100.0`. |
| REQ-004 | unwanted | If the Celsius value is below absolute zero (-273.15°C), then the system shall raise a ValueError. | Calling `c_to_f(-274)` raises ValueError. |
| REQ-005 | unwanted | If the Fahrenheit value is below absolute zero (-459.67°F), then the system shall raise a ValueError. | Calling `f_to_c(-460)` raises ValueError. |

## Non-goals
- Conversions to/from Kelvin or Rankine.
- GUI or CLI interface for temperature conversion.

## Open questions
- None.

## Changelog
> Appended by `/specify --amend` whenever an approved requirement changes (Article IX).

| Date | Change | Why | Trigger |
|------|--------|-----|---------|
| 2026-06-15 | initial spec | — | specify |
