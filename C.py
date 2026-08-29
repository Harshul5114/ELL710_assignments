# ============================================================
# Part C -- One Code, or Two?
# ============================================================

from telemetry_data import sunlit_distribution, eclipse_distribution
from huffman import HuffmanEncoder

SUNLIT_PROB = 0.65
ECLIPSE_PROB = 0.35


def calculate_part_c():
    # --------------------------------------------------------
    # Mode-averaged distribution
    # --------------------------------------------------------

    mode_averaged_distribution = {
        event: (
            SUNLIT_PROB * sunlit_distribution[event]
            + ECLIPSE_PROB * eclipse_distribution[event]
        )
        for event in sunlit_distribution
    }

    # --------------------------------------------------------
    # Single Huffman code
    # --------------------------------------------------------

    single_encoder = HuffmanEncoder(mode_averaged_distribution)

    single_lengths = {
        event: len(code)
        for event, code in single_encoder.codes.items()
    }

    L_single = sum(
        mode_averaged_distribution[event] * single_lengths[event]
        for event in mode_averaged_distribution
    )

    # --------------------------------------------------------
    # Two Huffman codes
    # --------------------------------------------------------

    sunlit_encoder = HuffmanEncoder(sunlit_distribution)
    eclipse_encoder = HuffmanEncoder(eclipse_distribution)

    sunlit_lengths = {
        event: len(code)
        for event, code in sunlit_encoder.codes.items()
    }

    eclipse_lengths = {
        event: len(code)
        for event, code in eclipse_encoder.codes.items()
    }

    L_sunlit = sum(
        sunlit_distribution[event] * sunlit_lengths[event]
        for event in sunlit_distribution
    )

    L_eclipse = sum(
        eclipse_distribution[event] * eclipse_lengths[event]
        for event in eclipse_distribution
    )

    # Average over the two operating modes
    L_two = (
        SUNLIT_PROB * L_sunlit
        + ECLIPSE_PROB * L_eclipse
    )

    # --------------------------------------------------------
    # Saving of two-code design over single-code design
    # --------------------------------------------------------

    saving = L_single - L_two
    saving_percentage = (saving / L_single) * 100

    # --------------------------------------------------------
    # Minimum frame size for the 1-bit mode flag to pay off
    # --------------------------------------------------------

    N = 1

    while N * L_two + 1 >= N * L_single:
        N += 1

    return {
        "mode_averaged_distribution": mode_averaged_distribution,
        "single_encoder": single_encoder,
        "single_lengths": single_lengths,
        "L_single": L_single,
        "sunlit_encoder": sunlit_encoder,
        "eclipse_encoder": eclipse_encoder,
        "sunlit_lengths": sunlit_lengths,
        "eclipse_lengths": eclipse_lengths,
        "L_sunlit": L_sunlit,
        "L_eclipse": L_eclipse,
        "L_two": L_two,
        "saving": saving,
        "saving_percentage": saving_percentage,
        "break_even_N": N
    }


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    results = calculate_part_c()

    print("Mode-averaged distribution:")
    for event, probability in results["mode_averaged_distribution"].items():
        print(f"{event}: {probability:.4f}")

    print("\nSingle-code Huffman:")
    print(results["single_encoder"].codes)
    print(
        f"Expected length: "
        f"{results['L_single']:.4f} bits/record"
    )

    print("\nTwo-code Huffman:")
    print(
        f"Sunlit expected length: "
        f"{results['L_sunlit']:.4f} bits/record"
    )
    print(
        f"Eclipse expected length: "
        f"{results['L_eclipse']:.4f} bits/record"
    )
    print(
        f"Overall expected length: "
        f"{results['L_two']:.4f} bits/record"
    )

    print("\nSaving:")
    print(
        f"Saving: "
        f"{results['saving']:.4f} bits/record"
    )
    print(
        f"Saving percentage: "
        f"{results['saving_percentage']:.4f}%"
    )

    print("\nBreak-even frame size:")
    print(
        f"Smallest N where two-code design is cheaper: "
        f"{results['break_even_N']}"
    )