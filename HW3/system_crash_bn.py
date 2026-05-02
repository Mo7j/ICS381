from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


def generate_bn():
    model = BayesianNetwork([
        ('M', 'S'),
        ('W', 'S'),
        ('W', 'H'),
        ('S', 'C'),
        ('H', 'C')
    ])

    cpd_M = TabularCPD('M', 2, [[0.15], [0.85]], state_names={'M': [False, True]})
    cpd_W = TabularCPD('W', 2, [[0.60], [0.40]], state_names={'W': [False, True]})

    cpd_S = TabularCPD(
        'S', 2,
        [
            [0.95, 0.90, 0.20, 0.05],
            [0.05, 0.10, 0.80, 0.95]
        ],
        evidence=['M', 'W'],
        evidence_card=[2, 2],
        state_names={'S': [False, True], 'M': [False, True], 'W': [False, True]}
    )

    cpd_H = TabularCPD(
        'H', 2,
        [
            [0.65, 0.25],
            [0.35, 0.75]
        ],
        evidence=['W'],
        evidence_card=[2],
        state_names={'H': [False, True], 'W': [False, True]}
    )

    cpd_C = TabularCPD(
        'C', 2,
        [
            [0.99, 0.35, 0.10, 0.01],
            [0.01, 0.65, 0.90, 0.99]
        ],
        evidence=['S', 'H'],
        evidence_card=[2, 2],
        state_names={'C': [False, True], 'S': [False, True], 'H': [False, True]}
    )

    model.add_cpds(cpd_M, cpd_W, cpd_S, cpd_H, cpd_C)

    model.check_model()

    return model


def exact_inference(sc_bn, variables, evidence=None):
    inference = VariableElimination(sc_bn)

    if isinstance(variables, dict):
        result = inference.query(
            variables=list(variables.keys()),
            evidence=evidence,
            show_progress=False
        )

        idx = tuple(
            result.state_names[var].index(val)
            for var, val in variables.items()
        )

        return float(result.values[idx])

    else:
        return inference.query(
            variables=list(variables),
            evidence=evidence,
            show_progress=False
        )
