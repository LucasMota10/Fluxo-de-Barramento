
def endereco_linear(seletor, offset, descritores):
    base = descritores.get_valor("", "END. BASE DO SEGMENTO")
    limite = descritores.get_valor("", "END. LIMITE")
    if offset > limite:
        print("Erro: Offset excede o limite do segmento!")
        return None
    return base + offset