def XCHG(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector):
    print("\nPara a instrução XCHG, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> XCHG <OP1_OFFSET>, <OP2_OFFSET>")
    print("Exemplo: 00024000 XCHG 00040000 00081B10")
    instr_input = input("   - Instrução: ").strip()

    # Tenta separar os componentes da linha de comando.
    try:
        # Exemplo de entrada: "00024000 XCHG 00040000 00081B10"
        # Primeiro separamos por espaços:
        partes = instr_input.split()
        if len(partes) != 4:
            raise ValueError("Formato inválido. É esperado 4 elementos separados por espaços.")

        # O primeiro elemento é o offset da instrução (EIP)
        instr_offset_str = partes[0]
        # O segundo deve ser o mnemônico (XCHG)
        mnemonic = partes[1].upper()
        if mnemonic != "XCHG":
            print("Erro: Instrução Inválida")
            return

        # O terceiro elemento contém o offset OP1 com uma vírgula no final (opcional)
        op1_offset_str = partes[2].replace(",", "")
        # O quarto elemento é o offset OP2
        op2_offset_str = partes[3]

        # Converte as strings em inteiros (base 16)
        instr_offset = int(instr_offset_str, 16)
        op1_offset   = int(op1_offset_str, 16)
        op2_offset   = int(op2_offset_str, 16)
    except ValueError as ve:
        print("Erro ao interpretar a entrada. Certifique-se de usar o formato hexadecimal correto.")
        print("Detalhe:", ve)
        return

    # Inicializa os registradores (incluindo EIP com o offset da instrução)
    registers = {
        "CS": cs_selector,
        "DS": ds_selector,
        "SS": ss_selector,
        "EIP": hex(instr_offset),
        "ESI": hex(op1_offset),
        "EDI": hex(op2_offset)
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução XCHG")
    print("==============================================\n")
    
    # -- Etapa 1: Busca da Instrução --
    print("Etapa 1: Busca da Instrução")
    # Calcula o endereço linear da instrução: CS_base + offset da instrução
    linear_address_instr = code_base + instr_offset
    print(f"   -> Offset da instrução (EIP): {instr_offset_str}")
    print(f"   -> Cálculo do endereço LINEAR: {hex(code_base)} (CS_base) + {hex(instr_offset)} = {hex(linear_address_instr)}")
    
    # Verifica se o endereço linear está dentro do segmento de código
    if linear_address_instr < code_base or linear_address_instr > code_limit:
        print("   -> GPF: Endereço de instrução fora do limite do segmento de código!")
        return

    print("   -> Barramento utilizado: Address Bus (busca do endereço) e Data Bus (transferência da instrução)")
    print(f"   -> Registradores: CS = {cs_selector} | EIP = {hex(instr_offset)}")
    print("-" * 60)
    
    # -- Etapa 2: Busca dos Operandos (OP1 e OP2) --
    print("Etapa 2: Busca dos Operandos")
    # Calcula os endereços lineares dos operandos no segmento de dados
    linear_address_op1 = data_base + op1_offset
    linear_address_op2 = data_base + op2_offset

    print(f"   -> Operando OP1:")
    print(f"      - Offset da memória (ESI): {op1_offset_str}")
    print(f"      - Endereço LINEAR: {hex(data_base)} (DS_base) + {hex(op1_offset)} = {hex(linear_address_op1)}")
    if linear_address_op1 < data_base or linear_address_op1 > data_limit:
        print("   -> GPF: Endereço do operando OP1 fora do limite do segmento de dados!")
        return

    print(f"   -> Operando OP2:")
    print(f"      - Offset da memória (EDI): {op2_offset_str}")
    print(f"      - Endereço LINEAR: {hex(data_base)} (DS_base) + {hex(op2_offset)} = {hex(linear_address_op2)}")
    if linear_address_op2 < data_base or linear_address_op2 > data_limit:
        print("   -> GPF: Endereço do operando OP2 fora do limite do segmento de dados!")
        return

    print("   -> Barramento utilizado: Address Bus (busca dos endereços) e Data Bus (transferência dos operandos)")
    print(f"   -> Registrador DS = {ds_selector}")
    print("-" * 60)
    
    # -- Etapa 3: Execução da XCHG --
    print("Etapa 3: Execução da Instrução XCHG")
    print(f"   -> Operação: XCHG [DS:{op1_offset_str}], [DS:{op2_offset_str}]")
    
    # Simula a busca dos valores armazenados nos operandos OP1 e OP2.
    op1_data_value = input("   - Informe o valor armazenado em OP1 (ex: 0x12345678): ").strip()
    op2_data_value = input("   - Informe o valor armazenado em OP2 (ex: 0x87654321): ").strip()
    
    print(f"   -> Trocando os valores {op1_data_value} (OP1) e {op2_data_value} (OP2)")
    
    # Simula a troca dos valores
    temp = op1_data_value
    op1_data_value = op2_data_value
    op2_data_value = temp
    
    # Atualiza os valores nos registradores
    registers["OP1"] = op1_data_value
    registers["OP2"] = op2_data_value
    
    print("   -> Operação interna: Troca dos valores entre OP1 e OP2")
    print("-" * 60)
    
    # -- Etapa 4: Estado Final dos Registradores --
    print("Estado final dos Registradores:")
    for reg, valor in registers.items():
        print(f"   {reg}: {valor}")
    
    print("\n==============================================")
    print("Fim da Simulação.")