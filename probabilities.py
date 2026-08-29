"""Backward-compatible import shim for the telemetry data module.

The project now stores the official system parameters and event distributions in
telemetry_data.py. This file preserves older imports such as
``from probabilities import sunlit_distribution`` while redirecting everything
through the shared centralized definitions.
"""

from telemetry_data import (
    DOWNLINK,
    DATA_RATE_BPS,
    PASS_DURATION_SECONDS,
    RECORDS_BUFFERED,
    SUNLIT_FRACTION,
    ECLIPSE_FRACTION,
    FRAME_SIZE,
    PASS_CAPACITY_BITS,
    sunlit_distribution,
    eclipse_distribution,
    pm_distribution,
    mode_averaged_distribution,
    mode_averaged,
)

__all__ = [
    "DOWNLINK",
    "DATA_RATE_BPS",
    "PASS_DURATION_SECONDS",
    "RECORDS_BUFFERED",
    "SUNLIT_FRACTION",
    "ECLIPSE_FRACTION",
    "FRAME_SIZE",
    "PASS_CAPACITY_BITS",
    "sunlit_distribution",
    "eclipse_distribution",
    "pm_distribution",
    "mode_averaged_distribution",
    "mode_averaged",
]

