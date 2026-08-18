# Traceability Matrix

| Requirement | Actor/use case | Rule | Permission | Validation | Design/implementation | Test evidence | Status |
|---|---|---|---|---|---|---|---|
| FR-01 | Editor/import | BR-04 | Local user | Extension and size | `app/main.py`, `app/static/app.js` | `tests/test_core.py` | Implemented |
| FR-02 | Editor/select | BR-03 | Local user | Intrinsic bounds | Canvas overlay in `app/static/app.js` | Manual UI check | Implemented |
| FR-03 | Editor/process | BR-01, BR-02 | Rights holder | Boolean attestation | `/api/process` gate | `test_rights_gate` | Implemented |
| FR-04 | Editor/process | BR-03 | Rights holder | Rectangle normalization | `normalize_region` | Region unit tests | Implemented |
| FR-05 | Editor/export | BR-05 | Rights holder | ffprobe comparison | `process_video` | Sample metadata verification | Implemented |
| FR-06 | Operator/audit | BR-06, BR-07 | Local operator | SHA-256 and JSONL | `write_audit_event` | Audit unit test | Implemented |
| FR-07 | Editor/select | BR-03, BR-05 | Rights holder | Shape allowlist | `create_logo_mask`, shape selector | Mask unit tests and sample visual QA | Implemented |
