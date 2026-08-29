import math

from huffman import HuffmanEncoder
from telemetry_data import *
from SFE import ShannonFanoElias


def entropy(distribution):
    return -sum(p * math.log2(p) for p in distribution.values())


def expected_length(distribution, codes):
    return sum(distribution[event] * len(codes[event]) for event in distribution)


def part_a():
    print("\n=== Part A: Huffman coding for the sunlit mode ===")
    encoder = HuffmanEncoder(sunlit_distribution)
    codes = encoder.codes
    events = sorted(codes)
    length_vector = [len(codes[event]) for event in events]
    L = expected_length(sunlit_distribution, codes)
    H = entropy(sunlit_distribution)
    efficiency = H / L if L > 0 else 0
    kraft_sum = sum(2 ** (-length) for length in length_vector)
    fixed_length = math.ceil(math.log2(len(events)))

    print(f"Events: {events}")
    print(f"Codes: {codes}")
    print(f"Length vector: {length_vector}")
    print(f"Expected length L: {L:.4f} bits/record")
    print(f"Entropy H: {H:.4f} bits/record")
    print(f"Efficiency η: {efficiency:.4f}")
    print(f"Kraft sum: {kraft_sum:.4f}")
    print(f"Fixed-length coding comparison: {fixed_length} bits/record")
    print(f"Savings vs fixed length: {fixed_length - L:.4f} bits/record")

    return {"codes": codes, "L": L, "H": H, "entropy": H}


def part_b():
    print("\n=== Part B: Cost of the code table ===")
    L = 2.6100
    header_bits = 32
    fixed_length = 3

    def fixed_bits_per_frame(N):
        return fixed_length * N

    def huffman_bits_per_frame(N):
        return header_bits + L * N

    N = 1
    while huffman_bits_per_frame(N) >= fixed_bits_per_frame(N):
        N += 1

    print(f"Smallest N where Huffman is cheaper: {N}")
    print(f"Fixed-length: {fixed_bits_per_frame(N):.4f} bits")
    print(f"Huffman:      {huffman_bits_per_frame(N):.4f} bits")

    for N in [50, 200, 500]:
        saving = (fixed_bits_per_frame(N) - huffman_bits_per_frame(N)) / N
        print(f"N = {N}: saving = {saving:.4f} bits/record")

    print(f"Maximum possible Huffman codeword length (8 symbols): 7 bits")


def part_c():
    print("\n=== Part C: One code vs two codes ===")
    sunlit_prob = 0.65
    eclipse_prob = 0.35

    single_encoder = HuffmanEncoder(mode_averaged_distribution)
    single_lengths = {event: len(code) for event, code in single_encoder.codes.items()}
    L_single = sum(mode_averaged_distribution[event] * single_lengths[event] for event in mode_averaged_distribution)

    sunlit_encoder = HuffmanEncoder(sunlit_distribution)
    eclipse_encoder = HuffmanEncoder(eclipse_distribution)

    sunlit_lengths = {event: len(code) for event, code in sunlit_encoder.codes.items()}
    eclipse_lengths = {event: len(code) for event, code in eclipse_encoder.codes.items()}
    L_sunlit = sum(sunlit_distribution[event] * sunlit_lengths[event] for event in sunlit_distribution)
    L_eclipse = sum(eclipse_distribution[event] * eclipse_lengths[event] for event in eclipse_distribution)
    L_two = sunlit_prob * L_sunlit + eclipse_prob * L_eclipse

    saving = L_single - L_two
    saving_percentage = (saving / L_single) * 100

    N = 1
    while N * L_two + 1 >= N * L_single:
        N += 1

    print(f"Mode-averaged entropy: {entropy(mode_averaged_distribution):.4f} bits/record")
    print(f"Single-code expected length: {L_single:.4f} bits/record")
    print(f"Two-code weighted expected length: {L_two:.4f} bits/record")
    print(f"Saving of two-code design: {saving:.4f} bits/record")
    print(f"Saving percentage: {saving_percentage:.4f}%")
    print(f"Break-even frame size: {N}")

    return {"L_single": L_single, "L_two": L_two, "L_eclipse": L_eclipse, "single_lengths": single_lengths, "mode_averaged_distribution": mode_averaged_distribution}


def part_d():
    print("\n=== Part D: Penalty of using the wrong model ===")
    c_results = part_c()
    single_lengths = c_results["single_lengths"]
    L_single = c_results["L_single"]
    L_eclipse = c_results["L_eclipse"]

    L_wrong = sum(eclipse_distribution[event] * single_lengths[event] for event in eclipse_distribution)
    H_eclipse = entropy(eclipse_distribution)
    penalty_huffman = L_wrong - L_eclipse
    penalty_entropy = L_wrong - H_eclipse

    D_e_pm = sum(
        eclipse_distribution[event] * math.log2(eclipse_distribution[event] / mode_averaged_distribution[event])
        for event in eclipse_distribution
    )

    print(f"Expected length using average-code in eclipse: {L_wrong:.4f} bits/record")
    print(f"Eclipse entropy: {H_eclipse:.4f} bits/record")
    print(f"Penalty relative to eclipse Huffman: {penalty_huffman:.4f} bits/record")
    print(f"Penalty relative to eclipse entropy: {penalty_entropy:.4f} bits/record")
    print(f"KL divergence D(pe || pm): {D_e_pm:.4f} bits/record")

    H_m = entropy(mode_averaged_distribution)
    redundancy_pm = L_single - H_m
    print(f"Single-code redundancy under pm: {redundancy_pm:.4f}")


