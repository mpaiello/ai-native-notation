# v7.5 Encoding Fix Patch

Generated: 2026-05-09T13:24:23Z

Five files patched. Each adds `encoding="utf-8"` to `Path.write_text()`
calls to handle Greek letters (α), arrows (→), and other non-ASCII Unicode
characters in markdown summary outputs on Windows (cp1252 default codec).

## SHA-256 Inventory

| File | SHA-256 | Lines patched |
|---|---|---|
| `generate_v7_5_problems.py` | `ac853d088c5e56a4db554e9971df2d073b53a57db78b930c5dc9205dcaeaf8df` | line 322 |
| `run_v7_5_pilot.py` | `a2bd592cba38b5a43c0861dbfc1af3b8857a2470a04c4a267dfc1531bc10632e` | line 410 |
| `score_v7_5_tagshuffle.py` | `8bf30c747c0d0729d817f8ab9b7b7cf526b41b0f59ff80a1a3d9f6240b96afef` | lines 334, 357 |
| `v7_5_analyze.py` | `e1766dd86cf654ac83c1b4397f798118f2ea2a05fa7ee50587d42d57cf156b97` | lines 183, 200 |
| `verify_v7_5_pilot.py` | `e1d639b28eadcde05fac053bffe11b19e84964eb9f36969a21a894674f301751` | lines 313, 350 |
