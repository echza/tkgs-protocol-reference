# Changelog

All notable changes to this reference. Dates are ISO 8601.

## 0.2 — 2026-11-12

### Added
- §2.4 Home transponders on 42.0°E and the TKGS PID `0x1FF5` (8181), with backup
  transponders and failover guidance.
- §2.6 Acquisition timing guidance (TR 101 211 repetition rates, timeouts, when to check).
- §3.4 Sub-tables: completeness is tracked per `(table_id, table_id_extension)`.
- §4.3.1 Text encoding (EN 300 468 Annex A, ISO 8859-9 fallback).
- §4.6 Worked example with synthetic test vectors.
- §5.5 LCN edge cases (range, LCN 0, misses, duplicates).
- §6.5 Where the operating mode comes from.
- §7.2 Firmware update signal location and comparison with DVB SSU (TS 102 006).
- §9 Open questions, with the evidence needed to settle each one.
- `tools/tkgs_decode.py` reference decoder with a self-test.

### Changed
- §7.1 The version rule now compares for inequality and explains why "greater than" is unsafe.
- §5.2 Default LCN `1` on a locator miss is now marked as single-implementation evidence.
- §4.3 Language codes are compared case-insensitively.
- README diagram and §2.5 acquisition steps include the TKGS PID.

### Known issues
- The SDT-descriptor carriage model (§2.2–§2.3) may be incomplete or wrong
  relative to the dedicated TKGS PID. See §9 C1–C4.

## 0.1

- Initial reference.
