# Acceptance Criteria

- `AC-01`: Given a supported video, when it is selected, then the UI shows a playable preview and its intrinsic dimensions.
- `AC-02`: Given a preview, when the editor drags a rectangle, then the displayed coordinates map to intrinsic video pixels.
- `AC-03`: Given rights are not attested, when processing is requested, then the server returns HTTP 403 and does not invoke FFmpeg.
- `AC-04`: Given an invalid or out-of-frame rectangle, when processing is requested, then the server returns HTTP 422 with a useful error.
- `AC-05`: Given valid input and rights attestation, when processing completes, then output width, height, FPS, duration tolerance (<= 0.1 s), and audio presence match the input.
- `AC-06`: Given successful processing, when the result is returned, then the audit log includes timestamp, checksum, metadata, and rectangle.
- `AC-07`: Given the service is opened on mobile or desktop, then all primary controls remain visible and usable without horizontal page overflow.

