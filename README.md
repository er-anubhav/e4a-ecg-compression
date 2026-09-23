# E4A ECG Compression Lab

A small browser-based experiment for testing whether actual ECG data can be losslessly compressed enough for the E4A medical telemetry design.

## What it does

1. Load a real ECG CSV/TXT/TSV file.
2. Parse numeric samples in the browser.
3. Compress using Delta + ZigZag Varint or Delta-of-Delta + ZigZag Varint.
4. Decompress the byte stream.
5. Compare every reconstructed sample against the original.
6. Report sample count, raw 24-bit size, compressed size, reduction, exact reconstruction, and whether the 1,000-byte target was met.
7. Plot original and reconstructed ECG.

The ECG data stays in the browser; the app does not upload it.

## Current experiment target

For 500 Hz ECG:
- 2 seconds = 1,000 samples/lead
- Raw ADS1292R sample = 24 bits = 3 bytes
- Raw window = 3,000 bytes/lead
- Target = <=1,000 bytes/lead
- Required reduction = 66.7%

The target is an experiment, not an assumption. Real ECG data must be measured.

## Run

Open index.html in a browser. No build system is required.

For multi-column files, the prototype currently uses the first numeric value from each line. A dedicated channel selector will be added once the actual ADS1292R dataset format is fixed.

## Important

This is a research prototype, not a medical device codec. Lossless reconstruction must pass before any compression result is considered valid.