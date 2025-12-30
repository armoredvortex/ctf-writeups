---
title: "Secure AES"
date: 2025-09-25
layout: writeup
platform: CTF
categories: [crypto, hardware, side-channel, python]
tags: [aes, cpa, power-analysis, numpy]
---

# Secure AES

Writeup for the Secure AES challenge involving Side-Channel Analysis.

## Analysis

We are provided with a set of files: `traces.npy` and `pts.npy`.
* `traces.npy`: Contains power consumption measurements (traces) captured during the encryption process.
* `pts.npy`: Contains the plaintext bytes associated with each trace.

The goal is to recover the 16-byte AES-128 key. Since we have physical power measurements, this is a classic **Correlation Power Analysis (CPA)** scenario.

In AES-128, the first operation in a round (after the initial `AddRoundKey`) is `SubBytes`. This operation is highly non-linear and is the standard target for power analysis. The power consumption of a device often correlates with the Hamming Weight (number of bits set to 1) of the data being processed.

## Attack Strategy

We attack the first round of AES. The intermediate value we target is the output of the S-Box:

$$Intermediate = SBox[Plaintext_{byte} \oplus Key_{byte}]$$

The attack logic is as follows:
1.  **Hypothesis:** For a specific byte of the key (0-15), we guess all possible values (0-255).
2.  **Model:** For every guess, we calculate the hypothetical S-Box output for every trace using the known plaintext. We then calculate the **Hamming Weight** of this output.
3.  **Correlation:** We compare our hypothetical power consumption (the Hamming Weights) against the *actual* power traces using Pearson Correlation.
4.  **Decision:** The key guess that produces the highest correlation peak is likely the correct key byte.

## Solution

I wrote a Python script using `numpy` to perform the CPA attack. The script loads the traces, pre-calculates the S-Box and Hamming Weight table, and iterates through key bytes.

Instead of using a library like `scikit-learn` for correlation (which can be slow in loops), I implemented a vectorized Pearson correlation calculation using `numpy` dot products to speed up the processing of the traces.

```python
import numpy as np
from tqdm import tqdm  # Optional, for progress bar (pip install tqdm)

# --- Configuration ---
TRACE_FILE = "traces/traces.npy"
PT_FILE = "traces/pts.npy"
NUM_KEY_BYTES = 16

# AES S-Box
sbox = np.array(
    [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
    ]
)

# Hamming Weight Lookup Table
hw_table = np.array([bin(x).count("1") for x in range(256)])


def solve():
    print(f"[*] Loading traces from {TRACE_FILE}...")
    traces = np.load(TRACE_FILE)
    pts = np.load(PT_FILE)

    num_traces = traces.shape[0]
    num_points = traces.shape[1]

    print(f"[*] Loaded {num_traces} traces with {num_points} samples each.")
    print("[*] Starting CPA Attack on Round 1 S-Box...")

    key = []

    # Iterate over each byte of the key (0 to 15)
    for byte_index in range(NUM_KEY_BYTES):
        best_cpa_for_byte = 0
        best_guess_for_byte = 0

        # Get the plaintext byte for this position across all traces
        pt_byte = pts[:, byte_index]  # Shape: (num_traces,)
        
        # Normalize traces for correlation (t - t_mean)
        t_mean = np.mean(traces, axis=0)
        t_diff = traces - t_mean
        t_std = np.std(traces, axis=0)

        # Try every possible key byte value (0x00 to 0xFF)
        for k_guess in range(256):
            # Calculate Hypothesis: Hamming Weight of SBox[PT ^ KeyGuess]
            intermediate = sbox[pt_byte ^ k_guess]
            hypothesis = hw_table[intermediate]  # Shape: (num_traces,)

            # Normalize hypothesis
            h_mean = np.mean(hypothesis)
            h_diff = hypothesis - h_mean
            h_std = np.std(hypothesis)
            
            if h_std == 0: continue

            # Calculate Correlation: cov(h, t) / (std(h) * std(t))
            numerator = np.dot(h_diff, t_diff) / num_traces
            denominator = h_std * t_std

            cpa_trace = np.zeros_like(denominator)
            valid = denominator != 0
            cpa_trace[valid] = numerator[valid] / denominator[valid]
            cpa_trace = np.abs(cpa_trace)  

            # Find the max correlation for this guess
            current_max = np.max(cpa_trace)

            if current_max > best_cpa_for_byte:
                best_cpa_for_byte = current_max
                best_guess_for_byte = k_guess

        key.append(best_guess_for_byte)
        print(
            f"    Byte {byte_index:02d}: Found 0x{best_guess_for_byte:02x} (Corr: {best_cpa_for_byte:.4f})"
        )

    print("\n[+] FULL KEY RECOVERED:")
    print("    Hex: " + " ".join([f"{x:02x}" for x in key]))
    print("    C  : { " + ", ".join([f"0x{x:02x}" for x in key]) + " }")


if __name__ == "__main__":
    solve()
```
# Flag
`ctf{a3s_br0k3n!}`