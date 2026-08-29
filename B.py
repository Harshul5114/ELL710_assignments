 # ============================================================
# Part B -- Pay for the Code Table
# ============================================================

L = 2.6100          # Expected Huffman length (bits/record)
HEADER_BITS = 32    # 8 code lengths x 4 bits
FIXED_LENGTH = 3    # bits/record for 8 symbols


# ------------------------------------------------------------
# B(i) Expected bits per frame
# ------------------------------------------------------------

def fixed_bits_per_frame(N):
    return FIXED_LENGTH * N


def huffman_bits_per_frame(N):
    return HEADER_BITS + L * N


# ------------------------------------------------------------
# B(ii) Smallest frame size where Huffman is cheaper
# ------------------------------------------------------------

N = 1

while huffman_bits_per_frame(N) >= fixed_bits_per_frame(N):
    N += 1

print("B(ii)")
print(f"Smallest N where Huffman is cheaper: {N}")
print(f"Fixed-length: {fixed_bits_per_frame(N):.4f} bits")
print(f"Huffman:      {huffman_bits_per_frame(N):.4f} bits")


# ------------------------------------------------------------
# B(iii) Net saving per record
# ------------------------------------------------------------

def saving_per_record(N):
    return (
        fixed_bits_per_frame(N) - huffman_bits_per_frame(N)
    ) / N


print("\nB(iii)")

for N in [50, 200, 500]:
    saving = saving_per_record(N)

    print(f"N = {N}")
    print(f"  Fixed-length: {fixed_bits_per_frame(N):.4f} bits")
    print(f"  Huffman:      {huffman_bits_per_frame(N):.4f} bits")
    print(f"  Saving:       {saving:.4f} bits/record")


# ------------------------------------------------------------
# B(iv) Maximum possible codeword length
# ------------------------------------------------------------

# For a binary Huffman tree with 8 symbols,
# determine the maximum possible depth of a leaf.

max_codeword_length = 7

print("\nB(iv)")
print(f"Maximum possible Huffman codeword length: "
      f"{max_codeword_length} bits")