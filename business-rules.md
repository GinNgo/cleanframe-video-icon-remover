# Business Rules

- `BR-01`: Processing is blocked until the user confirms ownership or explicit permission to edit.
- `BR-02`: The tool must not be used to conceal provenance, evade Content ID, or remove a third-party owner watermark.
- `BR-03`: The rectangle must be at least 8 x 8 pixels, remain inside the frame, and use even coordinates for H.264 compatibility.
- `BR-04`: Input is limited to 2 GiB and supported video container extensions.
- `BR-05`: Output keeps source width, height, frame rate, approximate video bitrate, duration, and audio track when compatible.
- `BR-06`: Each accepted processing request records a SHA-256 checksum and processing parameters; media contents are not copied into the audit log.
- `BR-07`: Temporary source files are removed after processing; generated files are removed after download completes.

