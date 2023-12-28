def custom_hash(seed):
    # Simple hash function
    hash_value = 5381
    for char in seed:
        hash_value = (hash_value * 33) ^ ord(char)
    return hash_value & 0xFFFFFFFF

def custom_random(seed):
    # Use the hash function to generate a random number between 0 and 1
    hash_value = custom_hash(seed)
    random_value = (hash_value % 1000000) / 1000000.0
    return random_value