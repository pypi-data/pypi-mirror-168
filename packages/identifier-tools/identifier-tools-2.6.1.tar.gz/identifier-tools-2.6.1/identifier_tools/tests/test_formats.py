from identifier_tools.formats import (
    verify_identifier_format,
    verify_national_identifier_country,
    get_country_identifiers,
    get_identifier_rank,
    get_sorted_identifiers,
)

from .utils import BadCodeType
from ..formats_constants import IDENTIFIER_FORMATS
from ..formats_constants import ECB_NATIONAL_IDENTIFIERS as IDENTIFIERS
from ..formats_constants import COUNTRY_IDENTIFIER_RANK as RANKS


def test_invalid_input_identifier_format_type():
    assert verify_identifier_format(identifier=None, identifier_type=None) is False
    assert verify_identifier_format(identifier="12345678", identifier_type=None) is False
    assert verify_identifier_format(identifier=None, identifier_type="SK_ICO_CD") is False
    assert verify_identifier_format(identifier="12345678", identifier_type="SK_ICO_CD") is True

    identifiers = ("11841036", "11841036x")
    identifiers_types = ("SK_ICO_CD", "ICO_NI")
    assert verify_identifier_format(identifier=identifiers, identifier_type=identifiers_types) is False

    identifiers = {
        "ico": "11841036",
        "ico_ni": "11841036x",
    }
    identifiers_types = {"ico": "SK_ICO_CD", "ico_ni": "ICO_NI"}
    assert verify_identifier_format(identifier=identifiers, identifier_type=identifiers_types) is False

    identifier = 11841036
    assert verify_identifier_format(identifier=identifier, identifier_type="SK_ICO_CD") is False
    assert verify_identifier_format(identifier="12345678", identifier_type=identifier) is False

    identifier = BadCodeType()
    assert verify_identifier_format(identifier="12345678", identifier_type=identifier) is False


def test_unknown_type_strict_checking():
    assert verify_identifier_format(identifier="", identifier_type="XX_XXX_XX", allow_unknown_type=True) is False
    assert verify_identifier_format(identifier="", identifier_type="XX_XXX_XX", allow_unknown_type=False) is False

    assert verify_identifier_format(identifier=" ", identifier_type="XX_XXX_XX", allow_unknown_type=True) is True
    assert verify_identifier_format(identifier=" ", identifier_type="XX_XXX_XX", allow_unknown_type=False) is False


def test_known_type_identifier_length():
    for code in IDENTIFIER_FORMATS:
        assert verify_identifier_format(identifier="A" * 80, identifier_type=code) is False


