from telemetry_data import (
    RECORDS_BUFFERED,
    DATA_RATE_BPS,
    PASS_DURATION_SECONDS,
    PASS_CAPACITY_BITS,
    FRAME_SIZE,
)

# Downlink parameters
RECORD_COUNT = RECORDS_BUFFERED
LINK_RATE = DATA_RATE_BPS
PASS_DURATION = PASS_DURATION_SECONDS
PASS_CAPACITY = PASS_CAPACITY_BITS

# Expected lengths per record (L in bits/record)
L_fixed = 3.0000
L_single_huffman = 2.7225
L_two_huffman = 2.6485
L_sfe = 4.0545

# Frame sizes and overheads for realistic deployment
FRAME_SIZE = FRAME_SIZE  # Records per frame
OVERHEAD_FIXED = 0  # No additional overhead
# Header/Flag bits per frame
HEADER_FIXED = 0  # No header
HEADER_SINGLE = 0  # Single code agreed in advance
HEADER_TWO = 1  # 1-bit mode flag per frame
HEADER_SFE = 0  # Agreed table in advance

designs = {
    "Fixed-Length (3-bit)": (L_fixed, HEADER_FIXED),
    "Single Huffman (p_m)": (L_single_huffman, HEADER_SINGLE),
    "Two-Code Huffman (p_s, p_e + 1-bit flag)": (L_two_huffman, HEADER_TWO),
    "Shannon-Fano-Elias (SFE)": (L_sfe, HEADER_SFE),
}

print(f"{'Design Scheme':<40} | {'L (bits/rec)':<12} | {'Total Bits':<12} | {'Capacity Used':<14} | {'Feasible?'}")
print("-" * 100)

for name, (L, header_bits) in designs.items():
    # Number of frames required
    num_frames = RECORD_COUNT / FRAME_SIZE
    
    # Total payload bits + total header/flag overhead
    total_payload = RECORD_COUNT * L
    total_overhead = num_frames * header_bits
    total_bits = total_payload + total_overhead
    
    cap_used = (total_bits / PASS_CAPACITY) * 100
    feasible = "YES" if total_bits <= PASS_CAPACITY else "NO (Overflow)"
    
    print(f"{name:<40} | {L:<12.4f} | {total_bits:<12,.0f} | {cap_used:<13.2f}% | {feasible}")