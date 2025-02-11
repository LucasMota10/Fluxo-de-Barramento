def XOR(code_base, code_limit, cs_selector):

    print("\nPara a instrução XOR, informe a instrução completa no formato:")
    print("   <OFFSET_INSTRUÇÃO> XOR <OPERANDO1> <OPERANDO2>")
    print("Exemplo: 00024000 XOR EAX EBX")
    instr_input = input("   - Instrução: ").strip()

    try:
        
        partes = instr_input.split()
        if len(partes) != 4:
            raise ValueError("Formato inválido. É esperado 4 elementos separados por espaços.")

        instr_offset_str = partes[0]
        mnemonic = partes[1].upper()
        if mnemonic != "XOR":
            print("Erro: Instrução Inválida")
            return

        operando1 = partes[2].upper()
        operando2 = partes[3].upper()

        instr_offset = int(instr_offset_str, 16)
    except ValueError as ve:
        print("Erro ao interpretar a entrada. Certifique-se de usar o formato hexadecimal correto.")
        print("Detalhe:", ve)
        return

    eax_value = int(input("Informe o valor do registrador EAX (em hexadecimal, ex: A): "), 16)
    ebx_value = int(input("Informe o valor do registrador EBX (em hexadecimal, ex: C): "), 16)    

    registers = {
        "CS": cs_selector,
        "EIP": hex(instr_offset),
        "EAX": hex(eax_value),
        "EBX": hex(ebx_value),
        "OPERANDO1": operando1,
        "OPERANDO2": operando2
    }

    print("\n==============================================")
    print("Simulação da Execução da Instrução XOR")
    print("==============================================\n")

    print("Etapa 1: Busca da Instrução")
    
    linear_address_instr = code_base + instr_offset
    print(f"   -> Offset da instrução (EIP): {instr_offset_str}")
    print(f"   -> Cálculo do endereço LINEAR: {hex(code_base)} (CS_base) + {hex(instr_offset)} = {hex(linear_address_instr)}")

    if linear_address_instr < code_base or linear_address_instr > code_limit:
        print("   -> GPF: Endereço de instrução fora do limite do segmento de código!")
        return

    print("   -> Barramento utilizado: Address Bus (busca do endereço) e Data Bus (transferência da instrução)")
    print(f"   -> Registradores: CS = {hex(cs_selector)} | EIP = {hex(instr_offset)}")
    print("-" * 60)

    print("Etapa 2: Verificação dos Operandos")
   
    operandos_validos = {"EAX", "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ESP"}
    if operando1 not in operandos_validos or operando2 not in operandos_validos:
        print("   -> Erro: Operandos inválidos. Use apenas registradores de 32 bits.")
        return

    valor_operando1 = eax_value if operando1 == "EAX" else ebx_value
    valor_operando2 = eax_value if operando2 == "EAX" else ebx_value

    print(f"   -> Operando 1: {operando1} = {hex(valor_operando1)}")
    print(f"   -> Operando 2: {operando2} = {hex(valor_operando2)}")
    print("-" * 60)

    print("Etapa 3: Execução da Instrução XOR")
    
    resultado = valor_operando1 ^ valor_operando2

    if operando1 == "EAX":
        eax_value = resultado
    elif operando1 == "EBX":
        ebx_value = resultado

    print(f"   -> Resultado da operação XOR: {hex(resultado)}")
    print(f"   -> Novo valor de {operando1}: {hex(eax_value if operando1 == 'EAX' else ebx_value)}")
    print("-" * 60)

    print("Estado final dos Registradores:")
    registers["EAX"] = hex(eax_value)
    registers["EBX"] = hex(ebx_value)
    for reg, valor in registers.items():
        print(f"   {reg}: {valor}")

    print("\n==============================================")
    print("Fim da Simulação.")