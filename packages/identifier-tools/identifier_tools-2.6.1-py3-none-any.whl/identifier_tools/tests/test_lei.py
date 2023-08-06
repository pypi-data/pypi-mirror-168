from identifier_tools.lei import (
    verify_lei_checksum,
    verify_lei_checksum_new,
    verify_lei_checksum_old,
)

from .utils import BadCodeType


def test_check_lei_format_nic_too_long():
    lei = "097900BEFH00000002179"
    assert verify_lei_checksum(lei) is False
    assert verify_lei_checksum_new(lei) is False
    assert verify_lei_checksum_old(lei) is False


def test_check_lei_format_nic_too_short():
    lei = "5M0EBIWWZRPS22MVDC4"
    assert verify_lei_checksum(lei) is False
    assert verify_lei_checksum_new(lei) is False
    assert verify_lei_checksum_old(lei) is False


def test_invalid_input_nic_type():
    lei = ("097900BEFH0000000217", "5M0EBIWWZRPS22MVDC43")
    assert verify_lei_checksum(lei) is False
    assert verify_lei_checksum_new(lei) is False
    assert verify_lei_checksum_old(lei) is False

    lei = {
        "lei1": "097900BEFH0000000217",
        "lei2": "5M0EBIWWZRPS22MVDC43",
    }
    assert verify_lei_checksum(lei) is False
    assert verify_lei_checksum_new(lei) is False
    assert verify_lei_checksum_old(lei) is False

    lei = 97900256700000002170
    assert verify_lei_checksum(lei) is False
    assert verify_lei_checksum_new(lei) is False
    assert verify_lei_checksum_old(lei) is False

    lei = BadCodeType()
    assert verify_lei_checksum(lei) is False
    assert verify_lei_checksum_new(lei) is False
    assert verify_lei_checksum_old(lei) is False


def test_valid_lei():
    lei = "097900BEFH0000000217"  # New
    assert verify_lei_checksum(lei) is True
    assert verify_lei_checksum_new(lei) is True
    assert verify_lei_checksum_old(lei) is True

    lei = "213800SQ8HA3IZPO1G03"  # New
    assert verify_lei_checksum(lei) is True
    assert verify_lei_checksum_new(lei) is True
    assert verify_lei_checksum_old(lei) is True

    lei = "5M0EBIWWZRPS22MVDC43"  # Old
    assert verify_lei_checksum(lei) is True
    assert verify_lei_checksum_new(lei) is False
    assert verify_lei_checksum_old(lei) is True

    lei = "HWUPKR0MPOU8FGXBT394"  # Old
    assert verify_lei_checksum(lei) is True
    assert verify_lei_checksum_new(lei) is False
    assert verify_lei_checksum_old(lei) is True


def test_output_type_for_verify_lei_checksum():
    output = verify_lei_checksum("RANDOM0CODE")
    assert isinstance(output, bool)
    assert output is False

    output = verify_lei_checksum("097900BEFH0000000217")  # New
    assert isinstance(output, bool)
    assert output is True

    output = verify_lei_checksum("5M0EBIWWZRPS22MVDC43")  # Old
    assert isinstance(output, bool)
    assert output is True


def test_output_type_for_verify_lei_checksum_new():
    output = verify_lei_checksum_new("RANDOM0CODE")
    assert isinstance(output, bool)
    assert output is False

    output = verify_lei_checksum_new("097900BEFH0000000217")  # New
    assert isinstance(output, bool)
    assert output is True

    output = verify_lei_checksum_new("5M0EBIWWZRPS22MVDC43")  # Old
    assert isinstance(output, bool)
    assert output is False


def test_output_type_for_verify_lei_checksum_old():
    output = verify_lei_checksum_old("RANDOM0CODE")
    assert isinstance(output, bool)
    assert output is False

    output = verify_lei_checksum_old("097900BEFH0000000217")  # New
    assert isinstance(output, bool)
    assert output is True

    output = verify_lei_checksum_old("5M0EBIWWZRPS22MVDC43")  # Old
    assert isinstance(output, bool)
    assert output is True
