"""
ISO 7064

Standard ISO 7064 is used to validate LEI or IBAN among other things. More info: https://en.wikipedia.org/wiki/ISO_7064

Formula:

1. Select number: 123456
2. Apply the formula to obtain the 2 digits checksum: 98 - ((number * 100) % 97) % 97
3. Concat number and checksum to obtain the code: 12345676
4. Validate a code: code % 97 == 1
"""

ISO7064_MAP = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "A": "10",
    "B": "11",
    "C": "12",
    "D": "13",
    "E": "14",
    "F": "15",
    "G": "16",
    "H": "17",
    "I": "18",
    "J": "19",
    "K": "20",
    "L": "21",
    "M": "22",
    "N": "23",
    "O": "24",
    "P": "25",
    "Q": "26",
    "R": "27",
    "S": "28",
    "T": "29",
    "U": "30",
    "V": "31",
    "W": "32",
    "X": "33",
    "Y": "34",
    "Z": "35",
}


def convert_code_with_iso7064_map(code: str) -> int:
    """
    Helper function to convert code into numeric code based on ISO 7064 character map.
    """
    return int("".join(ISO7064_MAP[c] for c in code))


def calculate_iso7064_checksum(code: str) -> str:
    """
    Function that calculates checksum for based on ISO 7064
    """
    numeric_code = convert_code_with_iso7064_map(code)
    checksum = 98 - ((numeric_code * 100) % 97) % 97

    return "%02d" % checksum


def verify_iso7064_code(code: str) -> bool:
    """
    Verify the input code based on ISO 7064 standard
    """
    numeric_code = convert_code_with_iso7064_map(code)

    return numeric_code % 97 == 1
