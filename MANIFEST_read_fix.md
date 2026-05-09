# v7.5 Read-Side Encoding Fix

Generated: 2026-05-09T13:56:22Z

Companion to commit 3b4c211 (write-side encoding fix). Adds explicit
encoding="utf-8" to Path.read_text() calls so the scripts can decode
UTF-8-encoded JSON inputs on Windows (cp1252 default codec).

## SHA-256 Inventory

| File | SHA-256 | Lines patched |
|---|---|---|
| `generate_v7_5_probes.py` | `c5b632d3965b8b7f43e5c71c3dd95bb49824e198dfa800a353b1da49e285ef72` | line 90 (read), lines 130/143/218 (writes for consistency) |
| `run_v7_5_pilot.py` | `da871e530c1fdf163211abe5048d72406f1685f62559be1c203b122ca1302ee4` | line 314 (read) |
| `score_v7_5_tagshuffle.py` | `1eeff580e2a5502c6850fdc00593f474ba5427d02c28cd03d61b58648368c938` | line 244 (read) |
| `v7_5_analyze.py` | `1c9db5e096ed1dfcd8c0c1561e6e359cba6142a266bbdd9f238fe4e460018256` | lines 51, 86 (reads) |
| `verify_v7_5_pilot.py` | `e125cd6777775125c2a2a520f320f0169e215a1df27daf3dd6ef6fc43e1e376a` | line 220 (read) |
