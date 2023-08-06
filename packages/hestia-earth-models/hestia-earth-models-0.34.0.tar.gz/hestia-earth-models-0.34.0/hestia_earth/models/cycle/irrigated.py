"""
Irrigated

This model returns the Practice [irrigated](https://hestia.earth/term/irrigated).
Cycles are marked as fully irrigated if the sum of the [irrigation Inputs](https://hestia.earth/glossary?termType=water)
is greater than 25mm per hectare (250m3 per hectare).
"""
from hestia_earth.schema import TermTermType, CycleFunctionalUnit, PracticeStatsDefinition
from hestia_earth.utils.tools import list_average
from hestia_earth.utils.model import filter_list_term_type

from hestia_earth.models.log import debugValues, logShouldRun
from hestia_earth.models.utils.practice import _new_practice
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "practices": [{"@type": "Practice", "value": "", "term.termType": "waterRegime"}],
        "or": {
            "functionalUnit": "relative",
            "inputs": [{"@type": "Input", "term.termType": "water", "value": "> 250 (m3 per hectare)"}]
        }
    }
}
RETURNS = {
    "Practice": [{
        "value": "",
        "statsDefinition": "modelled"
    }]
}
TERM_ID = 'irrigated'


def _practice(value: float):
    practice = _new_practice(TERM_ID)
    practice['value'] = [value]
    practice['statsDefinition'] = PracticeStatsDefinition.MODELLED.value
    return practice


def _has_water_practices(practices: list):
    return not any([
        p for p in practices if p.get('term', {}).get('termType') == TermTermType.WATERREGIME.value
        and p.get('term', {}).get('@id') != TERM_ID
    ])


def run(cycle: dict):
    functional_unit = cycle.get('functionalUnit')
    has_water_practices = _has_water_practices(cycle.get('practices', []))
    irrigation_inputs = filter_list_term_type(cycle.get('inputs', []), TermTermType.WATER)
    irrigation_value_m3 = sum([list_average(i.get('value')) for i in irrigation_inputs if len(i.get('value', [])) > 0])
    value = 100 if all([
        has_water_practices,
        functional_unit != CycleFunctionalUnit._1_HA.value or irrigation_value_m3 > 250
    ]) else 0

    debugValues(cycle, model=MODEL, term=TERM_ID,
                has_water_practices=has_water_practices,
                irrigation_value=irrigation_value_m3)

    logShouldRun(cycle, MODEL, TERM_ID, True)

    return [_practice(value)]
