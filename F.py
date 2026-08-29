from SFE import ShannonFanoElias
from probabilities import sunlit_distribution

encoder = ShannonFanoElias(sunlit_distribution)
print("Shannon-Fano-Elias Codes:")
for symbol, code in encoder.get_codes().items():
    print(f"{symbol}: {code}")