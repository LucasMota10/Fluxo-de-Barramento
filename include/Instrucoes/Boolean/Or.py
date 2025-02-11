def OR(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector):
    print("\nPara a instrução OR, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> OR <DST_OFFSET>, <SRC_OFFSET>")
    print("Exemplo: 00024000 OR 00040000 00081B10")
    instr_input = input("   - Instrução: ").strip()

    try:
        partes = instr_input.split()
        if len(partes) != 4:
            raise ValueError("Formato inválido. É esperado 4 elementos separados por espaços.")

        instr_offset_str = partes[0]
        mnemonic = partes[1].upper()
        if mnemonic != "OR":
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
    print("Simulação da Execução da Instrução OR")
    print("==============================================\n")
    
    print("Etapa 1: Busca da Instrução")
    linear_address_instr = code_base + instr_offset
    print("   -> Barramento de endereço: Calculo do endereço linear da instrução")
    print(f"   -> Endereço LINEAR da instrução: CS {hex(code_base)} + EIP {hex(instr_offset)} = {hex(linear_address_instr)}")
    
    if linear_address_instr < code_base or linear_address_instr > code_limit:
        print("   -> GPF: Endereço da instrução fora do limite do segmento de código!")
        return
    
    print("-" * 60)
    
    print("Etapa 2: Busca dos Operandos")
    print("   -> Barramento de endereço: Calculo do endereço linear do Destino (end1) e origem (end2)")
    linear_address_dst = data_base + dst_offset
    linear_address_src = data_base + src_offset

    print(f"Operando o END1 - Destino:")
    print(f"   -> Endereço Linear do endereço 1 (destino): DS {hex(data_base)} + EDI {hex(dst_offset)} = {hex(linear_address_dst)}")
    print(f"   -> Registradores manipulados:  DS = {hex(data_base)}, EDI = {hex(dst_offset)}")
    print(f"Embora não colocado, foi manipulado também CS e EIP, para a alocação do endereço no seguimento de código e possibilitar sua manipulação")
    if linear_address_dst < data_base or linear_address_dst > data_limit:
        print("   -> GPF: Endereço do operando DST fora do limite do segmento de dados!")
        return
    
    print(f"Operando o END2 - Origem")
    print(f"   -> Endereço Linear do endereço 2 (origem): DS {hex(data_base)} + ESI {hex(src_offset)} = {hex(linear_address_src)}")
    print(f"   -> Registradores manipulados:  DS = {hex(data_base)}, ESI = {hex(src_offset)}")
    print(f"Embora não colocado, foi manipulado também CS e EIP, para a alocação do endereço no seguimento de código e possibilitar sua manipulação")
    if linear_address_src < data_base or linear_address_src > data_limit:
        print("   -> GPF: Endereço do operando SRC fora do limite do segmento de dados!")
        return
    
    print("-" * 60)
    
    print("Etapa 3: Execução da Instrução OR")
    src_data_value = int(input("   - Informe o valor armazenado em SRC (ex: 0x12345678): "), 16)
    dst_data_value = int(input("   - Informe o valor armazenado em DST (ex: 0x87654321): "), 16)
    
    print(" A instrução OR vai comparar cada um dos bits dos dois operandos, mantendo 1 caso pelo menos um dos bits seja 1 e 0 se ambos os bits forem 0")
    
    end1 = (bin(dst_data_value)[2:])
    end2 = (bin(src_data_value)[2:])

    resultado = []
    for b1, b2 in zip(end1, end2):
        if b1 == '1' or b2 == '1':
            resultado.append('1')
        else:
            resultado.append('0')
    
    resultado = ''.join(resultado)
    resultado = int(resultado, 2)
    
    print(f"   -> Operação: {hex(dst_data_value)} | {hex(src_data_value)} = {hex(resultado)}")
    registers["DST"] = hex(resultado)
    
    print("-" * 60)
    
    print("Estado final dos Registradores:")
    for reg, valor in registers.items():
        print(f"   {reg}: {valor}")
    
    print("\n==============================================")
    print("Fim da Simulação.")