from .formats import verify_identifier_format


def verify_ico_checksum(ico: str) -> bool:
    """
    Verify the validity of IČO checksum
    """
    if not isinstance(ico, str):
        return False
    else:
        ico = ico.strip()

    if not verify_identifier_format(ico, "SK_ICO_CD"):
        return False

    sucet = 0

    for i in range(7):
        sucet += int(ico[i]) * (8 - i)

    sucet %= 11
    z = (11 - sucet) % 10

    return int(ico[7]) == z


def verify_ico_ni_checksum(ico_ni: str) -> bool:
    """
    Verify the validity of IČO NI checksum

    IČO NI is unique identifier issued by NBS for subjects with duplicate national identifier (IČO).
    """
    if not isinstance(ico_ni, str):
        return False
    else:
        ico_ni = ico_ni.strip()

    if not verify_identifier_format(ico_ni, "ICO_NI"):
        return False

    return verify_ico_checksum(ico_ni[:8])
