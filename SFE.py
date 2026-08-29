import math


class ShannonFanoElias:

    def __init__(self, probabilities):
        self.probabilities = probabilities
        self.codes = {}

        self._validate()
        self._build_codes()

    def _validate(self):
        total = sum(self.probabilities.values())

        if abs(total - 1.0) > 1e-9:
            raise ValueError("Probabilities must sum to 1.")

        if any(p <= 0 for p in self.probabilities.values()):
            raise ValueError("All probabilities must be positive.")

    def _build_codes(self):
        cumulative = 0.0

        for symbol, probability in self.probabilities.items():

            # Midpoint of the probability interval
            F = cumulative + probability / 2

            # Number of bits required: ceil(log2(1/p)) + 1
            L = math.ceil(-math.log2(probability)) + 1

            # Binary expansion of F
            code = self._binary_fraction(F, L)

            self.codes[symbol] = code

            cumulative += probability

    @staticmethod
    def _binary_fraction(x, length):
        """Return the first `length` bits of the binary

        fractional representation of x.
        """
        bits = []

        for _ in range(length):
            x *= 2

            if x >= 1:
                bits.append("1")
                x -= 1
            else:
                bits.append("0")

        return "".join(bits)

    def get_codes(self):
        return self.codes.copy()