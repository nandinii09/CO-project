import sys

op_code = {
    'add': '00000',
    'sub': '00001',
    'movb': '00010',  # ok
    'movc': '00011',
    'ld': '00100',
    'st': '00101',  # ok
    'mul': '00110',
    'div': '00111',
    'rs': '01000',
    'ls': '01001',
    'xor': '01010',
    'or': '01011',
    'and': '01100',
    'not': '01101',
    'cmp': '01110',
    'jmp': '01111',
    'jlt': '11100',
    'jgt': '11101',
    'je': '11111',
    'hlt': '11010',  # ok
    'clear': '10011',
    'incr': '11000',
    'decr': '10110',
    'swap': '10101'
}

op_type = {
    "A": ['add', 'sub', 'mul', 'xor', 'or', 'and'],
    "B": ['movb', 'rs', 'ls'],
    "C": ['movc', 'div', 'not', 'cmp','swap'],
    "D": ['ld', 'st'],
    "E": ['jmp', 'jlt', 'jgt', 'je'],
    "F": ['hlt'],
    "G": ['clear', 'incr', 'decr']
}

reg = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111'
}

initial_reg1 = {
    'R0': '0',
    'R1': '0',
    'R2': '0',
    'R3': '0',
    'R4': '0',
    'R5': '0',
    'R6': '0',
}
initial_reg = {
    'R0': '0' * 16,
    'R1': '0' * 16,
    'R2': '0' * 16,
    'R3': '0' * 16,
    'R4': '0' * 16,
    'R5': '0' * 16,
    'R6': '0' * 16,
    'FLAGS': '0' * 16,
}
flagreg = ['0'] * 16


def bin_to_decimal(n):
    return int(n, 2)


def dec_to_bin(val):
    binary = bin(int(val))[2:]
    c = ('0' * (16 - len(binary)) + binary)
    return ('0' * (16 - len(binary)) + binary)


