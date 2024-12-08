import sys
import os
import re

if (len(sys.argv) > 2):
    raise ValueError("Too many parameters")
if (len(sys.argv) == 1):
    raise ValueError("Excepted .asm filename")
if (not re.match(r".*\.asm", sys.argv[1])):
    raise ValueError(f"{sys.argv[1]} is not valid filename")
if (not os.path.exists(sys.argv[1])):
    raise ValueError(f"{sys.argv[1]} not found")

with open(sys.argv[1], "r") as asm_file:
    asm_with_labels = list(
        filter(lambda line: len(line) > 0,
               map(lambda line: line.strip().replace(" ", "").split("//")[0],
                   asm_file.readlines())))

labels: dict[str, int] = {
    "SP": 0x0000,
    "LCL": 0x0001,
    "ARG": 0x0002,
    "THIS": 0x0003,
    "THAT": 0x0004,
    **{f"R{i}": i for i in range(16)},
    "SCREEN": 0x4000,
    "KBD": 0x6000
}
variables: dict[str, int] = {}

for i, command in enumerate(asm_with_labels):
    if (bool(re.match(r"^\(.+\)$", command))):
        labels[command[1:-1]] = -1
    else:
        for k in labels.keys():
            if (labels[k] == -1):
                labels[k] = i-len(labels.keys())+7+16

asm = list(filter(lambda c: not bool(
    re.match(r"^\(.+\)$", command)), asm_with_labels))

jumps: dict[str, int] = {
    "JGT": 0b001,
    "JEQ": 0b010,
    "JGE": 0b011,
    "JLT": 0b100,
    "JNE": 0b101,
    "JLE": 0b110,
    "JMP": 0b111,
}
expressions: dict[str, int] = {
    "0": 0b101010,
    "1": 0b111111,
    "-1": 0b111010,
    "D": 0b001100,
    "A": 0b110000,
    "!D": 0b001101,
    "!A": 0b110001,
    "-D": 0b001111,
    "-A": 0b110011,
    "D+1": 0b011111,
    "A+1": 0b110111,
    "D-1": 0b001110,
    "A-1": 0b110010,
    "D+A": 0b000010,
    "D-A": 0b010011,
    "A-D": 0b000111,
    "D&A": 0b000000,
    "D|A": 0b010101,
}


hack: list[str] = []

for command in asm:
    if (command[0] == "@"):
        if (command[1:].isnumeric()):
            hack.append(bin(int(command[1:]))[2:].zfill(16))
        else:
            if (command[1:] in labels.keys()):
                hack.append(bin(labels[command[1:]])[2:].zfill(16))
            else:
                if (not (command[1:] in variables.keys())):
                    variables[command[1:]] = \
                        max(list(filter(lambda address: address >= 15 and address < 0x4000,
                                        [15, *variables.values()])))+1
                hack.append(bin(variables[command[1:]])[2:].zfill(16))
    else:
        memory, compute, destination, jump = 0, 0, 0, 0
        if (";" in command):
            jump = jumps[command[command.find(";")+1:]]
            command = command[:command.find(";")]
        if ("=" in command):
            destinations = command[:command.find("=")]
            if ("M" in destinations):
                destination += 0b001
            if ("D" in destinations):
                destination += 0b010
            if ("A" in destinations):
                destination += 0b100
            command = command[command.find("=")+1:]
        if ("M" in command):
            memory = 1
            command = command.replace("M", "A")
        compute = expressions[command]
        bin_code = 0b111_0_000000_000_000
        bin_code |= memory << 12
        bin_code |= compute << 6
        bin_code |= destination << 3
        bin_code |= jump
        hack.append(bin(bin_code)[2:].zfill(16))

with open(sys.argv[1].replace(".asm", ".hack"), "w") as hack_file:
    for i, command in enumerate(hack):
        hack_file.write(f"{command}")
        if (i != len(hack)-1):
            hack_file.write("\n")
