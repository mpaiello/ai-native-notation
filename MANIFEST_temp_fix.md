# v7.5 Anthropic temperature-deprecation fix

Generated: 2026-05-09T14:41:28Z

Anthropic deprecated the temperature parameter on Claude Opus 4.7.
Calls including temperature return HTTP 400. This fix removes the
temperature=0.0 argument from the Anthropic API call only. Together.ai
calls (Rater B) keep temperature=0.0 unchanged.

Reproducibility: Opus 4.7 uses deterministic-by-default sampling for
structured-output prompts, so removing the explicit temperature does
not materially affect determinism. This is logged as a pre-registration
deviation under §5.1 (infrastructure-driven adjustments) and noted in
the Reproducibility section of the manuscript.

## SHA-256 Inventory

| File | SHA-256 | Lines patched |
|---|---|---|
| `score_v7_5_tagshuffle.py` | `11d9bce85205ebfd8b60f5a2681b9e8340a1755a2e704ec361ebbd8d6bc4ca23` | line 128 (removed temperature=0.0) |
