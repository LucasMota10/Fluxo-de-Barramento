def JMP(code_base, code_limit, cs_selector):
    """
    Simulação de uma instrução JMP em modo Protegido (32 bits).
    Inclui verificação dos endereços lineares:
        - Se o endereço calculado estiver fora do intervalo do segmento,
          cancela a operação e informa a ocorrência de GPF.
    """
    print("\nPara a instrução JMP, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> JMP <ADDR_OFFSET>")
    print("Exemplo: 00024000 JMP 00040000")
    instr_input = input("   - Instrução: ").strip()

    # Tenta separar os componentes da linha de comando.
    try:
        # Exemplo de entrada: "00024000 JMP 00040000"
        # Primeiro separamos por espaços:
        partes = instr_input.split()
        if len(partes) != 3:
            raise ValueError("Formato inválido. É esperado 3 elementos separados por espaços.")

        # O primeiro elemento é o offset da instrução (EIP)
        instr_offset_str = partes[0]
        # O segundo deve ser o mnemônico (JMP)
        mnemonic = partes[1].upper()
        if mnemonic != "JMP":
            print("Erro: Instrução Inválida")
            return

        # O terceiro elemento é o offset do endereço de destino
        addr_offset_str = partes[2]

        # Converte as strings em inteiros (base 16)
        instr_offset = int(instr_offset_str, 16)
        addr_offset  = int(addr_offset_str, 16)
    except ValueError as ve:
        print("Erro ao interpretar a entrada. Certifique-se de usar o formato hexadecimal correto.")
        print("Detalhe:", ve)
        return

    # Inicializa os registradores (incluindo EIP com o offset da instrução)
    registers = {
        "CS": cs_selector,
        "EIP": hex(instr_offset),
        "ADDR": hex(addr_offset)
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução JMP")
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
    
    # -- Etapa 2: Verificação do Endereço de Destino --
    print("Etapa 2: Verificação do Endereço de Destino")
    # Calcula o endereço linear do destino: CS_base + offset do destino
    linear_address_dest = code_base + addr_offset

    print(f"   -> Endereço de Destino:")
    print(f"      - Offset do destino: {addr_offset_str}")
    print(f"      - Endereço LINEAR: {hex(code_base)} (CS_base) + {hex(addr_offset)} = {hex(linear_address_dest)}")
    
    # Verifica se o endereço de destino está dentro do segmento de código
    if linear_address_dest < code_base or linear_address_dest > code_limit:
        print("   -> GPF: Endereço de destino fora do limite do segmento de código!")
        return

    print("   -> Barramento utilizado: Address Bus (busca do endereço) e Data Bus (transferência do endereço de destino)")
    print(f"   -> Registrador CS = {cs_selector}")
    print("-" * 60)
    
    # -- Etapa 3: Execução da Instrução JMP --
    print("Etapa 3: Execução da Instrução JMP")
    print(f"   -> Operação: JMP {hex(addr_offset)}")
    print(f"   -> Atualizando EIP para o endereço de destino: {hex(addr_offset)}")
    
    # Atualiza o registrador EIP com o endereço de destino
    registers["EIP"] = hex(addr_offset)
    
    print("-" * 60)
    
    # -- Etapa 4: Estado Final dos Registradores --
    print("Estado final dos Registradores:")
    for reg, valor in registers.items():
        print(f"   {reg}: {valor}")
    
    print("\n==============================================")
    print("Fim da Simulação.")