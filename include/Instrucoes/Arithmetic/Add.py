def ADD(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector):
    print("\nPara a instrução ADD, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> ADD <DST_OFFSET>, <SRC_OFFSET>")
    print("Exemplo: 00024000 ADD 00040000 00081B10")
    instr_input = input("   - Instrução: ").strip()

    try:
        partes = instr_input.split()
        if len(partes) != 4:
            raise ValueError("Formato inválido. É esperado 4 elementos separados por espaços.")

        instr_offset_str = partes[0]
        mnemonic = partes[1].upper()
        if mnemonic != "ADD":
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
        "EAX": "0x0"
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução ADD")
    print("==============================================\n")
    
    print("Etapa 1: Busca da Instrução")
    linear_address_instr = code_base + instr_offset
    print(f"   -> Endereço Linear da instrução = CS {code_base} + EIP {instr_offset}: {hex(linear_address_instr)}")
    if linear_address_instr < code_base or linear_address_instr > code_limit:
        print("   -> GPF: Endereço da instrução fora do limite do segmento de código!")
        return
    print("   -> Salva no seguimento de código a instrução ADD")
    print("-" * 60)

    print("Etapa 2: Busca dos Operandos")

    linear_address_dst = data_base + dst_offset
    linear_address_src = data_base + src_offset

    print(f"   -> Endereço Linear do End1 = DS ({hex(data_base)} + EDI = {linear_address_dst}")
    if linear_address_dst < data_base or linear_address_dst > data_limit:
        print("   -> GPF: Endereço do operando DST fora do limite do segmento de dados!")
        return
    
    print(f"   -> Endereço Linear do End2 = DS {hex(data_base)} + ESI = {linear_address_src}")

    if linear_address_src < data_base or linear_address_src > data_limit:
        print("   -> GPF: Endereço do operando SRC fora do limite do segmento de dados!")
        return
    
    print("-" * 60)
    
    print("Etapa 3: Execução da Instrução ADD")
    src_data_value = int(input("   - Informe o valor armazenado em SRC (ex: 0x12345678): "), 16)
    dst_data_value = int(input("   - Informe o valor armazenado em DST (ex: 0x87654321): "), 16)
    
    result = dst_data_value + src_data_value
    
    print(f"   -> Operação: {hex(dst_data_value)} + {hex(src_data_value)} = {hex(result)}")
    registers["DST"] = hex(result)
    registers["EAX"] = hex(result)
    
    print("-" * 60)
    
    print("Estado final dos Registradores:")
    for reg, valor in registers.items():
        print(f"   {reg}: {valor}")
        
    print("\n==============================================")
    print("Fim da Simulação.")
