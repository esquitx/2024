def read_data(filename='../input.txt'):
    with open(filename) as f:
        lines = [int(line) for line in f.read().strip().split("\n")]


    return lines


def part1(data):

    sum = 0
    for initial_number in data:
        secret_number = initial_number
        for _ in range(2000):

            # Step 1: multiply by 64 and mix
            temp = secret_number * 64
            secret_number ^= temp  # mix using XOR
            secret_number %= 16777216  # prune

            # Step 2: divide by 32 (floor division) and mix
            temp = secret_number // 32
            secret_number ^= temp  # mix using XOR
            secret_number %= 16777216  # prune

            # Step 3: multiply by 2048 and mix
            temp = secret_number * 2048
            secret_number ^= temp  # mix using XOR
            secret_number %= 16777216  # prune


        sum += secret_number
    
    return sum


def part2(data):
    # Store all possible sequences and their corresponding prices for each buyer
    buyer_sequences = {}
    
    for initial_number in data:
        secret_number = initial_number
        prices = []
        changes = []
        
        # Generate 2000 prices
        for _ in range(2001):  # 2001 to get 2000 changes
            prices.append(secret_number % 10)
            
            # Step 1: multiply by 64 and mix
            temp = secret_number * 64
            secret_number ^= temp
            secret_number %= 16777216

            # Step 2: divide by 32 and mix
            temp = secret_number // 32
            secret_number ^= temp
            secret_number %= 16777216

            # Step 3: multiply by 2048 and mix
            temp = secret_number * 2048
            secret_number ^= temp
            secret_number %= 16777216
        
        # Calculate price changes
        for i in range(1, len(prices)):
            changes.append(prices[i] - prices[i-1])
        
        # Store sequences of 4 changes and their corresponding prices
        sequences = {}
        for i in range(len(changes) - 3):
            seq = tuple(changes[i:i+4])
            if seq not in sequences:
                sequences[seq] = prices[i+4]
        
        buyer_sequences[initial_number] = sequences
    
    # Find the sequence that gives maximum bananas
    max_bananas = 0
    best_sequence = None
    
    # Get all unique sequences from all buyers
    all_sequences = set()
    for sequences in buyer_sequences.values():
        all_sequences.update(sequences.keys())
    
    # Test each sequence
    for seq in all_sequences:
        total_bananas = 0
        for buyer, sequences in buyer_sequences.items():
            if seq in sequences:
                total_bananas += sequences[seq]
        
        if total_bananas > max_bananas:
            max_bananas = total_bananas
            best_sequence = seq
    
    print(f"Best sequence: {best_sequence}")
    return max_bananas


if __name__ == '__main__':
    data = read_data('../test.txt')

    print(part1(data))
    print(part2(data))