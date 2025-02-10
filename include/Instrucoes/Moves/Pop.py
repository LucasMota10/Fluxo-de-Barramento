def POP(code_base, code_limit, stack_base, stack_limit, cs_selector, ss_selector):
    print("\nPara a instrução POP, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> POP <DESTINO>")
    print("Exemplo: 00024000 POP EAX")
    instr_input = input("   - Instrução: ").strip()

    try:
        # Separa os componentes da entrada
        partes = instr_input.split()
        if len(partes) != 3:
            raise ValueError("Formato inválido. É esperado 3 elementos separados por espaços.")

        # O primeiro elemento é o offset da instrução (EIP)
        instr_offset_str = partes[0]
        # O segundo deve ser o mnemônico (POP)
        mnemonic = partes[1].upper()
        if mnemonic != "POP":
            print("Erro: Instrução Inválida")
            return

        # O terceiro elemento é o registrador de destino
        destino = partes[2].upper()

        # Converte o offset da instrução para inteiro
        instr_offset = int(instr_offset_str, 16)
    except ValueError as ve:
        print("Erro ao interpretar a entrada. Certifique-se de usar o formato hexadecimal correto.")
        print("Detalhe:", ve)
        return

    # Inicializa os registradores
    registers = {
        "CS": cs_selector,
        "SS": ss_selector,
        "EIP": hex(instr_offset),
        "ESP": hex(stack_limit - 4),  # Inicializa ESP no limite superior da pilha - 4 (último valor empurrado)
        destino: "0x00000000",  # Inicializa o registrador de destino
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução POP")
    print("==============================================\n")

    # -- Etapa 1: Busca da Instrução --
    print("Etapa 1: Busca da Instrução")
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

    # -- Etapa 2: Execução da POP --
    print("Etapa 2: Execução da Instrução POP")
    # Recupera o valor do topo da pilha
    esp_value = int(registers["ESP"], 16)
    linear_address_stack = stack_base + (esp_value - stack_base)
    print(f"   -> Endereço LINEAR na pilha: {hex(stack_base)} (SS_base) + {hex(esp_value - stack_base)} = {hex(linear_address_stack)}")

    # Verifica se o endereço está dentro do limite da pilha
    if esp_value < stack_base or esp_value > stack_limit:
        print("   -> GPF: Endereço fora do limite do segmento de pilha!")
        return

    # Simula a leitura do valor da pilha
    valor_pilha = input(f"   - Informe o valor armazenado no topo da pilha (ex: 0x12345678): ").strip()
    registers[destino] = valor_pilha

    # Incrementa ESP (pilha cresce para baixo)
    registers["ESP"] = hex(esp_value + 4)
    print(f"   -> Valor recuperado da pilha: {valor_pilha}")
    print(f"   -> Registrador {destino} atualizado: {valor_pilha}")
    print(f"   -> Registrador ESP atualizado: {hex(esp_value + 4)}")
    print("-" * 60)

    # -- Etapa 3: Estado Final dos Registradores --
    print("Estado final dos Registradores:")
    for reg, valor_reg in registers.items():
        print(f"   {reg}: {valor_reg}")

    print("\n==============================================")
    print("Fim da Simulação.")