def Verifica_gpf(selector_base, selector_limit, data):
    if data < selector_base or data > selector_limit:
        print("   -> GPF: Endereço fora do limite do segmento!")
        return False
    else:
        return True

def SUB(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector):
    print("\nPara a instrução SUB, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> SUB <DST_OFFSET>, <SRC_OFFSET>")
    print("Exemplo: 00002400 SUB 00004000 000081B1")
    instr_input = input("   - Instrução: ").strip()

    try:
        partes = instr_input.split()
        if len(partes) != 4:
            raise ValueError("Formato inválido. É esperado 4 elementos separados por espaços.")

        instr_offset_str = partes[0]
        mnemonic = partes[1].upper()
        if mnemonic != "SUB":
            print("Erro: Instrução Inválida")
            return

        dst_offset_str = partes[2].replace(",", "")
        src_offset_str = partes[3]

        instr_offset = int(instr_offset_str, 16)
        dst_offset = int(dst_offset_str, 16)
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
        "EDI": hex(dst_offset),
        "EAX - High": 0x0,
        "EAX - Low": 0x0
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução SUB")
    print("==============================================\n")
    print("-" * 60)
    print("Passo 1 - Barramento de endereço:")
    linear_address_instr = code_base + instr_offset
    print(f"   -> Registradores: CS = {hex(code_base)}, EIP = {hex(instr_offset)}")
    if Verifica_gpf(code_base,code_limit,linear_address_instr):
        print(f"   -> Endereço Linear da instrução SUB = CS + EIP: {hex(linear_address_instr)}")
    else:
        return
    print("-" * 60)
    print("Passo 2 - Barramento de dados")
    print("   -> Salva no seguimento de código a instrução SUB")
    print(f"   -> EIP é Atualizado: EIP = EIP + 16 bits (4 em hexa) = {hex(instr_offset+4)}")
    registers['EIP'] = instr_offset+4
    print("-" * 60)
    print("Passo 3 - Barramento de endereço")
    print(f"   -> Registradores: CS = {hex(code_base)}, EIP = {hex(registers['EIP'])}")
    if Verifica_gpf(code_base,code_limit,code_base+registers['EIP']):
        print(f"   -> Endereço Linear do end1 (Destino) = CS + EIP = {hex(code_base + registers['EIP'])}")
    else:
        return
    print("-" * 60)
    print("Passo 4 - Barramento de dados")
    registers["EIP"] = registers["EIP"]+4
    print(f"   -> Salva no seguimento de código o end1")
    print(f"   -> EIP é atualizado: EIP = EIP + 16 bits (4 bits em hexa) = {hex(registers['EIP'])}")
    print(f"   -> Atribui valor a ESI e EDI: ESI = {hex(dst_offset)}, EDI = {hex(dst_offset)}")
    registers['EDI'] = dst_offset
    registers['ESI'] = dst_offset
    print("-" * 60)
    print("Passo 5 - Barramento de endereço")
    print(f"   -> Registradores: DS = {hex(data_base)}, ESI  = {hex(registers['ESI'])}")
    if Verifica_gpf(data_base,data_limit,data_base+registers['ESI']):
        print(f"   -> Endereço Linear do end1 em DS: DS + ESI = {hex(data_base+registers['ESI'])}")
    else:
        return
    print("-" * 60)
    print("Passo 6 - Barramento de dados")
    print(f"   -> Faz a leitura do valor armazenado no seguimento de dados em end1")
    dst_data_value = int(input("   -> Informe o valor armazenado no end1 (ex: 10): "), 16)
    print(f"   -> Salva em EAX High o valor armazenado: {hex(dst_data_value)}")
    registers["EAX - High"] = dst_data_value
    print("-" * 60)
    print("Passo 7 - Barramento de endereço")
    print(f"   -> Registradores: CS = {hex(code_base)}, EIP = {hex(registers['EIP'])}")
    if Verifica_gpf(code_base,code_limit,code_base+registers["EIP"]):
        print(f"   -> Endereço Linear do end2 em CS: CS + EIP = {hex(code_base+registers['EIP'])}")
    else:
        return
    print("-" * 60)
    print("Passo 8 - Barramento de dados")
    registers["EIP"] = registers["EIP"]+4
    print("   -> Salva no seguimento de código o end2")
    print(f"   -> EIP é atualizado: EIP = EIP + 16 bits (4 bits em hexa) = {hex(registers['EIP'])}")
    print(f"   -> Atribui o valor do end2 para ESI: ESI = {hex(src_offset)}")
    registers["ESI"] = src_offset
    print("-" * 60)
    print("Passo 9 - Barramento de endereço")
    print(f"   -> Registradores: DS = {hex(data_base)}, ESI = {hex(src_offset)}")
    if Verifica_gpf(data_base,data_limit,data_base+src_offset):
        print(f"   -> Endereço Linear do end2 em DS: DS + ESI = {hex(data_base+registers['ESI'])}")
    else:
        return
    print("-" * 60)
    print("Passo 10 - Barramento de dados")
    print(f"   -> Faz a leitura do valor armazenado no end2")
    src_data_value = int(input("   - Informe o valor armazenado em end2 (ex: 10): "), 16)
    print(f"   -> Salva em EAX low o valor armazenado: {hex(src_data_value)}")
    registers['EAX - Low'] = src_data_value
    print("-" * 60)
    print("Passo 11 - Barramento de endereço")
    print(f"   -> Registradores: DS = {hex(data_base)}, EDI = {hex(registers['EDI'])}")
    if Verifica_gpf(data_base,data_limit, data_base+registers['EDI']):
        print(f"   -> Endereço linear do end1 onde vai ser escrito o resultado da instrução SUB: DS + EDI = {hex(data_base+registers['EDI'])}")
    else:
        return
    print("-" * 60)
    print("Passo 12 - Barramento de dados")
    print("   -> É realizada a operação de subtração dos conteudos de end1 e end2")
    if registers['EAX - High'] - registers['EAX - Low'] < 0:
        registers["EAX"] = 0
    else:
        registers["EAX"] = hex(registers['EAX - High'] - registers['EAX - Low'])
    print(f"   -> EAX = EAX High - EAX LOW, EAX = {hex(registers['EAX - High'])} - {hex(registers['EAX - Low'])} = {registers['EAX']}")
    print(f" Resultado da subtração é escrito em end1!")
    print("-" * 60)
    print("Estado final dos Registradores:")
    registers["EAX - High"] = hex(registers["EAX - High"])
    registers["EAX - Low"] = hex(registers["EAX - Low"])
    registers["EDI"] = hex(registers['EDI'])
    registers['EIP'] = hex(registers['EIP'])
    registers['ESI'] = hex(registers['ESI'])
    for reg, valor in registers.items():
        print(f"   {reg}: {valor}") 
    print("\n")     
    print("="*60)
    print("Fim da Instrução.")