def part_e():
    print("\n=== Part E: Ternary link analysis ===")
    c_results = part_c()
    pm = c_results["mode_averaged_distribution"]
    encoder = HuffmanEncoder(pm, D=3)
    codes = encoder.codes
    N_d = encoder.N_d
    L_ternary = expected_length(pm, codes)
    H3 = -sum(p * math.log(p) / math.log(3) for p in pm.values())
    efficiency = H3 / L_ternary if L_ternary > 0 else 0

    rec_per_sym_b = 1.0 / c_results["L_single"]
    rec_per_sym_t = 1.0 / L_ternary
    increase_pct = ((rec_per_sym_t - rec_per_sym_b) / rec_per_sym_b) * 100

    print(f"Dummy symbols required: {N_d}")
    print(f"Ternary expected length: {L_ternary:.4f} ternary symbols/record")
    print(f"Ternary entropy: {H3:.4f} ternary symbols/record")
    print(f"Efficiency: {efficiency * 100:.2f}%")
    print(f"Throughput increase vs binary link: {increase_pct:.2f}%")


def part_f():
    print("\n=== Part F: Shannon-Fano-Elias code ===")
    pm_distribution = mode_averaged_distribution

    encoder = ShannonFanoElias(pm_distribution)
    codes = encoder.get_codes()
    cumulative_prob = 0.0
    total_expected_length = 0.0
    H = 0.0

    print(f"{'Event':<6} | {'p_m(x)':<7} | {'F(x)':<7} | {'F_bar(x)':<10} | {'l(x)':<5} | {'Codeword'}")
    print('-' * 70)

    for symbol, p in pm_distribution.items():
        F = cumulative_prob + p
        F_bar = cumulative_prob + p / 2.0
        code = codes[symbol]
        length = len(code)
        total_expected_length += p * length
        H -= p * math.log2(p)
        print(f"{symbol:<6} | {p:<7.4f} | {F:<7.4f} | {F_bar:<10.6f} | {length:<5} | {code}")
        cumulative_prob = F

    print(f"Expected length L: {total_expected_length:.4f} bits/record")
    print(f"Mode-average entropy H: {H:.4f} bits/record")
    print(f"Bound check: {H + 1:.4f} <= {total_expected_length:.4f} < {H + 2:.4f}")

    record_count = RECORDS_BUFFERED
    link_rate = DATA_RATE_BPS
    pass_duration = PASS_DURATION_SECONDS
    pass_capacity = link_rate * pass_duration
    total_bits = record_count * total_expected_length
    capacity_used = (total_bits / pass_capacity) * 100
    print(f"Total bits needed: {total_bits:,.0f} bits")
    print(f"Pass capacity: {pass_capacity:,.0f} bits")
    print(f"Capacity used: {capacity_used:.2f}%")
    print("SFE feasible for the pass?" + (" YES" if total_bits <= pass_capacity else " NO"))


def part_g():
    print("\n=== Part G: Design comparison for the downlink ===")
    record_count = RECORDS_BUFFERED
    link_rate = DATA_RATE_BPS
    pass_duration = PASS_DURATION_SECONDS
    pass_capacity = link_rate * pass_duration
    frame_size = FRAME_SIZE

    designs = {
        "Fixed-Length (3-bit)": (3.0000, 0),
        "Single Huffman (p_m)": (2.7225, 0),
        "Two-Code Huffman (p_s, p_e + 1-bit flag)": (2.6485, 1),
        "Shannon-Fano-Elias (SFE)": (4.0545, 0),
    }

    print(f"{'Design Scheme':<40} | {'L (bits/rec)':<12} | {'Total Bits':<12} | {'Capacity Used':<14} | {'Feasible?'}")
    print('-' * 100)

    for name, (L, header_bits) in designs.items():
        num_frames = record_count / frame_size
        total_payload = record_count * L
        total_overhead = num_frames * header_bits
        total_bits = total_payload + total_overhead
        capacity_used = (total_bits / pass_capacity) * 100
        feasible = "YES" if total_bits <= pass_capacity else "NO (Overflow)"
        print(f"{name:<40} | {L:<12.4f} | {total_bits:<12,.0f} | {capacity_used:<13.2f}% | {feasible}")


def main():
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    part_f()
    part_g()


if __name__ == "__main__":
    main()
