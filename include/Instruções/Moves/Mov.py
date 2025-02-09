"""
Simulação de uma instrução MOV em modo Protegido (32 bits)
Inclui verificação dos endereços lineares:
    - Se o endereço calculado estiver fora do intervalo do segmento,
      cancela a operação e informa a ocorrência de GPF.
"""
def MOV(code_base, code_limit, data_base, data_limit, cs_selector, ds_selector, ss_selector):
    print("\nPara a instrução MOV, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> MOV <DST_OFFSET>, <SRC_OFFSET>")
    print("Exemplo: 00024000 MOV 00040000 00081B10")
    instr_input = input("   - Instrução: ").strip()

    # Tenta separar os componentes da linha de comando.
    try:
        # Exemplo de entrada: "00024000 MOV 00040000 00081B10"
        # Primeiro separamos por espaços:
        partes = instr_input.split()
        if len(partes) != 4:
            raise ValueError("Formato inválido. É esperado 4 elementos separados por espaços.")

        # O primeiro elemento é o offset da instrução (EIP)
        instr_offset_str = partes[0]
        # O segundo deve ser o mnemônico (MOV)
        mnemonic = partes[1].upper()
        if mnemonic != "MOV":
            print("Erro: Instrução Inválida")
            return

        # O terceiro elemento contém o offset DST com uma vírgula no final (opcional)
        dst_offset_str = partes[2].replace(",", "")
        # O quarto elemento é o offset SRC
        src_offset_str = partes[3]

        # Converte as strings em inteiros (base 16)
        instr_offset = int(instr_offset_str, 16)
        dst_offset   = int(dst_offset_str, 16)
        src_offset   = int(src_offset_str, 16)
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
        "ESI": hex(src_offset),
        "EDI": hex(dst_offset)
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução MOV")
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
    
    # -- Etapa 2: Busca dos Operandos (DST e SRC) --
    print("Etapa 2: Busca dos Operandos")
    # Calcula os endereços lineares dos operandos no segmento de dados
    linear_address_dst = data_base + dst_offset
    linear_address_src = data_base + src_offset

    print(f"   -> Operando DST:")
    print(f"      - Offset da memória (ESI): {dst_offset_str}")
    print(f"      - Endereço LINEAR: {hex(data_base)} (DS_base) + {hex(dst_offset)} = {hex(linear_address_dst)}")
    print(f"      - O valor passa a ser armazenado em (EDI)")
    if linear_address_dst < data_base or linear_address_dst > data_limit:
        print("   -> GPF: Endereço do operando DST fora do limite do segmento de dados!")
        return

    print(f"   -> Operando SRC:")
    print(f"      - Offset da memória (ESI): {src_offset_str}")
    print(f"      - Endereço LINEAR: {hex(data_base)} (DS_base) + {hex(src_offset)} = {hex(linear_address_src)}")
    if linear_address_src < data_base or linear_address_src > data_limit:
        print("   -> GPF: Endereço do operando SRC fora do limite do segmento de dados!")
        return

    print("   -> Barramento utilizado: Address Bus (busca dos endereços) e Data Bus (transferência dos operandos)")
    print(f"   -> Registrador DS = {ds_selector}")
    print("-" * 60)
    
    # -- Etapa 3: Execução da MOV --
    print("Etapa 3: Execução da Instrução MOV")
    print(f"   -> Operação: MOV [DS:{dst_offset_str}], [DS:{src_offset_str}]")
    # Simula a busca do valor armazenado no operando SRC.
    src_data_value = input("   - Informe o valor armazenado em SRC (ex: 0x12345678): ").strip()
    
    print(f"   -> Transferindo o dado {src_data_value} do endereço SRC para o endereço DST")
    # Como não há uma memória real, usamos o dicionário de registradores para ilustrar o resultado.
    registers["DST"] = src_data_value
    print("   -> Operação interna: Atualização do conteúdo em DST")
    print("-" * 60)
    
    # -- Etapa 4: Estado Final dos Registradores --
    print("Estado final dos Registradores:")
    for reg, valor in registers.items():
        print(f"   {reg}: {valor}")
    
    print("\n==============================================")
    print("Fim da Simulação.")