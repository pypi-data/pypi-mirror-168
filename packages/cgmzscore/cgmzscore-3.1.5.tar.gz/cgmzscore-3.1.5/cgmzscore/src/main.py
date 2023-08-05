import json
from decimal import Decimal as D  # noqa: N817
import numpy as np

from .calculate import Zscore
from .constant import REPO_DIR, WHO_TABLES
from .extract_value import LmsBoxCox
from .table import Table
TABLE_REPO = REPO_DIR / 'tables'
GROWTH_CHART = {}


def setup_tables():
    for t in WHO_TABLES:
        table_name, _, _ = t.split('.')[0].rpartition('_')
        table = Table(TABLE_REPO / t)
        table.load_table()
        table.add_value()
        new_table = table.append_value()
        GROWTH_CHART[table_name] = new_table


def z_score_calculation(lms_box_cox: LmsBoxCox) -> float:
    lms_box_cox.get_file_name_from_data()
    lms_box_cox.get_lms_value(GROWTH_CHART)
    skew, median, coff, measurement = lms_box_cox.resolve_lms_value()
    z_score_value = Zscore(skew, median, coff, measurement).z_score_measurement()
    return z_score_value


def z_score_wfa(weight: str, age_in_days: str, sex: str) -> int:
    """z-score for weight for age"""
    setup_tables()
    z_score_wfa = []
    for w, a, s in zip(weight, age_in_days, sex):
        lms_box_cox = LmsBoxCox('wfa', weight=w, muac=None, age_in_days=a, sex=s, height=None)
        try:
            zscore = z_score_calculation(lms_box_cox)
        except:
            zscore = np.nan
        z_score_wfa.append(zscore)
    return z_score_wfa


def z_score_wfh(weight: list, age_in_days: list, sex: list, height: list) -> list:
    """z-score for weight for height"""
    setup_tables()

    z_score_wfh = []

    for w, a, s, h in zip(weight, age_in_days, sex, height):
        if D(a) <= 731:
            zscore = 'use z_score_wfl'
        else:
            lms_box_cox = LmsBoxCox('wfh', weight=w, muac=None, age_in_days=a, sex=s, height=h)
            try:
                zscore = z_score_calculation(lms_box_cox)
            except:
                zscore = np.nan
        z_score_wfh.append(zscore)
    return z_score_wfh


def z_score_wfl(weight: list, age_in_days: list, sex: list, height: list) -> list:
    """z-score for weight for length"""
    setup_tables()

    z_score_wfl = []

    for w, a, s, h in zip(weight, age_in_days, sex, height):
        if D(a) > 731:
            zscore = 'use z score wfh'
        else:
            lms_box_cox = LmsBoxCox('wfl', weight=w, muac=None, age_in_days=a, sex=s, height=h)
            try:
                zscore = z_score_calculation(lms_box_cox)
            except:
                zscore = np.nan
        z_score_wfl.append(zscore)
    return z_score_wfl


def z_score_lhfa(age_in_days: str, sex: str, height: str) -> int:
    """z-score for length/height for age"""
    setup_tables()
    z_score_lhfa = []
    for a, s, h in zip(age_in_days, sex, height):
        lms_box_cox = LmsBoxCox('lhfa', weight=None, muac=None, age_in_days=a, sex=s, height=h)
        try:
            zscore = z_score_calculation(lms_box_cox)
        except:
            zscore = np.nan
        z_score_lhfa.append(zscore)
    return z_score_lhfa


def z_score_with_class(weight: str, muac: str, age_in_days: str, sex: str, height: str):
    wfa = z_score_wfa(weight=weight, age_in_days=age_in_days, sex=sex)
    if wfa < -3:
        class_wfa = 'Severely Under-weight'
    elif -3 <= wfa < -2:
        class_wfa = 'Moderately Under-weight'
    else:
        class_wfa = 'Healthy'

    wfl = z_score_wfl(weight=weight, age_in_days=age_in_days, sex=sex, height=height)
    class_wfl = calculate_sam_mam(weight, muac, age_in_days, sex, height)

    lhfa = z_score_lhfa(age_in_days=age_in_days, sex=sex, height=height)
    if lhfa < -3:
        class_lhfa = 'Severely Stunted'
    elif -3 <= lhfa < -2:
        class_lhfa = 'Moderately Stunted'
    else:
        class_lhfa = 'Healthy'

    return json.dumps({'Z_score_WFA': wfa, 'Class_WFA': class_wfa, 'Z_score_WFH' if D(age_in_days) > 24 else
                       'Z_score_WFL': wfl, 'Class_WFH' if D(age_in_days) > 24 else 'Class_WFL': class_wfl,
                       'Z_score_HFA': lhfa, 'Class_HFA': class_lhfa})


def calculate_sam_mam(weight: str, muac: str, age_in_days: str, sex: str, height: str) -> str:
    assert muac is not None

    if D(age_in_days) > 731:
        wfl = z_score_wfh(
            weight=weight, age_in_days=age_in_days, sex=sex, height=height)
    else:
        wfl = z_score_wfl(
            weight=weight, age_in_days=age_in_days, sex=sex, height=height)
    if wfl < -3 or D(muac) < 11.5:
        diagnosis = "SAM"
    elif -3 <= wfl < -2 or D(muac) < 12.5:
        diagnosis = "MAM"
    else:
        diagnosis = "Healthy"
    return diagnosis
