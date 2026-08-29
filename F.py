from SFE import ShannonFanoElias
from probabilities import sunlit_distribution

import math

# Downlink system parameters
RECORD_COUNT = 1_700_000
LINK_RATE = 9600  # bits per second
PASS_DURATION = 480  # seconds
PASS_CAPACITY = LINK_RATE * PASS_DURATION  # 4,608,000 bits

# Part F requires using the mode-averaged distribution p_m
pm_distribution = {
    "E1": 0.2970,
    "E2": 0.1650,
    "E3": 0.1750,
    "E4": 0.1625,
    "E5": 0.0730,
    "E6": 0.0605,
    "E7": 0.0435,
    "E8": 0.0235,
}

# Initialize encoder with mode-averaged distribution
encoder = ShannonFanoElias(pm_distribution)
codes = encoder.get_codes()

# 1. Tabulate F(x), F_bar(x), l(x), and codewords
print(
    f"{'Event':<6} | {'p_m(x)':<7} | {'F(x)':<7} | {'F_bar(x)':<10} | {'l(x)':<5} | {'Codeword'}"
)
print("-" * 55)

cumulative_prob = 0.0
total_expected_length = 0.0
entropy = 0.0

for symbol, p in pm_distribution.items():
    f_bar = cumulative_prob + (p / 2.0)
    cumulative_prob += p

    cw = codes[symbol]
    length = len(cw)

    total_expected_length += p * length
    entropy -= p * math.log2(p)

    print(
        f"{symbol:<6} | {p:<7.4f} | {cumulative_prob:<7.4f} | {f_bar:<10.6f} | {length:<5} | {cw}"
    )

# 2. Performance Metrics
print("\n--- Part F Results ---")
print(f"Expected Length (L) : {total_expected_length:.4f} bits/record")
print(f"Mode-Avg Entropy (H): {entropy:.4f} bits/record")

# 3. Check bounds: H + 1 <= L < H + 2
lower_bound = entropy + 1
upper_bound = entropy + 2
print(
    f"Bound Check        : {lower_bound:.4f} <= {total_expected_length:.4f} < {upper_bound:.4f}"
)
print(f"Bound Satisfied    : {lower_bound <= total_expected_length < upper_bound}")

# 4. Bits per pass calculations
total_pass_bits = RECORD_COUNT * total_expected_length
capacity_percent = (total_pass_bits / PASS_CAPACITY) * 100

print(f"\n--- Downlink Analysis ---")
print(f"Total Bits Needed  : {total_pass_bits:,.0f} bits")
print(f"Pass Capacity      : {PASS_CAPACITY:,.0f} bits")
print(f"Capacity Used      : {capacity_percent:.2f}%")

if total_pass_bits > PASS_CAPACITY:
    print(
        "Is SFE a candidate?: NO. Requiring >100% pass capacity causes buffer overflow."
    )
else:
    print("Is SFE a candidate?: YES.")