def test_verify_identifier_formats():
    # Samples from European Central Bank spreadsheet
    assert verify_identifier_format(identifier_type="AE_BL_CD", identifier="41479") is True
    assert verify_identifier_format(identifier_type="AR_CUIT_CD", identifier="30-71024269-7") is True
    assert verify_identifier_format(identifier_type="AT_FB_CD", identifier="119982w") is True
    assert verify_identifier_format(identifier_type="AT_FB_CD", identifier="79063w") is True
    assert verify_identifier_format(identifier_type="AT_FB_CD", identifier="79063w3") is True
    assert verify_identifier_format(identifier_type="AT_GEM_CD", identifier="40801") is True
    assert verify_identifier_format(identifier_type="AT_IDENT_CD", identifier="7934858") is True
    assert verify_identifier_format(identifier_type="AT_LAE_CD", identifier="4") is True
    assert verify_identifier_format(identifier_type="AT_ZVR_CD", identifier="881400879") is True
    assert verify_identifier_format(identifier_type="AU_ABN_CD", identifier="34 072 814 058") is True
    assert verify_identifier_format(identifier_type="AU_ACN_CD", identifier="150 217 299") is True
    assert verify_identifier_format(identifier_type="BA_JIB_CD", identifier="4401057510004") is True
    assert verify_identifier_format(identifier_type="BA_MBS_CD", identifier="1-2454-10") is True
    assert verify_identifier_format(identifier_type="BA_MBS_CD", identifier="1-24548") is True
    assert verify_identifier_format(identifier_type="BA_MBS_CD", identifier="64-01-0012-10") is True
    assert verify_identifier_format(identifier_type="BA_PIB_CD", identifier="236031950005") is True
    assert verify_identifier_format(identifier_type="BE_OND_CD", identifier="0203201340") is True
    assert verify_identifier_format(identifier_type="BG_BULSTAT_CD", identifier="999999999") is True
    assert verify_identifier_format(identifier_type="BG_BULSTAT_CD", identifier="9999999999") is True
    assert verify_identifier_format(identifier_type="BG_BULSTAT_CD", identifier="9999999999999") is True
    assert verify_identifier_format(identifier_type="BG_UIC_CD", identifier="999999999") is True
    assert verify_identifier_format(identifier_type="BG_UIC_CD", identifier="9999999999999") is True
    assert verify_identifier_format(identifier_type="BG_VAT_CD", identifier="BG999999999") is True
    assert verify_identifier_format(identifier_type="BG_VAT_CD", identifier="BG9999999999") is True
    assert verify_identifier_format(identifier_type="BM_RN_CD", identifier="50657") is True
    assert verify_identifier_format(identifier_type="BM_RN_CD", identifier="7671") is True
    assert verify_identifier_format(identifier_type="BR_CNPJ_CD", identifier="21.325.097/2156-88") is True
    assert verify_identifier_format(identifier_type="BR_CNPJ_CD", identifier="21.325.097/2156-88") is True
    assert verify_identifier_format(identifier_type="BS_NBR_CD", identifier="8046725") is True
    assert verify_identifier_format(identifier_type="BS_NBR_CD", identifier="85844") is True
    assert verify_identifier_format(identifier_type="BY_NBR_CD", identifier="191262660") is True
    assert verify_identifier_format(identifier_type="BZ_TIN_CD", identifier="167815") is True
    assert verify_identifier_format(identifier_type="CA_BN_CD", identifier="167251986") is True
    assert verify_identifier_format(identifier_type="CA_REG_ID_CD", identifier="0759736") is True
    assert verify_identifier_format(identifier_type="CA_REG_ID_CD", identifier="BC1006807") is True
    assert verify_identifier_format(identifier_type="CH_ID_CD", identifier="CH-020-3003970-9") is True
    assert verify_identifier_format(identifier_type="CH_NUMMER", identifier="CH-130.3.018.934-7") is True
    assert verify_identifier_format(identifier_type="CH_UID_CD", identifier="CHE-123.456.789") is True
    assert verify_identifier_format(identifier_type="CL_RUT_CD", identifier="61.704.000-K") is True
    assert verify_identifier_format(identifier_type="CL_RUT_CD", identifier="61704000-1") is True
    assert verify_identifier_format(identifier_type="CN_CC_CD", identifier="167251986167251433") is True
    assert verify_identifier_format(identifier_type="CO_NIT_CD", identifier="802024439-2") is True
    assert verify_identifier_format(identifier_type="CY_CBCID_CD", identifier="DD447") is True
    assert verify_identifier_format(identifier_type="CY_DRCOR_CD", identifier="C273730") is True
    assert verify_identifier_format(identifier_type="CY_GG_CD", identifier="S1311020700") is True
    assert verify_identifier_format(identifier_type="CY_IF_CD", identifier="CYIF0242") is True
    assert verify_identifier_format(identifier_type="CY_OTHER_CD", identifier="DD447ASASASXCX44") is True
    assert verify_identifier_format(identifier_type="CY_PF_CD", identifier="PF3268") is True
    assert verify_identifier_format(identifier_type="CY_PF_CD", identifier="PF602") is True
    assert verify_identifier_format(identifier_type="CY_TIC_CD", identifier="12000018M") is True
    assert verify_identifier_format(identifier_type="CY_VAT_CD", identifier="10145530D") is True
    assert verify_identifier_format(identifier_type="CZ_ICO_CD", identifier="00006947") is True
    assert verify_identifier_format(identifier_type="CZ_NID_CD", identifier="8080107948") is True
    assert verify_identifier_format(identifier_type="CZ_NID_CD", identifier="90091883") is True
    assert verify_identifier_format(identifier_type="DE_GNR_CD", identifier="GNR3034LA-D4102") is True
    assert verify_identifier_format(identifier_type="DE_GNR_CD", identifier="GnR3034LA-D4102") is True
    assert verify_identifier_format(identifier_type="DE_HRA_CD", identifier="HRA100484-K1101") is True
    assert verify_identifier_format(identifier_type="DE_HRB_CD", identifier="HRB1234-R1101") is True
    assert verify_identifier_format(identifier_type="DE_PR_CD", identifier="PR2359-Y1101") is True
    assert verify_identifier_format(identifier_type="DE_TAX_CD", identifier="2475081508155") is True
    assert verify_identifier_format(identifier_type="DE_TRD_RGSTR_CD", identifier="GNR3034LA-D4102") is True
    assert verify_identifier_format(identifier_type="DE_TRD_RGSTR_CD", identifier="GnR3034LA-D4102") is True
    assert verify_identifier_format(identifier_type="DE_TRD_RGSTR_CD", identifier="HRA100484-K1101") is True
    assert verify_identifier_format(identifier_type="DE_TRD_RGSTR_CD", identifier="HRB1234UE-R1101") is True
    assert verify_identifier_format(identifier_type="DE_TRD_RGSTR_CD", identifier="PR2359-Y1101") is True
    assert verify_identifier_format(identifier_type="DE_TRD_RGSTR_CD", identifier="VR350378-M1305") is True
    assert verify_identifier_format(identifier_type="DE_VAT_CD", identifier="DE811258273") is True
    assert verify_identifier_format(identifier_type="DE_VR_CD", identifier="VR350378-M1305") is True
    assert verify_identifier_format(identifier_type="DK_CVR_CD", identifier="22756214") is True
    assert verify_identifier_format(identifier_type="DK_FT_CD", identifier="12345-678") is True
    assert verify_identifier_format(identifier_type="DK_FT_CD", identifier="3") is True
    assert verify_identifier_format(identifier_type="DK_FT_CD", identifier="3-123") is True
    assert verify_identifier_format(identifier_type="DK_FT_CD", identifier="3000") is True
    assert verify_identifier_format(identifier_type="DK_FT_CD", identifier="3000-01") is True
    assert verify_identifier_format(identifier_type="DK_SE_CD", identifier="22756214") is True
    assert verify_identifier_format(identifier_type="EC_RUC_CD", identifier="9922882800010") is True
    assert verify_identifier_format(identifier_type="EE_FON_CD", identifier="21") is True
    assert verify_identifier_format(identifier_type="EE_RG_CD", identifier="10005211") is True
    assert verify_identifier_format(identifier_type="ES_NIF_CD", identifier="A28015865") is True
    assert verify_identifier_format(identifier_type="ES_NIF_CD", identifier="S2826011E") is True
    assert verify_identifier_format(identifier_type="FI_ALV_CD", identifier="FI01120389") is True
    assert verify_identifier_format(identifier_type="FI_SIRA_CD", identifier="06716026#001") is True
    assert verify_identifier_format(identifier_type="FI_Y_CD", identifier="0112038-9") is True
    assert verify_identifier_format(identifier_type="FI_Y_CD", identifier="01120389") is True
    assert verify_identifier_format(identifier_type="FR_CIB", identifier="30003") is True
    assert verify_identifier_format(identifier_type="FR_IF_CD", identifier="FR0000000439") is True
    assert verify_identifier_format(identifier_type="FR_IF_CD", identifier="FR44444AA800") is True
    assert verify_identifier_format(identifier_type="FR_IF_CD", identifier="FRPI00004289") is True
    assert verify_identifier_format(identifier_type="FR_RNA_CD", identifier="W861001547") is True
    assert verify_identifier_format(identifier_type="FR_SIREN_CD", identifier="542051180") is True
    assert verify_identifier_format(identifier_type="GB_CRN_CD", identifier="01234567") is True
    assert verify_identifier_format(identifier_type="GB_CRN_CD", identifier="NL012345") is True
    assert verify_identifier_format(identifier_type="GB_CRN_CD", identifier="SC012345") is True
    assert verify_identifier_format(identifier_type="GB_FSR_CD", identifier="827161") is True
    assert verify_identifier_format(identifier_type="GB_UTR_CD", identifier="2415326715") is True
    assert verify_identifier_format(identifier_type="GB_UTR_CD", identifier="241532671K") is True
    assert verify_identifier_format(identifier_type="GB_VAT_CD", identifier="GB412051121") is True
    assert verify_identifier_format(identifier_type="GB_VAT_CD", identifier="GB532476983177") is True
    assert verify_identifier_format(identifier_type="GB_VAT_CD", identifier="GBGD321") is True
    assert verify_identifier_format(identifier_type="GB_VAT_CD", identifier="GBHA666") is True
    assert verify_identifier_format(identifier_type="GG_RN_CD", identifier="56753") is True
    assert verify_identifier_format(identifier_type="GR_AFM_CD", identifier="940498654") is True
    assert verify_identifier_format(identifier_type="GR_IMO_CD", identifier="9074729") is True
    assert verify_identifier_format(identifier_type="HK_CR_CD", identifier="2153177") is True
    assert verify_identifier_format(identifier_type="HK_CR_CD", identifier="F0002646") is True
    assert verify_identifier_format(identifier_type="HR_MBS_CD", identifier="080020970") is True
    assert verify_identifier_format(identifier_type="HR_MB_CD", identifier="03449602") is True
    assert verify_identifier_format(identifier_type="HR_OIB_CD", identifier="05937759187") is True
    assert verify_identifier_format(identifier_type="HU_CEG_CD", identifier="01-17-000705") is True
    assert verify_identifier_format(identifier_type="HU_FB_CD", identifier="FB999999") is True
    assert verify_identifier_format(identifier_type="HU_FB_CD", identifier="FB999A99") is True
    assert verify_identifier_format(identifier_type="HU_KOZ_CD", identifier="HU99999999") is True
    assert verify_identifier_format(identifier_type="HU_TOR_CD", identifier="99999999") is True
    assert verify_identifier_format(identifier_type="ID_NPWP_CD", identifier="01.001.634.3-093.000") is True
    assert verify_identifier_format(identifier_type="IE_CRO_CD", identifier="900488") is True
    assert verify_identifier_format(identifier_type="IE_GOV_CD", identifier="GV1040") is True
    assert verify_identifier_format(identifier_type="IE_GOV_CD", identifier="LA006") is True
    assert verify_identifier_format(identifier_type="IE_VAT_CD", identifier="IE1234567") is True
    assert verify_identifier_format(identifier_type="IE_VAT_CD", identifier="IE1234567WH") is True
    assert verify_identifier_format(identifier_type="IL_TAX_CD", identifier="514157999") is True
    assert verify_identifier_format(identifier_type="IM_RN_CD", identifier="000899L") is True
    assert verify_identifier_format(identifier_type="IM_RN_CD", identifier="016104V") is True
    assert verify_identifier_format(identifier_type="IM_RN_CD", identifier="114293C") is True
    assert verify_identifier_format(identifier_type="IM_TAX_CD", identifier="C155673-79") is True
    assert verify_identifier_format(identifier_type="IN_CIN_CD", identifier="L28920MH1945PLC004520") is True
    assert verify_identifier_format(identifier_type="IN_PAN_CD", identifier="AFZPK7190K") is True
    assert verify_identifier_format(identifier_type="IT_CCIAA_CD", identifier="NA0091712") is True
    assert verify_identifier_format(identifier_type="IT_CF_CD", identifier="00470400011") is True
    assert verify_identifier_format(identifier_type="IT_UCITS_CD", identifier="103900") is True
    assert verify_identifier_format(identifier_type="JE_TAX_CD", identifier="CC17261") is True
    assert verify_identifier_format(identifier_type="JP_CN_CD", identifier="1251425368993") is True
    assert verify_identifier_format(identifier_type="KR_TIN_CD", identifier="219-82-01220") is True
    assert verify_identifier_format(identifier_type="LI_FL_CD", identifier="FL-0001.012.124-5") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="AVI-68/74") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="D001") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="F001") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="I001") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="INV-TIPF") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="P001") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="S001") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="SF007") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="SF123") is True
    assert verify_identifier_format(identifier_type="LT_INV_CD", identifier="V001") is True
    assert verify_identifier_format(identifier_type="LT_JAR_CD", identifier="110486217") is True
    assert verify_identifier_format(identifier_type="LU_IF_CD", identifier="O123456C12345") is True
    assert verify_identifier_format(identifier_type="LU_RCS_CD", identifier="B0030775") is True
    assert verify_identifier_format(identifier_type="LU_RCS_CD", identifier="C126") is True
    assert verify_identifier_format(identifier_type="LU_VAT_CD", identifier="10355144") is True
    assert verify_identifier_format(identifier_type="LV_FON_CD", identifier="LV40203123846") is True
    assert verify_identifier_format(identifier_type="LV_FON_CD", identifier="LV44103104436") is True
    assert verify_identifier_format(identifier_type="LV_FON_CD", identifier="LVAF098101") is True
    assert verify_identifier_format(identifier_type="LV_FON_CD", identifier="LVAF211B02") is True
    assert verify_identifier_format(identifier_type="LV_FON_CD", identifier="LVB001007") is True
    assert verify_identifier_format(identifier_type="LV_FON_CD", identifier="LVIF098D10") is True
    assert verify_identifier_format(identifier_type="LV_FON_CD", identifier="LVIF263002") is True
    assert verify_identifier_format(identifier_type="LV_FON_CD", identifier="LVVF098010") is True
    assert verify_identifier_format(identifier_type="LV_NBR_CD", identifier="40103681895") is True
    assert verify_identifier_format(identifier_type="LV_VAT_CD", identifier="LV40103681895") is True
    assert verify_identifier_format(identifier_type="MC_CIB", identifier="30003") is True
    assert verify_identifier_format(identifier_type="MC_NIS_CD", identifier="6110Z07638") is True
    assert verify_identifier_format(identifier_type="MC_NIS_CD", identifier="6110Z07638") is True
    assert verify_identifier_format(identifier_type="MC_RCI_CD", identifier="84P02123") is True
    assert verify_identifier_format(identifier_type="MC_RCI_CD", identifier="84S02071") is True
    assert verify_identifier_format(identifier_type="MH_NBR_CD", identifier="478893") is True
    assert verify_identifier_format(identifier_type="MH_NBR_CD", identifier="53765") is True
    assert verify_identifier_format(identifier_type="MH_NBR_CD", identifier="8232") is True
    assert verify_identifier_format(identifier_type="MT_CNUM_CD", identifier="C 12345") is True
    assert verify_identifier_format(identifier_type="MT_OLE_CD", identifier="VO/0467") is True
    assert verify_identifier_format(identifier_type="MT_VAT_CD", identifier="13240110") is True
    assert verify_identifier_format(identifier_type="MX_RFC_CD", identifier="GFI-920961-IL7") is True
    assert verify_identifier_format(identifier_type="MY_CRN_CD", identifier="175932-M") is True
    assert verify_identifier_format(identifier_type="MY_CRN_CD", identifier="540781-U") is True
    assert verify_identifier_format(identifier_type="MY_CRN_CD", identifier="838820-A") is True
    assert verify_identifier_format(identifier_type="NC_NBR_CD", identifier="2000133058") is True
    assert verify_identifier_format(identifier_type="NL_KVK_CD", identifier="12345678") is True
    assert verify_identifier_format(identifier_type="NL_RSIN_CD", identifier="123456789") is True
    assert verify_identifier_format(identifier_type="NO_NBR_CD", identifier="987654321") is True
    assert verify_identifier_format(identifier_type="PA_RUC_CD", identifier="155646287") is True
    assert verify_identifier_format(identifier_type="PE_RUC_CD", identifier="20100152941") is True
    assert verify_identifier_format(identifier_type="PL_KRS_CD", identifier="56228") is True
    assert verify_identifier_format(identifier_type="PL_NIP_CD", identifier="7740001454") is True
    assert verify_identifier_format(identifier_type="PL_REGON_CD", identifier="610188201") is True
    assert verify_identifier_format(identifier_type="PL_VAT_CD", identifier="PL7740001454") is True
    assert verify_identifier_format(identifier_type="PT_ASF_CD", identifier="1206") is True
    assert verify_identifier_format(identifier_type="PT_FSA_CD", identifier="502") is True
    assert verify_identifier_format(identifier_type="PT_IF_CD", identifier="1131") is True
    assert verify_identifier_format(identifier_type="PT_NIF_CD", identifier="500792771") is True
    assert verify_identifier_format(identifier_type="RO_CUI_CD", identifier="RO1234567890") is True
    assert verify_identifier_format(identifier_type="RO_TAX_CD", identifier="RO9999999999") is True
    assert verify_identifier_format(identifier_type="RO_TRN_CD", identifier="J40/8302/1997") is True
    assert verify_identifier_format(identifier_type="RS_MB_CD", identifier="17464523") is True
    assert verify_identifier_format(identifier_type="RS_PIB_CD", identifier="600184098") is True
    assert verify_identifier_format(identifier_type="RU_INN_CD", identifier="1624351625") is True
    assert verify_identifier_format(identifier_type="RU_OGRN_CD", identifier="1036165026589") is True
    assert verify_identifier_format(identifier_type="SE_FIN_CD", identifier="11187") is True
    assert verify_identifier_format(identifier_type="SE_MOM_CD", identifier="SE554521579501") is True
    assert verify_identifier_format(identifier_type="SE_ORG_CD", identifier="554521-5795") is True
    assert verify_identifier_format(identifier_type="SE_ORG_CD", identifier="5545215795") is True
    assert verify_identifier_format(identifier_type="SG_ROB_CD", identifier="193500026Z") is True
    assert verify_identifier_format(identifier_type="SG_ROB_CD", identifier="201117341E") is True
    assert verify_identifier_format(identifier_type="SG_ROB_CD", identifier="S73FC2287H") is True
    assert verify_identifier_format(identifier_type="SI_DAV_CD", identifier="79007589") is True
    assert verify_identifier_format(identifier_type="SI_DDV_CD", identifier="SI79007589") is True
    assert verify_identifier_format(identifier_type="SI_MAT_CD", identifier="5063345000") is True
    assert verify_identifier_format(identifier_type="SK_ICO_CD", identifier="31364501") is True
    assert verify_identifier_format(identifier_type="SK_IF_CD", identifier="SK35742968TAM24") is True
    assert verify_identifier_format(identifier_type="SM_COE_CD", identifier="19854") is True
    assert verify_identifier_format(identifier_type="TH_NBR_CD", identifier="1055380286655") is True
    assert verify_identifier_format(identifier_type="TR_VKN_CD", identifier="71524152") is True
    assert verify_identifier_format(identifier_type="TW_TAX_CD", identifier="73251209") is True
    assert verify_identifier_format(identifier_type="US_CIK_CD", identifier="0001543040") is True
    assert verify_identifier_format(identifier_type="US_DSFN_CD", identifier="430749") is True
    assert verify_identifier_format(identifier_type="US_DSFN_CD", identifier="4307493") is True
    assert verify_identifier_format(identifier_type="US_EIN_CD", identifier="21-2567152") is True
    assert verify_identifier_format(identifier_type="UY_RUT_CD", identifier="216549300014") is True
    assert verify_identifier_format(identifier_type="AT_NOTAP_CD", identifier="123-to-je-jedno-nema-regex") is True
    assert verify_identifier_format(identifier_type="GEN_NOTAP_CD", identifier="123-to-je-jedno-nema-regex") is True
    assert verify_identifier_format(identifier_type="IE_NOTAP_CD", identifier="123-to-je-jedno-nema-regex") is True
    assert verify_identifier_format(identifier_type="SE_NOTAP_CD", identifier="123-to-je-jedno-nema-regex") is True
    assert verify_identifier_format(identifier_type="GEN_IPF_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_NBR_ENTTY_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_NCB_ENTTY_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_NSA_ENTTY_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_NSI_ENTTY_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_OTHER_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_PS_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_TAX_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_TRD_RGSTR_ENTTY_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="GEN_VAT_CD", identifier="1111") is True
    assert verify_identifier_format(identifier_type="BIC", identifier="BNPAFRPPXXX") is True
    assert verify_identifier_format(identifier_type="BIC", identifier="BNPAFRPP") is True


def test_invalid_identifier_formats():
    # Edge cases in regex which shouldnt pass
    assert verify_identifier_format(identifier="000184098", identifier_type="RS_PIB_CD") is False
    assert verify_identifier_format(identifier="31364501a", identifier_type="SK_ICO_CD") is False
    assert verify_identifier_format(identifier="551521-5795", identifier_type="SE_ORG_CD") is False
    assert verify_identifier_format(identifier="5505215795", identifier_type="SE_ORG_CD") is False


def test_verify_national_identifier_country_true():
    assert verify_national_identifier_country(country_code="CZ", national_id_type="CZ_ICO_CD") is True
    assert verify_national_identifier_country(country_code="ZZ", national_id_type="BIC") is True
    assert verify_national_identifier_country(country_code="ZZ", national_id_type="GEN_OTHER_CD") is True

    # Territory mapper case
    assert verify_national_identifier_country(country_code="BL", national_id_type="FR_RNA_CD") is True

    # Monaco special case
    assert verify_national_identifier_country(country_code="MC", national_id_type="MC_CIB") is True

    # Check countries that are allowed to have from GEN_IDENTIFIER
    assert verify_national_identifier_country(country_code="AE", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="AR", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="AU", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="BA", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="BM", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="BR", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="BS", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="BY", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="BZ", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="CA", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="CH", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="CL", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="CN", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="CO", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="EC", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="GB", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="GG", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="HK", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="ID", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="IL", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="IM", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="IN", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="JE", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="JP", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="KR", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="LI", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="MX", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="MY", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="NC", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="PA", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="PE", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="RS", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="RU", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="SG", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="SM", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="TH", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="TR", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="TW", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="US", national_id_type="GEN_OTHER_CD") is True
    assert verify_national_identifier_country(country_code="UY", national_id_type="GEN_OTHER_CD") is True


def test_verify_national_identifier_country_false():
    assert verify_national_identifier_country(country_code="CZ", national_id_type="GEN_OTHER_CD") is False
    assert verify_national_identifier_country(country_code="SG", national_id_type="SK_ICO_CD") is False
    assert verify_national_identifier_country(country_code="SK", national_id_type="CZ_ICO_CD") is False
    assert verify_national_identifier_country(country_code="ZZ", national_id_type="NON_EXISTING_TYPE") is False


def test_get_country_identifiers():
    assert get_country_identifiers("XX") == []
    assert get_country_identifiers("5") == []
    assert get_country_identifiers("") == []
    assert get_country_identifiers("TR") == [(1, "TR_VKN_CD")]


def test_get_identifier_rank():
    assert get_identifier_rank("BIC") == 33
    assert get_identifier_rank("DE_HRB") == 35
    assert get_identifier_rank("DE_DRB") == 35
    assert get_identifier_rank("XXX") == 35
    assert get_identifier_rank("US_EIN_CD") == 1
    assert get_identifier_rank("US_CIK_CD") == 2
    assert get_identifier_rank("GEN_TRD_RGSTR_ENTTY_CD") == 24
    assert get_identifier_rank("GEN_PS_CD") == 28


def test_get_sorted_identifiers():
    assert get_sorted_identifiers([(6175, "US_CIK_CD"), (6162, "US_EIN_CD"), (6174, "US_DSFN_CD")]) == [
        6175,
        6162,
        6174,
    ]
    assert get_sorted_identifiers([]) == []


def test_regex_for_every_rank():
    for identifier in IDENTIFIERS.keys():
        found = False

        for country_ranks in RANKS.items():
            for identifier_rank in country_ranks[1]:
                if identifier == identifier_rank[1]:
                    found = True
                    break

        # Do not compare with OLD identifiers not used by ECB any more...
        if identifier not in ("BIC", "DE_GNR_CD", "DE_HRA_CD", "DE_HRB_CD", "DE_PR_CD", "DE_VR_CD", "HK_BR_CD"):
            assert found is True, f"Identifier: {identifier} doesnt have RANK!"


def test_rank_for_every_regex():
    for country_ranks in RANKS.items():
        for identifier_rank in country_ranks[1]:
            found = False

            for identifier in IDENTIFIERS.keys():
                if identifier == identifier_rank[1]:
                    found = True
                    break

            assert found is True, f"Identifier RANK: {identifier_rank} doesnt have REGEX!"
