def PUSH(code_base, code_limit, stack_base, stack_limit, cs_selector, ss_selector):
    print("\nPara a instrução PUSH, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> PUSH <VALOR>")
    print("Exemplo: 00024000 PUSH 0x12345678")
    instr_input = input("   - Instrução: ").strip()

    try:
        # Separa os componentes da entrada
        partes = instr_input.split()
        if len(partes) != 3:
            raise ValueError("Formato inválido. É esperado 3 elementos separados por espaços.")

        # O primeiro elemento é o offset da instrução (EIP)
        instr_offset_str = partes[0]
        # O segundo deve ser o mnemônico (PUSH)
        mnemonic = partes[1].upper()
        if mnemonic != "PUSH":
            print("Erro: Instrução Inválida")
            return

        # O terceiro elemento é o valor a ser empurrado para a pilha
        valor_str = partes[2]
        valor = int(valor_str, 16)  # Converte para inteiro (base 16)

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
        "ESP": hex(stack_limit),  # Inicializa ESP no limite superior da pilha
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução PUSH")
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

    # -- Etapa 2: Execução da PUSH --
    print("Etapa 2: Execução da Instrução PUSH")
    # Decrementa ESP (pilha cresce para baixo)
    esp_value = int(registers["ESP"], 16) - 4
    if esp_value < stack_base:
        print("   -> GPF: Estouro da pilha! Endereço fora do limite do segmento de pilha.")
        return

    # Atualiza ESP
    registers["ESP"] = hex(esp_value)

    # Calcula o endereço linear na pilha
    linear_address_stack = stack_base + (esp_value - stack_base)
    print(f"   -> Endereço LINEAR na pilha: {hex(stack_base)} (SS_base) + {hex(esp_value - stack_base)} = {hex(linear_address_stack)}")
    print(f"   -> Valor empurrado para a pilha: {hex(valor)}")
    print("   -> Barramento utilizado: Address Bus (busca do endereço) e Data Bus (transferência do valor)")
    print(f"   -> Registrador ESP atualizado: {hex(esp_value)}")
    print("-" * 60)

    # -- Etapa 3: Estado Final dos Registradores --
    print("Estado final dos Registradores:")
    for reg, valor_reg in registers.items():
        print(f"   {reg}: {valor_reg}")

    print("\n==============================================")
    print("Fim da Simulação.")