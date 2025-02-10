def Verifica_gpf(selector_base, selector_limit, data):
    if data < selector_base or data > selector_limit:
        print("   -> GPF: Endereço fora do limite do segmento!")
        return False
    else:
        return True

def MUL(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector):
    print("\nPara a instrução MUL, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> MUL <SRC_OFFSET>")
    print("Exemplo: 00002400 MUL 00004000")
    instr_input = input("   - Instrução: ").strip()

    try:
        partes = instr_input.split()
        if len(partes) != 3:
            raise ValueError("Formato inválido. É esperado 3 elementos separados por espaços.")

        instr_offset_str = partes[0]
        mnemonic = partes[1].upper()
        if mnemonic != "MUL":
            print("Erro: Instrução Inválida")
            return

        src_offset_str = partes[2]

        instr_offset = int(instr_offset_str, 16)
        src_offset = int(src_offset_str, 16)
    except ValueError as ve:
        print("Erro ao interpretar a entrada. Certifique-se de usar o formato hexadecimal correto.")
        print("Detalhe:", ve)
        return

    registers = {
        "CS": cs_selector,
        "DS": ds_selector,
        "SS": ss_selector,
        "EIP": hex(instr_offset),
        "ESI": hex(src_offset),
        "EAX": 0x0,  # Valor inicial de EAX (pode ser alterado pelo usuário)
        "EDX": 0x0,  # Parte alta do resultado
        "EFLAGS": {"CF": 0, "OF": 0}  # Flags relevantes para a operação MUL
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução MUL")
    print("==============================================\n")
    print("-" * 60)
    print("Passo 1 - Barramento de endereço:")
    linear_address_instr = code_base + instr_offset
    print(f"   -> Registradores: CS = {hex(code_base)}, EIP = {hex(instr_offset)}")
    if Verifica_gpf(code_base, code_limit, linear_address_instr):
        print(f"   -> Endereço Linear da instrução MUL = CS + EIP: {hex(linear_address_instr)}")
    else:
        return
    print("-" * 60)
    print("Passo 2 - Barramento de dados")
    print("   -> Salva no segmento de código a instrução MUL")
    print(f"   -> EIP é Atualizado: EIP = EIP + 16 bits (4 em hexa) = {hex(instr_offset + 4)}")
    registers['EIP'] = instr_offset + 4
    print("-" * 60)
    print("Passo 3 - Barramento de endereço")
    print(f"   -> Registradores: CS = {hex(code_base)}, EIP = {hex(registers['EIP'])}")
    if Verifica_gpf(code_base, code_limit, code_base + registers['EIP']):
        print(f"   -> Endereço Linear do SRC (Fonte) = CS + EIP = {hex(code_base + registers['EIP'])}")
    else:
        return
    print("-" * 60)
    print("Passo 4 - Barramento de dados")
    registers["EIP"] = registers["EIP"] + 4
    print(f"   -> Salva no segmento de código o SRC")
    print(f"   -> EIP é atualizado: EIP = EIP + 16 bits (4 bits em hexa) = {hex(registers['EIP'])}")
    print(f"   -> Atribui valor a ESI: ESI = {hex(src_offset)}")
    registers['ESI'] = src_offset
    print("-" * 60)
    print("Passo 5 - Barramento de endereço")
    print(f"   -> Registradores: DS = {hex(data_base)}, ESI = {hex(registers['ESI'])}")
    if Verifica_gpf(data_base, data_limit, data_base + registers['ESI']):
        print(f"   -> Endereço Linear do SRC em DS: DS + ESI = {hex(data_base + registers['ESI'])}")
    else:
        return
    print("-" * 60)
    print("Passo 6 - Barramento de dados")
    print(f"   -> Faz a leitura do valor armazenado no SRC")
    src_data_value = int(input("   -> Informe o valor armazenado no SRC (ex: 0x00000002): "), 16)
    print(f"   -> Valor lido do SRC: {hex(src_data_value)}")
    print("-" * 60)
    print("Passo 7 - Barramento de endereço")
    print(f"   -> Registradores: EAX = {hex(registers['EAX'])}")
    eax_value = int(input("   -> Informe o valor armazenado em EAX (ex: 0x00000003): "), 16)
    registers['EAX'] = eax_value
    print("-" * 60)
    print("Passo 8 - Execução da Instrução MUL")
    resultado = registers['EAX'] * src_data_value  # Multiplicação de EAX por SRC
    edx_value = (resultado >> 32) & 0xFFFFFFFF  # Parte alta do resultado
    eax_value = resultado & 0xFFFFFFFF  # Parte baixa do resultado
    registers['EAX'] = eax_value
    registers['EDX'] = edx_value
    registers['EFLAGS']['CF'] = 1 if edx_value != 0 else 0  # CF = 1 se EDX != 0
    registers['EFLAGS']['OF'] = registers['EFLAGS']['CF']  # OF = CF para MUL
    print(f"   -> Resultado da Multiplicação: {hex(resultado)}")
    print(f"      - EAX (parte baixa): {hex(eax_value)}")
    print(f"      - EDX (parte alta): {hex(edx_value)}")
    print("   -> Flags atualizados:")
    print(f"      CF (Carry Flag): {registers['EFLAGS']['CF']}")
    print(f"      OF (Overflow Flag): {registers['EFLAGS']['OF']}")
    print("-" * 60)
    print("Estado final dos Registradores:")
    registers["EAX"] = hex(registers["EAX"])
    registers["EDX"] = hex(registers["EDX"])
    registers["EIP"] = hex(registers["EIP"])
    registers["ESI"] = hex(registers["ESI"])
    for reg, valor in registers.items():
        if reg == "EFLAGS":
            print(f"   {reg}:")
            for flag, val in valor.items():
                print(f"      {flag}: {val}")
        else:
            print(f"   {reg}: {valor}")
    print("\n==============================================")
    print("Fim da Instrução.")