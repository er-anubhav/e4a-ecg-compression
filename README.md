# E4A ECG Compression

Lossless ECG compression for ADS1292R-based medical telemetry on nRF52840/Zephyr.

## Project structure

- `include/` — public compressor API
- `src/` — compressor implementation
- `zephyr/` — Zephyr/nRF52840 application scaffold
- `tests/` — correctness and robustness tests
- `benchmarks/` — compression and resource benchmarks
- `docs/` — architecture and protocol notes

## Initial engineering target

- 2 ECG channels
- 24-bit ADS1292R samples
- 500 Hz sampling
- 2-second logical windows / 1000 samples per channel
- Bit-exact lossless reconstruction
- Approximately 1 KB compressed target per channel, to be validated with real recordings

## Development plan

1. Acquire representative ADS1292R data.
2. Measure delta/delta-of-delta statistics.
3. Freeze the binary format.
4. Implement and benchmark the compressor.
5. Add bit-exact tests and corruption handling.
6. Integrate with Zephyr/nRF52840 and Thread/CoAP.

Compression ratio is not assumed until benchmarked against real ECG data.
