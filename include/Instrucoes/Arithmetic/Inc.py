def INC(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector):
    """
    Simulação de uma instrução INC em modo Protegido (32 bits).
    Inclui verificação dos endereços lineares:
        - Se o endereço calculado estiver fora do intervalo do segmento,
          cancela a operação e informa a ocorrência de GPF.
    """
    print("\nPara a instrução INC, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> INC <DST_OFFSET>")
    print("Exemplo: 00024000 INC 00040000")
    instr_input = input("   - Instrução: ").strip()

    # Tenta separar os componentes da linha de comando.
    try:
        # Exemplo de entrada: "00024000 INC 00040000"
        # Primeiro separamos por espaços:
        partes = instr_input.split()
        if len(partes) != 3:
            raise ValueError("Formato inválido. É esperado 3 elementos separados por espaços.")

        # O primeiro elemento é o offset da instrução (EIP)
        instr_offset_str = partes[0]
        # O segundo deve ser o mnemônico (INC)
        mnemonic = partes[1].upper()
        if mnemonic != "INC":
            print("Erro: Instrução Inválida")
            return

        # O terceiro elemento é o offset DST
        dst_offset_str = partes[2]

        # Converte as strings em inteiros (base 16)
        instr_offset = int(instr_offset_str, 16)
        dst_offset   = int(dst_offset_str, 16)
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
        "DST": hex(dst_offset),
        "EFLAGS": {"ZF": 0, "SF": 0, "OF": 0}  # Flags relevantes para a operação INC
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução INC")
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
    
    # -- Etapa 2: Busca do Operando DST --
    print("Etapa 2: Busca do Operando DST")
    # Calcula o endereço linear do operando no segmento de dados
    linear_address_dst = data_base + dst_offset

    print(f"   -> Operando DST:")
    print(f"      - Offset da memória: {dst_offset_str}")
    print(f"      - Endereço LINEAR: {hex(data_base)} (DS_base) + {hex(dst_offset)} = {hex(linear_address_dst)}")
    if linear_address_dst < data_base or linear_address_dst > data_limit:
        print("   -> GPF: Endereço do operando DST fora do limite do segmento de dados!")
        return

    print("   -> Barramento utilizado: Address Bus (busca do endereço) e Data Bus (transferência do operando)")
    print(f"   -> Registrador DS = {ds_selector}")
    print("-" * 60)
    
    # -- Etapa 3: Captura do Valor do Operando DST --
    print("Etapa 3: Captura do Valor do Operando DST")
    dst_data_value = int(input("   - Informe o valor armazenado em DST (ex: 0x12345678): "), 16)
    
    # -- Etapa 4: Execução da Instrução INC --
    print("\nEtapa 4: Execução da Instrução INC")
    resultado = dst_data_value + 1  # Incrementa o valor em 1
    
    # Atualiza as flags com base no resultado do incremento
    registers["EFLAGS"]["ZF"] = 1 if resultado == 0 else 0  # ZF = 1 se o resultado for zero
    registers["EFLAGS"]["SF"] = 1 if resultado < 0 else 0  # SF = 1 se o resultado for negativo
    
    print(f"   -> Resultado do Incremento: {hex(resultado)}")
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