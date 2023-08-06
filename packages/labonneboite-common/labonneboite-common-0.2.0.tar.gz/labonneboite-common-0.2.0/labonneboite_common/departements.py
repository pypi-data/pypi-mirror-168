from typing import Sequence


def get_departements() -> Sequence[str]:
    departements = ["{:02d}".format(d) for d in range(1, 96)] + ["97"]
    return departements


DEPARTEMENTS = get_departements()
