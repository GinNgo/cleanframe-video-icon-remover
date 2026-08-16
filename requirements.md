# Requirements

## Scope

Build a local web tool that accepts a user-owned video, lets the user mark a static icon region, removes that region, and exports a video without cropping or resizing.

## Actors and use cases

- Editor: imports a video, confirms edit rights, selects the icon rectangle, processes the file, and downloads the result.
- Operator: runs the local service and reviews the audit log when needed.

## Functional requirements

- `FR-01`: Accept MP4, MOV, M4V, or WebM input through drag-and-drop or file selection.
- `FR-02`: Read intrinsic video dimensions and allow rectangle selection on the preview.
- `FR-03`: Require a rights attestation before processing.
- `FR-04`: Validate the selected rectangle against the source dimensions.
- `FR-05`: Remove a static icon with FFmpeg's `delogo` filter while preserving dimensions, frame rate, duration, and audio.
- `FR-06`: Return an MP4 download and record checksum, source metadata, selected region, and timestamp in a local audit log.

## Non-functional requirements

- Run locally; uploaded media is not sent to a third party.
- Use bounded uploads and non-shell subprocess arguments.
- Preserve source audio by stream copy when compatible.
- Provide responsive, keyboard-accessible controls and clear failure messages.
- Do not claim byte-identical output because video pixels must be re-encoded.

## Constraints and assumptions

- FFmpeg and ffprobe must be available on `PATH`.
- The target icon is static in position. Moving objects require tracking and are outside this version.
- The user owns the video or has explicit edit rights; owner watermarks must not be removed to conceal provenance.

## Definition of Ready

- Scope, supported formats, rights gate, output invariants, and FFmpeg dependency are documented.
- No unresolved blocker prevents local implementation.

## Definition of Done

- Code, validation, audit trail, tests, security notes, usage docs, and rollback-by-deletion are present.
- Sample processing confirms dimensions, FPS, duration, and audio are retained.

