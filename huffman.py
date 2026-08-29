from heapq import heappop, heappush, heapify

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"(char={self.char}, freq={self.freq})"

class HuffmanEncoder:
    def __init__(self, frequency_table):
        self.frequency_table = frequency_table
        self.huffman_tree = self.build_huffman_tree()
        self.codes = self.generate_codes()

    def build_huffman_tree(self):
        heap = [HuffmanNode(char, freq) for char, freq in self.frequency_table.items()]
        heapify(heap)

        while len(heap) > 1:
            left = heappop(heap)
            right = heappop(heap)
            merged = HuffmanNode("#", left.freq + right.freq)
            merged.left = left
            merged.right = right
            heappush(heap, merged)
        return heappop(heap)

    def generate_codes(self):
        if not self.huffman_tree:
            return {}
        codes = {}
        stack = [(self.huffman_tree, "")]
        while stack:
            node, current_code = stack.pop()
            if node is not None:
                if node.char != "#":
                    codes[node.char] = current_code
                if node.right is not None:
                    stack.append((node.right, current_code + "1"))
                if node.left is not None:
                    stack.append((node.left, current_code + "0"))
        return codes

    def encode(self, data):
        # Implementation for encoding data using the generated Huffman codes
        pass

    def decode(self, encoded_data):
        # Implementation for decoding data using the Huffman tree
        pass

    def printTree(self):
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except Exception:
                pass
        self._printTreeHelper(self.huffman_tree, "", is_left=None, is_last=True)

    def _printTreeHelper(self, node, prefix, is_left=None, is_last=True):
        if node is None:
            return

        if node.char == "#":
            label = f"# ({node.freq:.2f})"
        else:
            label = f"{node.char}: {node.freq:.2f}"

        if is_left is not None:
            bit = "0" if is_left else "1"
            connector = ("└── " if is_last else "├── ") + bit + " "
        else:
            connector = ""

        print(prefix + connector + label)

        if is_left is None:
            new_prefix = prefix
        else:
            new_prefix = prefix + ("      " if is_last else "│     ")

        children = []
        if node.left is not None:
            children.append((True, node.left))
        if node.right is not None:
            children.append((False, node.right))

        for i, (child_is_left, child_node) in enumerate(children):
            child_is_last = (i == len(children) - 1)
            self._printTreeHelper(child_node, new_prefix, is_left=child_is_left, is_last=child_is_last)