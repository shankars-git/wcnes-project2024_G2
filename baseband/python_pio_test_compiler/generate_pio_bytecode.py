from typing import List

chip_extended_dict = {
    "0": "11 01 10 01 11 00 00 11 01 01 00 10 00 10 11 10",
    "1": "11 10 11 01 10 01 11 00 00 11 01 01 00 10 00 10",
    "2": "00 10 11 10 11 01 10 01 11 00 00 11 01 01 00 10",
    "3": "00 10 00 10 11 10 11 01 10 01 11 00 00 11 01 01",
    "4": "01 01 00 10 00 10 11 10 11 01 10 01 11 00 00 11",
    "5": "00 11 01 01 00 10 00 10 11 10 11 01 10 01 11 00",
    "6": "11 00 00 11 01 01 00 10 00 10 11 10 11 01 10 01",
    "7": "10 01 11 00 00 11 01 01 00 10 00 10 11 10 11 01",
    "8": "10 00 11 00 10 01 01 10 00 00 01 11 01 11 10 11",
    "9": "10 11 10 00 11 00 10 01 01 10 00 00 01 11 01 11",
    "A": "01 11 10 11 10 00 11 00 10 01 01 10 00 00 01 11",
    "B": "01 11 01 11 10 11 10 00 11 00 10 01 01 10 00 00",
    "C": "00 00 01 11 01 11 10 11 10 00 11 00 10 01 01 10",
    "D": "01 10 00 00 01 11 01 11 10 11 10 00 11 00 10 01",
    "E": "10 01 01 10 00 00 01 11 01 11 10 11 10 00 11 00",
    "F": "11 00 10 01 01 10 00 00 01 11 01 11 10 11 10 00", }


# data_hex = "0000000000000000000000000000000000000000000000000000000000000000"
# data_hex = "00000BADCFE00000BADCFE00000BADCFE00000BADCFE00000BADCFE"
# data_hex = "00000000A70E418801222234124444CDAB0177D5"
# data_hex = "000000007AE0148810222243214444DCBA10775D000000007AE0148810222243214444DCBA10775D000000007AE0148810222243214444DCBA10775D000000007AE0148810222243214444DCBA10775D"
# data_hex = "00000000A7 17 41 88 0B 22 22 34 12 44 44 CD AB 01 02 03 04 05 06 07 08 09 0A 4B 49"
# data_hex = "000000007A 71 14 88 B0 22 22 43 21 44 44 DC BA 10 20 30 40 50 60 70 80 90 A0 B4 94"
def flip_bytes(hex_str: str) -> str:
    return ''.join([hex_str[x:x + 2][::-1] for x in range(0, len(hex_str), 2)])


hex_packet_from_excel = "00000000A71741880B222234124444CDAB0102030405060708090A4B49"
data_hex = flip_bytes(hex_packet_from_excel)
print(data_hex)


def data_to_chips(hex_str: str) -> List[str]:
    output_array: List[str] = []
    for hex_character in hex_str:
        output_array.append(chip_extended_dict[hex_character])
    return output_array


def get_middle(sym1, sym2):
    # i1 = sym1[0]
    i2 = sym2[0]
    q1 = sym1[1]
    # q2 = sym2[1]
    return i2 + q1


def combine_chips(chips_list: List[str]) -> List[str]:
    full = " ".join(chips_list)
    symbols = full.split(" ")
    output_array: List[str] = [symbols[0]]
    for idx, symbol in enumerate(symbols[1:]):
        output_array.append(get_middle(symbols[idx], symbol))
        output_array.append(symbol)
    return output_array


waveforms_dict = {
    "01": "0000000011111111",
    "00": "0000111111110000",
    "10": "1111111100000000",
    "11": "1111000000001111",

}


def to_wave_forms(symbols: List[str], repeats: int = 1) -> List[str]:
    output_array: List[str] = []
    for symbol in symbols:
        for i in range(repeats):
            output_array.append(waveforms_dict[symbol])
    return output_array


def to_lengths(waves: List[str]):
    wave_str = "".join(waves)
    output_array: List[int] = []
    if wave_str[0] == "1":
        output_array.append(1)
    else:
        output_array.append(0)
    count = 1
    curr_char = wave_str[0]
    for char in wave_str[1:]:
        if curr_char != char:
            output_array.append(count)
            curr_char = char
            count = 1
        else:
            count += 1
    return output_array


def to_bits(lengths: List[int]):
    is_high = lengths[0] == 1
    values = lengths[1:]
    bits = []
    if is_high:
        bits.append(0)
    for l in lengths:
        if l == 4:
            bits += [0]
        if l == 8:
            bits += [1, 1, 0]
        if l == 12:
            bits += [1, 1, 1, 1, 0]
    # print(bits)
    bytes: List[str] = [""]
    idx = 0
    for b in bits:
        if len(bytes[idx]) >= 32:
            idx += 1
            bytes += [""]
        bytes[idx] += str(b)
    while len(bytes[idx]) < 32:
        bytes[idx] += str(0)
    # for s in bytes:
    #     print("0b"+s)
    return bytes


chips_extended: List[str] = combine_chips(data_to_chips(data_hex))
print(chips_extended)
bytes = to_bits(to_lengths(to_wave_forms(chips_extended, 4)))

for byte in bytes:
    print("0b" + byte + ",")
