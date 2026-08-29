# ============================================================
# Part D -- Put a Number on Using the Wrong Model
# ============================================================

import math
from telemetry_data import sunlit_distribution, eclipse_distribution
from huffman import HuffmanEncoder
from C import calculate_part_c

# The single Huffman code was constructed using pm
# from Part C.
c_results = calculate_part_c()
single_code_lengths = c_results['single_lengths']
mode_averaged_distribution = c_results['mode_averaged_distribution']
L_single = c_results['L_single']
L_eclipse = c_results['L_eclipse']



# ------------------------------------------------------------
# Expected length of the single-code Huffman code
# on the eclipse distribution
# ------------------------------------------------------------

L_wrong = sum(
    eclipse_distribution[event] * single_code_lengths[event]
    for event in eclipse_distribution
)

print("Part D")
print(f"Expected length using average-code in eclipse: "
      f"{L_wrong:.4f} bits/record")


# ------------------------------------------------------------
# Eclipse entropy
# ------------------------------------------------------------

H_eclipse = -sum(
    p * math.log2(p)
    for p in eclipse_distribution.values()
)

print(f"Eclipse entropy: {H_eclipse:.4f} bits/record")


# ------------------------------------------------------------
# Penalty relative to eclipse-optimal Huffman
# ------------------------------------------------------------

# L_eclipse was calculated in Part C
penalty_huffman = L_wrong - L_eclipse

print(f"Penalty relative to eclipse Huffman: "
      f"{penalty_huffman:.4f} bits/record")


# ------------------------------------------------------------
# Penalty relative to eclipse entropy
# ------------------------------------------------------------

penalty_entropy = L_wrong - H_eclipse

print(f"Penalty relative to eclipse entropy: "
      f"{penalty_entropy:.4f} bits/record")


# ------------------------------------------------------------
# KL divergence D(pe || pm)
# ------------------------------------------------------------

D_e_pm = sum(
    eclipse_distribution[event]
    * math.log2(
        eclipse_distribution[event] / mode_averaged_distribution[event]
    )
    for event in eclipse_distribution
)

print(f"KL divergence D(pe || pm): "
      f"{D_e_pm:.4f} bits/record")


# ------------------------------------------------------------
# ------------------------------------------------------------
# Check the relationship:
#
# L_wrong - H(pe)
# =
# D(pe || pm) + Expected Discretization Overhead under pe
# where
# Expected Discretization Overhead under pe = sum( pe(x) * (l(x) + log2(pm(x))) )
# ------------------------------------------------------------

expected_discretization_overhead_pe = sum(
    eclipse_distribution[event]
    * (single_code_lengths[event] + math.log2(mode_averaged_distribution[event]))
    for event in eclipse_distribution
)

# For comparison, the redundancy under pm itself:
H_m = -sum(
    p * math.log2(p)
    for p in mode_averaged_distribution.values()
)
redundancy_pm = L_single - H_m

print("\nVerification:")
print(f"L_wrong - H(pe):                 {penalty_entropy:.4f}")
print(f"D(pe || pm):                     {D_e_pm:.4f}")
print(f"Expected discretization overhead: {expected_discretization_overhead_pe:.4f}")
print(f"D + overhead:                    {D_e_pm + expected_discretization_overhead_pe:.4f}")
print(f"Single-code redundancy (under pm):{redundancy_pm:.4f}")