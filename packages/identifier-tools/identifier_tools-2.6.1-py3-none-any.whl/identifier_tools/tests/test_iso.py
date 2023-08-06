import pytest

from identifier_tools.iso import (
    calculate_iso7064_checksum,
    convert_code_with_iso7064_map,
    verify_iso7064_code,
)

from .utils import BadCodeType


def test_output_value_for_calculate_iso7064_checksum():
    """
    Test to calculate iso7064 checksum

    Same codes are used in test test_output_value_for_verify_iso7064_code to verify the code + checksum
    """
    checksum = calculate_iso7064_checksum("54930084UKLVMY22DS")
    assert checksum == "16"

    checksum = calculate_iso7064_checksum("213800WSGIIZCXF1P5")
    assert checksum == "72"

    checksum = calculate_iso7064_checksum("5493000IBP32UQZ0KL")
    assert checksum == "24"

    checksum = calculate_iso7064_checksum("U")
    assert checksum == "08"


def test_output_value_for_verify_iso7064_code():
    """
    Test verify code if the last two digit number as a checksum match the code

    Codes and checksums from test test_output_value_for_calculate_iso7064_checksum are used to verify the result
    """
    assert verify_iso7064_code("54930084UKLVMY22DS16") == 1
    assert verify_iso7064_code("213800WSGIIZCXF1P572") == 1
    assert verify_iso7064_code("5493000IBP32UQZ0KL24") == 1
    assert verify_iso7064_code("U08") == 1


def test_output_value_for_convert_code_with_iso7064_map():
    output = convert_code_with_iso7064_map("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert output == 1234567891011121314151617181920212223242526272829303132333435


def test_output_type_for_calculate_iso7064_checksum():
    output = calculate_iso7064_checksum("RANDOM0CODE")
    assert isinstance(output, str)


def test_output_type_for_verify_iso7064_code():
    output = verify_iso7064_code("RANDOM0CODE")
    assert isinstance(output, bool)


def test_output_type_for_convert_code_with_iso7064_map():
    output = convert_code_with_iso7064_map("RANDOM0CODE")
    assert isinstance(output, int)


def test_unexpected_code_type_for_calculate_iso7064_checksum():
    with pytest.raises(TypeError):
        assert calculate_iso7064_checksum(1346979)

    with pytest.raises(TypeError):
        assert calculate_iso7064_checksum(BadCodeType)


def test_unexpected_code_type_for_verify_iso7064_code():
    with pytest.raises(TypeError):
        assert verify_iso7064_code(1346979)

    with pytest.raises(TypeError):
        assert verify_iso7064_code(BadCodeType)


def test_unexpected_code_type_for_convert_code_with_iso7064_map():
    with pytest.raises(TypeError):
        assert convert_code_with_iso7064_map(1346979)

    with pytest.raises(TypeError):
        assert convert_code_with_iso7064_map(BadCodeType)
