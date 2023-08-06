from identifier_tools.formats import verify_identifier_format


def test_identifier_does_not_pass_regex():
    assert verify_identifier_format(identifier=None, identifier_type="DE_TRD_RGSTR_CD") is False
    assert (
        verify_identifier_format(identifier="GnR3034LA-D410", identifier_type="DE_TRD_RGSTR_CD") is False
    )  # incorrect format of xjustiz_id
    assert (
        verify_identifier_format(identifier="GnR3034LALALA-D4102", identifier_type="DE_TRD_RGSTR_CD") is False
    )  # incorrect number of capital letters
    assert (
        verify_identifier_format(identifier="GnRLA-D4102", identifier_type="DE_TRD_RGSTR_CD") is False
    )  # incorrect length of register nummer
    assert (
        verify_identifier_format(identifier="GGG3034LA-D4102", identifier_type="DE_TRD_RGSTR_CD") is False
    )  # incorrect first letters


def test_identifier_pass_regex():
    assert (
        verify_identifier_format(identifier="GnR3034LA-Q4102", identifier_type="DE_TRD_RGSTR_CD") is False
    )  # incorrect xjustix_id
    assert verify_identifier_format(identifier="GnR3034LA-Q4102", identifier_type=None) is False
    assert verify_identifier_format(identifier="GnR3034LA-D4102", identifier_type="DE_TRD_RGSTR_CD") is True
