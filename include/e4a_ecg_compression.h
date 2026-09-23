/* Public API for the E4A ECG lossless compressor. */
#ifndef E4A_ECG_COMPRESSION_H
#define E4A_ECG_COMPRESSION_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define E4A_ECG_MAX_SAMPLES 1000U

typedef struct {
    uint32_t sample_count;
    uint32_t sample_rate_hz;
    uint8_t channel_id;
} e4a_ecg_block_info_t;

/* Compression/decompression API will be implemented after the format is frozen. */
int e4a_ecg_compress(const int32_t *samples, size_t sample_count,
                     uint8_t *out, size_t out_capacity, size_t *out_size);
int e4a_ecg_decompress(const uint8_t *data, size_t data_size,
                       int32_t *samples, size_t sample_capacity, size_t *sample_count);

#ifdef __cplusplus
}
#endif

#endif
