import re

from operator import itemgetter

from . import formats_constants as constants
from .mappers import territory_to_parent_mapper

BIC_RANK = 33
OTHER_IDENTIFIERS_RANK = 35


def verify_identifier_format(identifier: str, identifier_type: str, allow_unknown_type: bool = True) -> bool:
    """
    Validate identifier format, based on its type
    """
    if not isinstance(identifier, str) or not isinstance(identifier_type, str):
        result = False
    elif identifier_type in constants.IDENTIFIER_FORMATS:

        if bool(re.match(constants.IDENTIFIER_FORMATS[identifier_type], identifier)):
            result = True

            if identifier_type == "DE_TRD_RGSTR_CD":
                xjustiz_id = identifier.split("-")[1]

                if xjustiz_id not in constants.DE_TRD_RGSTR_CD_XJUSTIZ_ID:
                    result = False

        else:
            result = False

    elif allow_unknown_type:
        result = bool(re.match("[^+,]{1,50}", identifier))
    else:
        result = False

    return result


def verify_national_identifier_country(country_code: str, national_id_type: str) -> bool:
    """
    Checks if the national identifier type belongs to the specified country.

    :param country_code: String, containing ISO2 format country code.
    :param national_id_type: String, containing national identifier type.
    :return:
        True if identifier type belongs to the country.
        False if identifier type DOESN'T belong to the country.
    """
    if country_code != "MC":  # Monaco doesn't have identifiers which starts with FR (parent)
        country_iso2_mapped = territory_to_parent_mapper(country_code)
    else:
        country_iso2_mapped = country_code

    country_national_codes = [x for x in constants.ECB_NATIONAL_IDENTIFIERS if x.startswith(country_iso2_mapped)]

    if (
        national_id_type.startswith(country_iso2_mapped)
        or national_id_type == "BIC"
        or (
            national_id_type.startswith("GEN")
            and (len(country_national_codes) == 0 or country_iso2_mapped in constants.GEN_IDENTIFIER_COUNTRY_EXCEPTIONS)
        )
    ):
        return True
    else:
        return False


def get_country_identifiers(country_code: str) -> list:
    """
    returns all the national identifiers (from formats_constants) requested by country_code sorted descending by rank

    :param country_code: String, containing ISO2 format country code.
    """

    country_identifiers = []

    if country_code in constants.COUNTRY_IDENTIFIER_RANK:
        country_identifiers = sorted(constants.COUNTRY_IDENTIFIER_RANK.get(country_code), key=itemgetter(0))

    return country_identifiers


def get_identifier_rank(identifier_type: str) -> int:
    """
    returns rank value of given identifier_type from formats_constants
    """

    return_rank = OTHER_IDENTIFIERS_RANK

    if identifier_type == "BIC":
        return_rank = BIC_RANK

    country_code = identifier_type.split("_")[0]

    if country_code in constants.COUNTRY_IDENTIFIER_RANK:
        country_identifier_types = get_country_identifiers(country_code)

        for item in country_identifier_types:
            if identifier_type in item:
                return_rank = item[0]
                break

    return return_rank


def get_sorted_identifiers(identifiers: []) -> []:
    """
    returns given (in argument) identifiers sorted ascending by their rank values

    @param identifiers: an array of given identifiers as (subject_identifier_id, subject_identifier.code)
                   example : [(6175, 'US_CIK_CD'), (6162, 'US_EIN_CD'), (6174, 'US_DSFN_CD')]
    @return: an array of ascending sorted subject_identifiers by their rank
             example: [<SubjectIdentifier(id: 5002, type_id: 6162, list_id: 14, identifier: '12-3456789',
             identifier_meta: None, replaced_by: None)>, <SubjectIdentifier(id: 5000, type_id: 6175, list_id: 14,
             identifier: '0123456789', identifier_meta: None, replaced_by: None)>, <SubjectIdentifier(id: 5003,
             type_id: 6174, list_id: 14, identifier: '1234567', identifier_meta: None, replaced_by: None)>]
    """
    result = []
    to_be_sorted = []

    for identifier in identifiers:
        rank = get_identifier_rank(identifier[1][1])

        if rank < OTHER_IDENTIFIERS_RANK:
            result.append((identifier[0], identifier[1][0], identifier[1][1], rank))
        else:
            to_be_sorted.append((identifier[0], identifier[1][0], identifier[1][1], rank))

    to_be_sorted = sorted(to_be_sorted, key=itemgetter(2))
    result = sorted(result, key=itemgetter(3))

    # removing of redundant that used to be necessary for sorting purpose
    final_to_be_sorted = []
    for record in to_be_sorted:
        final_to_be_sorted.append(record[0])

    final_result = []
    for record in result:
        final_result.append(record[0])
    # it was more comfortable to sort that separately because result was sorted by rank, to_be_sorted alphabetically
    return final_result + final_to_be_sorted
