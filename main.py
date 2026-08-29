from huffman import HuffmanEncoder

def main():
    # Example frequency table for characters
    frequency_table = {
        'a': 5,
        'b': 9,
        'c': 12,
        'd': 13,
        'e': 16,
        'f': 45
    }

    # Create a HuffmanEncoder instance
    encoder = HuffmanEncoder(frequency_table)

    # Print the generated Huffman codes
    print("Huffman Codes:")
    for char, code in encoder.codes.items():
        print(f"{char}: {code}")

    print("\nHuffman Tree:")
    encoder.printTree()

if __name__ == "__main__":
    main()