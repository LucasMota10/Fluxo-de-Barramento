def CMP(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector):
    """
    Simulação de uma instrução CMP em modo Protegido (32 bits).
    Inclui verificação dos endereços lineares:
        - Se o endereço calculado estiver fora do intervalo do segmento,
          cancela a operação e informa a ocorrência de GPF.
    """
    print("\nPara a instrução CMP, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> CMP <SRC1_OFFSET>, <SRC2_OFFSET>")
    print("Exemplo: 00024000 CMP 00040000 00081B10")
    instr_input = input("   - Instrução: ").strip()

    # Tenta separar os componentes da linha de comando.
    try:
        # Exemplo de entrada: "00024000 CMP 00040000 00081B10"
        # Primeiro separamos por espaços:
        partes = instr_input.split()
        if len(partes) != 4:
            raise ValueError("Formato inválido. É esperado 4 elementos separados por espaços.")

        # O primeiro elemento é o offset da instrução (EIP)
        instr_offset_str = partes[0]
        # O segundo deve ser o mnemônico (CMP)
        mnemonic = partes[1].upper()
        if mnemonic != "CMP":
            print("Erro: Instrução Inválida")
            return

        # O terceiro elemento contém o offset SRC1 com uma vírgula no final (opcional)
        src1_offset_str = partes[2].replace(",", "")
        # O quarto elemento é o offset SRC2
        src2_offset_str = partes[3]

        # Converte as strings em inteiros (base 16)
        instr_offset = int(instr_offset_str, 16)
        src1_offset  = int(src1_offset_str, 16)
        src2_offset  = int(src2_offset_str, 16)
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
        "SRC1": hex(src1_offset),
        "SRC2": hex(src2_offset),
        "EFLAGS": {"ZF": 0, "SF": 0, "OF": 0}  # Flags relevantes para a operação CMP
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução CMP")
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
    
    # -- Etapa 2: Busca dos Operandos (SRC1 e SRC2) --
    print("Etapa 2: Busca dos Operandos")
    # Calcula os endereços lineares dos operandos no segmento de dados
    linear_address_src1 = data_base + src1_offset
    linear_address_src2 = data_base + src2_offset

    print(f"   -> Operando SRC1:")
    print(f"      - Offset da memória: {src1_offset_str}")
    print(f"      - Endereço LINEAR: {hex(data_base)} (DS_base) + {hex(src1_offset)} = {hex(linear_address_src1)}")
    if linear_address_src1 < data_base or linear_address_src1 > data_limit:
        print("   -> GPF: Endereço do operando SRC1 fora do limite do segmento de dados!")
        return

    print(f"   -> Operando SRC2:")
    print(f"      - Offset da memória: {src2_offset_str}")
    print(f"      - Endereço LINEAR: {hex(data_base)} (DS_base) + {hex(src2_offset)} = {hex(linear_address_src2)}")
    if linear_address_src2 < data_base or linear_address_src2 > data_limit:
        print("   -> GPF: Endereço do operando SRC2 fora do limite do segmento de dados!")
        return

    print("   -> Barramento utilizado: Address Bus (busca dos endereços) e Data Bus (transferência dos operandos)")
    print(f"   -> Registrador DS = {ds_selector}")
    print("-" * 60)
    
    # -- Etapa 3: Captura dos Valores dos Operandos --
    print("Etapa 3: Captura dos Valores dos Operandos")
    print(f"   -> Operação: CMP [DS:{src1_offset_str}], [DS:{src2_offset_str}]")
    src1_data_value = int(input("   - Informe o valor armazenado em SRC1 (ex: 0x12345678): "), 16)
    src2_data_value = int(input("   - Informe o valor armazenado em SRC2 (ex: 0x87654321): "), 16)
    
    # -- Etapa 4: Execução da Instrução CMP --
    print("\nEtapa 4: Execução da Instrução CMP")
    resultado = src1_data_value - src2_data_value
    
    # Atualiza as flags com base no resultado da subtração
    registers["EFLAGS"]["ZF"] = 1 if resultado == 0 else 0  # ZF = 1 se os valores forem iguais
    registers["EFLAGS"]["SF"] = 1 if resultado < 0 else 0  # SF = 1 se SRC1 for menor que SRC2
    
    print(f"   -> Resultado da Subtração: {hex(resultado)}")
    print("   -> Flags atualizados:")
    print(f"      ZF (Zero Flag): {registers['EFLAGS']['ZF']}")
    print(f"      SF (Sign Flag): {registers['EFLAGS']['SF']}")
    print("-" * 60)
    
    # -- Etapa 5: Estado Final dos Registradores --
    print("Estado final dos Registradores:")
    for reg, valor in registers.items():
        if reg == "EFLAGS":
            print(f"   {reg}:")
            for flag, val in valor.items():
                print(f"      {flag}: {val}")
        else:
            print(f"   {reg}: {valor}")
    
    print("\n==============================================")
    print("Fim da Simulação.")