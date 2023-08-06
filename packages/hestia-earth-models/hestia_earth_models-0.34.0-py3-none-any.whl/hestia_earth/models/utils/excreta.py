def term_id_prefix(term_id: str): return term_id.split('Kg')[0]


def get_kg_term_id(term_id: str): return f"{term_id_prefix(term_id)}KgMass"


def get_kg_N_term_id(term_id: str): return f"{term_id_prefix(term_id)}KgN"


def get_kg_VS_term_id(term_id: str): return f"{term_id_prefix(term_id)}KgVs"


def get_all_term_ids(term_id: str):
    return [
        get_kg_term_id(term_id),  # set `kg` as first item because it usually contains the conversion ratios
        get_kg_N_term_id(term_id),
        get_kg_VS_term_id(term_id)
    ]
