from identifier_tools.ico import verify_ico_checksum, verify_ico_ni_checksum

from .utils import BadCodeType


def test_check_ico_format_nic_too_long():
    ico = "118410369"
    assert verify_ico_checksum(ico) is False


def test_check_ico_ni_format_nic_too_long():
    ico_ni = "118410369a"
    assert verify_ico_ni_checksum(ico_ni) is False


def test_check_ico_format_nic_too_short():
    ico = "1184103"
    assert verify_ico_checksum(ico) is False


def test_check_ico_ni_format_nic_too_short():
    ico_ni = "1184103a"
    assert verify_ico_ni_checksum(ico_ni) is False


def test_invalid_input_ico_type():
    ico = ("11841036", "11841036x")
    assert verify_ico_checksum(ico) is False
    assert verify_ico_ni_checksum(ico) is False

    ico = {
        "ico": "11841036",
        "ico_ni": "11841036x",
    }
    assert verify_ico_checksum(ico) is False
    assert verify_ico_ni_checksum(ico) is False

    ico = 11841036
    assert verify_ico_checksum(ico) is False
    assert verify_ico_ni_checksum(ico) is False

    ico = BadCodeType()
    assert verify_ico_checksum(ico) is False
    assert verify_ico_ni_checksum(ico) is False


def test_invalid_ico_format_not_numeric():
    ico = "A1841036"
    assert verify_ico_checksum(ico) is False

    ico = "1B841036"
    assert verify_ico_checksum(ico) is False

    ico = "11C41036"
    assert verify_ico_checksum(ico) is False

    ico = "118D1036"
    assert verify_ico_checksum(ico) is False

    ico = "1184E036"
    assert verify_ico_checksum(ico) is False

    ico = "11841F36"
    assert verify_ico_checksum(ico) is False

    ico = "118410G6"
    assert verify_ico_checksum(ico) is False

    ico = "1184103H"
    assert verify_ico_checksum(ico) is False


def test_invalid_ico_ni_format_first_part_not_numeric():
    ico_ni = "A1841036a"
    assert verify_ico_checksum(ico_ni) is False

    ico_ni = "1B841036b"
    assert verify_ico_checksum(ico_ni) is False

    ico_ni = "11C41036c"
    assert verify_ico_checksum(ico_ni) is False

    ico_ni = "118D1036d"
    assert verify_ico_checksum(ico_ni) is False

    ico_ni = "1184E036e"
    assert verify_ico_checksum(ico_ni) is False

    ico_ni = "11841F36f"
    assert verify_ico_checksum(ico_ni) is False

    ico_ni = "118410G6g"
    assert verify_ico_checksum(ico_ni) is False

    ico_ni = "1184103Hh"
    assert verify_ico_checksum(ico_ni) is False


def test_invalid_ico_ni_format_second_part_not_lowercase_character():
    ico_ni = "11841036I"
    assert verify_ico_ni_checksum(ico_ni) is False

    ico_ni = "118410361"
    assert verify_ico_ni_checksum(ico_ni) is False

    ico_ni = "11841036?"
    assert verify_ico_ni_checksum(ico_ni) is False

    ico_ni = "11841036@"
    assert verify_ico_ni_checksum(ico_ni) is False

    ico_ni = "11841036>"
    assert verify_ico_ni_checksum(ico_ni) is False


def test_valid_ico_and_ico_ni_strip_white_space_characters():
    ico = "     11841036         "  # spaces
    assert verify_ico_checksum(ico)
    ico_ni = "   11841036x       "  # spaces
    assert verify_ico_ni_checksum(ico_ni)
    ico = " 11841036        "  # tabs
    assert verify_ico_checksum(ico)
    ico_ni = "  11841036x      "  # tabs
    assert verify_ico_ni_checksum(ico_ni)


def test_valid_ico():
    ico = "11841036"
    assert verify_ico_checksum(ico)


def test_valid_ico_ni():
    ico = "11841036x"
    assert verify_ico_ni_checksum(ico)


def test_output_type_for_verify_ico_checksum():
    output = verify_ico_checksum("RANDOM0CODE")
    assert isinstance(output, bool)
    assert output is False

    output = verify_ico_checksum("11841036")
    assert isinstance(output, bool)
    assert output is True


def test_output_type_for_verify_ico_ni_checksum():
    output = verify_ico_ni_checksum("RANDOM0CODE")
    assert isinstance(output, bool)
    assert output is False

    output = verify_ico_ni_checksum("11841036a")
    assert isinstance(output, bool)
    assert output is True
