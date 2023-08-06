from .iso import verify_iso7064_code


def verify_lei_checksum_old(lei: str) -> bool:
    """
    Verify the validity of LEI checksum; old format before 1.12.2012
    """
    if not isinstance(lei, str):
        return False
    else:
        lei = lei.strip()

    if len(lei) != 20:
        return False

    return verify_iso7064_code(lei)


def verify_lei_checksum_new(lei: str) -> bool:
    """
    Verify the validity of LEI checksum; new format after 1.12.2012 with two reserved characters
    """
    if verify_lei_checksum_old(lei):
        return lei[4:6] == "00"  # Characters 5-6: Two reserved characters set to zero.

    return False


def verify_lei_checksum(lei: str) -> bool:
    """
    Verify the validity of LEI checksum
    """
    return verify_lei_checksum_new(lei) or verify_lei_checksum_old(lei)
