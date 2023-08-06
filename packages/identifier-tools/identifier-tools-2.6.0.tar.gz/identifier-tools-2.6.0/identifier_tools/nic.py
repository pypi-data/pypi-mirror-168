import datetime

from .formats import verify_identifier_format
from .iso import calculate_iso7064_checksum, verify_iso7064_code


def verify_nic_sequence_checksum(sequence: str, checksum: str) -> bool:
    """
    Verify the validity of NIČ sequence checksum

    NIČ is unique identifier issued in sequence and each sequence has its own checksum.
    """
    if calculate_iso7064_checksum(code=sequence) != checksum:
        return False

    return True


def verify_nic_checksum(nic: str) -> bool:
    """
    Verify the validity of NIČ checksum

    NIČ is unique identifier issued by NBS for foreign (non-SK) subjects.
    """
    if not isinstance(nic, str):
        return False
    else:
        nic = nic.strip()

    if not verify_identifier_format(nic, "NIC"):
        return False

    if not int(nic[9:13]) > 0:
        return False

    try:
        datetime.date(year=int(nic[:4]), month=int(nic[4:6]), day=int(nic[6:8]))
    except ValueError:
        return False

    if not verify_nic_sequence_checksum(sequence=nic[0:13], checksum=nic[13:15]):
        return False

    return verify_iso7064_code(nic)
