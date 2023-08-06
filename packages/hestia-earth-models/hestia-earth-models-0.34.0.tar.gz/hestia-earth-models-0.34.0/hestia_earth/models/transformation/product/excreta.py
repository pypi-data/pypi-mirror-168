"""
Product Excreta

This model calculates the value of every `Product` by taking the value of the `Input` with the same `term`.
Note: this model also substract `Emissions` for `Input` with `units` = `kg N`.
"""
from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.tools import list_sum, non_empty_list
from hestia_earth.utils.model import filter_list_term_type, find_term_match

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.product import _new_product
from hestia_earth.models.utils.constant import Units, convert_to_N
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.input import total_excreta
from .. import MODEL

REQUIREMENTS = {
    "Transformation": {
        "term.termType": "excretaManagement",
        "inputs": [{"@type": "Input", "value": "", "term.termType": "excreta"}],
        "products": [{"@type": "Product", "value": ""}]
    }
}
RETURNS = {
    "Product": [{
        "term.termType": "excreta",
        "value": ""
    }]
}
LOOKUPS = {
    "emission": "causesExcretaMassLoss"
}
MODEL_KEY = 'excreta'
MODEL_LOG = '/'.join([MODEL, 'product', MODEL_KEY])

EMISSIONS_VALUE = {
    Units.KG_N.value: lambda input, emissions: total_excreta([input]) - list_sum(list(map(convert_to_N, emissions))),
    Units.KG.value: lambda input, emissions: total_excreta([input], Units.KG),
    Units.KG_VS.value: lambda input, emissions: total_excreta([input], Units.KG_VS)
}


def _product_value(input: dict, emissions: list):
    units = input.get('term', {}).get('units')
    return EMISSIONS_VALUE.get(units, lambda *args: 0)(input, emissions)


def _add_product(transformation: dict, input: dict, emissions: list):
    term_id = input.get('term', {}).get('@id')
    value = list_sum(input.get('value', []), None)
    has_value = value is not None

    logRequirements(transformation, model=MODEL_LOG, term=term_id,
                    value=value,
                    has_value=has_value,
                    method='add')

    should_run = all([has_value])
    logShouldRun(transformation, MODEL_LOG, term_id, should_run)
    return {
        **input,
        **_new_product(term_id, _product_value(input, emissions))
    } if should_run else None


def _update_product(transformation: dict, product: dict, inputs: list, emissions: list):
    term_id = product.get('term', {}).get('@id')
    input = find_term_match(inputs, term_id)
    value = _product_value(input, emissions)
    has_value = value is not None

    logRequirements(transformation, model=MODEL_LOG, term=term_id,
                    value=value,
                    has_value=has_value,
                    method='update')

    should_run = all([has_value])
    logShouldRun(transformation, MODEL_LOG, term_id, should_run)
    return {**product, 'value': [value]} if should_run else None


def _run(transformation: dict):
    emissions = transformation.get('emissions', [])
    # only some emissions will reduce the mass
    emissions = [e for e in emissions if get_lookup_value(e.get('term', {}), LOOKUPS['emission'])]
    inputs = filter_list_term_type(transformation.get('inputs', []), TermTermType.EXCRETA)
    products = transformation.get('products', [])
    missing_products = [i for i in inputs if not find_term_match(products, i.get('term', {}).get('@id'), None)]

    debugValues(transformation, model=MODEL_LOG,
                missing_products=';'.join([p.get('term', {}).get('@id') for p in missing_products]))

    return non_empty_list([
        #  update the Product value that already exist
        (
            p if not find_term_match(inputs, p.get('term', {}).get('@id'))
            else _update_product(transformation, p, inputs, emissions)
        ) for p in products
    ]) + non_empty_list([
        #  add the Inputs as Product that do not exist
        _add_product(transformation, i, emissions) for i in missing_products
    ])


def _should_run(transformation: dict):
    node_type = transformation.get('type', transformation.get('@type'))
    should_run = all([
        node_type == SchemaType.TRANSFORMATION.value,
        transformation.get('term', {}).get('termType') == TermTermType.EXCRETAMANAGEMENT.value
    ])
    logShouldRun(transformation, MODEL_LOG, None, should_run)
    return should_run


def run(transformation: dict):
    return _run(transformation) if _should_run(transformation) else []
