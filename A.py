import math
from huffman import HuffmanEncoder
from telemetry_data import sunlit_distribution

# building the Huffman tree and generating codes
encoder = HuffmanEncoder(sunlit_distribution)
codes = encoder.generate_codes()

encoder.printTree()
print("\nHuffman Codes:")

events = sorted(codes.keys())
for event in events:
    print(f"{event}: {codes[event]}")

#length vector
length_vector = [len(codes[event]) for event in events]
print(f"\nLength Vector: L = {length_vector}")    

# expected length L
L = sum(sunlit_distribution[event] * len(codes[event]) for event in events)
print(f"Expected Length: L = {L:.4f} bits")

# entropy H
H = -sum(p * math.log2(p) for p in sunlit_distribution.values())
print(f"\nEntropy: H = {H:.2f} bits")

# efficiency
efficiency = H / L if L > 0 else 0
print(f"Efficiency: η = {efficiency:.4f}")

# Kraft inequality
kraft_sum = sum(2**(-l) for l in length_vector)
print(f"Kraft inequality: Σ 2^(-l_i) ≤ 1")
print(f"Kraft Sum: {kraft_sum:.4f}")


if kraft_sum <= 1:
    print("The code satisfies the Kraft inequality.")
else:
    print("The code does not satisfy the Kraft inequality.")

# Comparison with fixed-length coding
fixed_length = math.ceil(math.log2(len(events)))
print(f"\nComparison with fixed-length coding:")
print(f"Fixed-length code would use {fixed_length} bits per record.")
print(f"Huffman code uses {L:.2f} bits per record on average.")
print(f"This saves {fixed_length - L:.2f} bits per record on average.")