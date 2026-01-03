PARAMS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(PARAMS)

def encode(num: int) -> str:
    if num == 0:
        return PARAMS[0]
    encoded = []
    while num > 0:
        remainder = num % BASE
        encoded.append(PARAMS[remainder])
        num //= BASE
    return "".join(reversed(encoded))

def decode(string: str) -> int:
    decoded = 0
    for char in string:
        index = PARAMS.find(char)
        if index == -1:
            raise ValueError(f"Invalid character in Base62 string: {char}")
        decoded = decoded * BASE + index
    return decoded