def execute(i, instruction, name, type):
    global temp_i
    flag = True
    if type == "A":
        for x, y in reg.items():
            if y == instruction[7:10]:
                reg1 = x
            if y == instruction[10:13]:
                reg2 = x
            if y == instruction[13::]:
                reg3 = x
        if name == "add":
            if (bin_to_decimal(str(initial_reg[reg2])) + bin_to_decimal(str(initial_reg[reg3]))) > ((2 ** 16) - 1):
                initial_reg[reg1] = (bin_to_decimal(str(initial_reg[reg2])) + bin_to_decimal(
                    str(initial_reg[reg3]))) % (2 ** 16)
                flagreg[-4] = '1'
                initial_reg['FLAGS'] = "".join(flagreg)
            else:
                initial_reg[reg1] = dec_to_bin(int(initial_reg[reg2], 2) + int(initial_reg[reg3], 2))

        if name == "sub":
            if bin_to_decimal(bin(int(initial_reg[reg2], 2) - int(initial_reg[reg3], 2))) < 0:
                initial_reg[reg1] = 0
                flagreg[-4] = '1'
                initial_reg['FLAGS'] = "".join(flagreg)
            else:
                initial_reg[reg1] = dec_to_bin(int(initial_reg[reg2], 2) - int(initial_reg[reg3], 2))

        if name == "mul":
            if int(initial_reg[reg2], 2) * int(initial_reg[reg3]) > ((2 ** 16) - 1):
                initial_reg[reg1] = bin(int(initial_reg[reg2], 2) * int(initial_reg[reg3], 2)) % 2 ** 16
                flagreg[-4] = '1'
                initial_reg['FLAGS'] = "".join(flagreg)
            else:
                initial_reg[reg1] = bin(int(initial_reg[reg2], 2) * int(initial_reg[reg3], 2))

        if name == "or":
            initial_reg[reg1] = bin(int(initial_reg[reg2], 2) | int(initial_reg[reg3], 2))
        if name == "and":
            initial_reg[reg1] = bin(int(initial_reg[reg2], 2) & int(initial_reg[reg3], 2))
        if name == "xor":
            initial_reg[reg1] = bin(int(initial_reg[reg2], 2) ^ int(initial_reg[reg3], 2))

    if type == "B":
        for x, y in reg.items():
            if y == instruction[6:9]:
                reg_name = x
        imm = instruction[9::]
        if name == "movb":  # checked
            initial_reg[reg_name] = '0' * 9 + imm
        elif name == "rs":
            initial_reg[reg_name] = initial_reg[reg_name] >> imm
        elif name == "ls":
            initial_reg[reg_name] = initial_reg[reg_name] << imm

    if type == "C":
        for x, y in reg.items():
            if y == instruction[10:13]:
                reg1 = x
            if y == instruction[13::]:
                reg2 = x
        if name == "movc":
            initial_reg[reg1] = initial_reg[reg2]
        elif name == "div":
            initial_reg['R0'] = initial_reg[reg1] // initial_reg[reg2]
            initial_reg['R1'] = initial_reg[reg1] % initial_reg[reg2]
            if (initial_reg[reg2]) == '0':
                flagreg[-4] = '1'
                initial_reg['R0'] = '0'
                initial_reg['R1'] = '0'
        elif name == "not":
            value = initial_reg[reg2]
            value = bin_to_decimal(value)
            initial_reg[reg1] = (~value)
        elif name == "cmp":  # checked
            r1 = bin_to_decimal(initial_reg[reg1])
            r2 = bin_to_decimal(initial_reg[reg2])
            if (r1 == r2):
                flagreg[-1] = '1'
                initial_reg['FLAGS'] = "".join(flagreg)
            elif (r1 < r2):
                flagreg[-3] = '1'
                initial_reg['FLAGS'] = "".join(flagreg)
            elif (r1 > r2):
                flagreg[-2] = '1'
                initial_reg['FLAGS'] = "".join(flagreg)
        elif name=='swap':
            temp_reg = initial_reg.get(reg1)
            initial_reg[reg1] = initial_reg.get(reg2)
            initial_reg[reg2] = temp_reg

    if type == "D":
        for x, y in reg.items():
            if y == instruction[6:9]:
                reg_name = x
        if name == "st":  # checked
            memory[bin_to_decimal(instruction[-7::])] = (
            initial_reg[reg_name])  # stores value in reg in memory at imm value index
        elif name == "ld":  # checked
            initial_reg[reg_name] = memory[bin_to_decimal(instruction[9:16])]
    if type == 'E':  # "E": ['jmp', 'jlt', 'jgt', 'je'],
        flag = False
        if name == 'jmp':
            i1 = bin_to_decimal(instruction[-7:])
        elif (name == 'jlt' and initial_reg['FLAGS'][-3]) == '1':
            i1 = bin_to_decimal(instruction[-7:])
        elif (name == 'jgt' and initial_reg['FLAGS'][-2]) == '1':
            i1 = bin_to_decimal(instruction[-7:])
        if (name == 'je' and initial_reg['FLAGS'][-1] == '1'):
            i1 = bin_to_decimal(instruction[-7:])
    if type == 'G':
        for x, y in reg.items():
            if y == instruction[13:]:
                reg_name = x
        if name == "clear":
            initial_reg[reg_name] = '0' * 16
        elif name == "set":
            initial_reg[reg_name] = '1' * 16
        val = bin_to_decimal(initial_reg.get(reg_name))
        if name == "incr":
            if val <= 126:
                initial_reg[reg_name] = dec_to_bin(str(val + 1))
            else:
                initial_reg[reg_name] = "0" * 16
        elif name == "decr":
            if val > 0:
                initial_reg[reg_name] = dec_to_bin(str(val - 1))
            else:
                initial_reg[reg_name] ="1"*16




    temp_i = str(i)
    if not (flag):
        try:
            i = i1 - 1
            flag = not flag
        except:
            pass
    if inst_name == 'cmp':
        print((dec_to_bin(temp_i))[-7:], "      ", initial_reg['R0'], initial_reg['R1'], initial_reg['R2'],
              initial_reg['R3'], initial_reg['R4'], initial_reg['R5'], initial_reg['R6'], initial_reg['FLAGS'])
    else:
        print((dec_to_bin(temp_i))[-7:], "      ", initial_reg['R0'], initial_reg['R1'], initial_reg['R2'],
              initial_reg['R3'], initial_reg['R4'], initial_reg['R5'], initial_reg['R6'], '0' * 16)
    i += 1
    return i


# main
memory = []
file = ""
line = ""

f = open('input.txt', 'r')
file = f.read()
# while True:
#     line = sys.stdin.readline().strip()
#     if not line:
#         break
#     file += line + "\n"

lines = [x.rstrip().lstrip() for x in file.split("\n") if x != '']
memory.extend(lines)
zeros = '0' * 16
for i in range(len(lines), 128):
    memory.append(zeros)

temp_i = 0
halted = False
i = 0

while (not halted):
    instruction = lines[i]
    for name, opcode in op_code.items():
        if instruction[:5] == opcode:
            inst_name = name
    for type, list in op_type.items():
        if inst_name in list:
            inst_type = type
    # print(inst_type, inst_name)
    if inst_type == "F":
        halted = True
    i = execute(i, instruction, inst_name, inst_type)

for i in range(0, 128):
    print(memory[i])
