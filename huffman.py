from heapq import heappop, heappush, heapify

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.children = []

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"(char={self.char}, freq={self.freq})"

class HuffmanEncoder:
    def __init__(self, frequency_table, D=2):
        self.frequency_table = frequency_table
        self.D = D
        self.huffman_tree, self.N_d = self.build_huffman_tree()
        self.codes = self.generate_codes()

    def build_huffman_tree(self):
        N_s = len(self.frequency_table)
        if self.D > 2:
            remainder = (N_s - 1) % (self.D - 1)
            N_d = 0 if remainder == 0 else (self.D - 1) - remainder
        else:
            N_d = 0

        heap = [HuffmanNode(char, freq) for char, freq in self.frequency_table.items()]
        # Add dummy symbols with 0 probability
        for i in range(N_d):
            heap.append(HuffmanNode(f"Dummy_{i}", 0.0))

        heapify(heap)

        while len(heap) > 1:
            group = []
            for _ in range(self.D):
                if heap:
                    group.append(heappop(heap))
            
            merged_freq = sum(child.freq for child in group)
            merged = HuffmanNode("#", merged_freq)
            merged.children = group
            heappush(heap, merged)
            
        return heappop(heap), N_d

    def generate_codes(self):
        if not self.huffman_tree:
            return {}
        codes = {}
        # Iterative stack-based generation
        stack = [(self.huffman_tree, "")]
        while stack:
            node, current_code = stack.pop()
            if node is not None:
                if node.char != "#" and not node.char.startswith("Dummy_"):
                    codes[node.char] = current_code
                # Push children to the stack in reverse order so they are popped in correct order (0 to D-1)
                for i in range(len(node.children) - 1, -1, -1):
                    stack.append((node.children[i], current_code + str(i)))
        return codes

    def printTree(self):
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except Exception:
                pass
        self._printTreeHelper(self.huffman_tree, "", branch_label=None, is_last=True)

    def _printTreeHelper(self, node, prefix, branch_label=None, is_last=True):
        if node is None:
            return

        if node.char == "#":
            label = f"# ({node.freq:.4f})"
        else:
            label = f"{node.char}: {node.freq:.4f}"

        if branch_label is not None:
            connector = ("└── " if is_last else "├── ") + str(branch_label) + " "
        else:
            connector = ""

        print(prefix + connector + label)

        if branch_label is None:
            new_prefix = prefix
        else:
            new_prefix = prefix + ("      " if is_last else "│     ")

        valid_children = [c for c in node.children if c is not None]
        for i, child in enumerate(valid_children):
            child_is_last = (i == len(valid_children) - 1)
            self._printTreeHelper(child, new_prefix, branch_label=i, is_last=child_is_last)