DOWNLINK = "UHF"
DATA_RATE_BPS = 9600
PASS_DURATION_SECONDS = 480
RECORDS_BUFFERED = 1_700_000
SUNLIT_FRACTION = 0.65
ECLIPSE_FRACTION = 0.35
FRAME_SIZE = 200

PASS_CAPACITY_BITS = DATA_RATE_BPS * PASS_DURATION_SECONDS

sunlit_distribution = {
    "E1": 0.36,
    "E2": 0.20,
    "E3": 0.14,
    "E4": 0.11,
    "E5": 0.08,
    "E6": 0.05,
    "E7": 0.04,
    "E8": 0.02,
}

eclipse_distribution = {
    "E1": 0.18,
    "E2": 0.10,
    "E3": 0.24,
    "E4": 0.26,
    "E5": 0.06,
    "E6": 0.08,
    "E7": 0.05,
    "E8": 0.03,
}


def get_mode_averaged_distribution():
    return {
        event: SUNLIT_FRACTION * sunlit_distribution[event]
        + ECLIPSE_FRACTION * eclipse_distribution[event]
        for event in sunlit_distribution
    }

mode_averaged_distribution = get_mode_averaged_distribution()