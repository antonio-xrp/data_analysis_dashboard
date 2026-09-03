def formato_soles(valor):
    return f"S/ {valor:,.0f}"

def formato_monto(valor):
    """
    Convierte un monto en soles a un formato compacto.
    
    Ejemplos:
    1500       → S/ 1.5 K
    1500000    → S/ 1.5 M
    850        → S/ 850
    """

    if abs(valor) >= 1_000_000:
        return f"S/ {valor / 1_000_000:,.1f} M"

    elif abs(valor) >= 1_000:
        return f"S/ {valor / 1_000:,.1f} K"

    else:
        return f"S/ {valor:,.0f}"


def nombre_mes(numero):
    """
    Devuelve el nombre corto del mes en español.
    """

    meses = {
        1: "Ene",
        2: "Feb",
        3: "Mar",
        4: "Abr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dic"
    }

    return meses.get(numero)