def is_siret(siret: str) -> bool:
    # A valid SIRET is composed of 14 digits
    return len(siret) == 14 and siret.isdigit()
