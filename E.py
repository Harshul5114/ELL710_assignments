# ============================================================
# Part E -- Consider a Ternary Link
# ============================================================

import math
from C import calculate_part_c
from huffman import HuffmanEncoder

def calculate_part_e():
    c_results = calculate_part_c()
    pm = c_results["mode_averaged_distribution"]

    # Use the general D-ary HuffmanEncoder from huffman.py
    encoder = HuffmanEncoder(pm, D=3)
    codes = encoder.codes
    N_d = encoder.N_d

    L_ternary = sum(pm[event] * len(codes[event]) for event in pm)
    H3 = -sum(p * math.log(p) / math.log(3) for p in pm.values())
    efficiency = H3 / L_ternary

    return {
        "dummy_symbols": N_d,
        "codes": codes,
        "L_ternary": L_ternary,
        "H3": H3,
        "efficiency": efficiency,
        "L_binary": c_results["L_single"]
    }

if __name__ == "__main__":
    res = calculate_part_e()

    print("--- Part E: Ternary Huffman Coding (D = 3) ---")
    print(f"Dummy symbols required: {res['dummy_symbols']}\n")
    print("Event | Codeword | Length")
    print("-------------------------")
    for event, code in sorted(res['codes'].items()):
        print(f" {event}   |    {code:5} |   {len(code)}")

    print(f"\nExpected length:  {res['L_ternary']:.4f} ternary symbols/record")
    print(f"Ternary entropy:  {res['H3']:.4f} ternary symbols/record")
    print(f"Efficiency:       {res['efficiency']*100:.2f}%")

    # Ternary vs Binary throughputs
    rec_per_sym_b = 1.0 / res["L_binary"]
    rec_per_sym_t = 1.0 / res["L_ternary"]
    increase_pct = (rec_per_sym_t - rec_per_sym_b) / rec_per_sym_b * 100

    print("\nComparison with Binary Link:")
    print(f"  Baud-rate limited: Ternary is BETTER (+{increase_pct:.2f}% throughput: {rec_per_sym_t:.4f} vs {rec_per_sym_b:.4f} records/symbol)")
    print("  Power-limited:     Binary is BETTER (requires lower SNR for equivalent error rate)")
