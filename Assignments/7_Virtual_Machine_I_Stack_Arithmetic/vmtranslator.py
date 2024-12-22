from pathlib import Path
import sys
import os
import re
from typing import Callable, Literal

vm_code: list[str] = []
output_filename: str | None = None


def read_file(path: Path | str):
    with open(path, "r") as asm_file:
        vm_code.extend(list(
            filter(lambda line: len(line) > 0,
                   map(lambda line: " ".join(
                       list(filter(lambda x: x != "", line.strip().split(" ")))
                   ).split("//")[0],
                       asm_file.readlines()))))


if (len(sys.argv) == 1):
    raise ValueError("At least one .vm file was expected")
for i in range(1, len(sys.argv)):
    if (not os.path.exists(sys.argv[i])):
        raise ValueError(f"{sys.argv[i]} not found")
    if (output_filename is None):
        output_filename = \
            f"{sys.argv[i].replace(".vm", "").replace(
                "/", "").replace("\\", "").replace(".", "")}.asm"
    if (os.path.isdir(sys.argv[i])):
        for file in os.listdir(sys.argv[i]):
            if (not re.match(r".*\.vm", file)):
                print(f"Missing {file} because it's not a .vm file")
            else:
                read_file(Path() / sys.argv[i] / file)
    else:
        read_file(sys.argv[i])


ram_areas: dict[str, int] = {
    "REGISTERS": 0,
    "STATIC": 16,
    "STACK": 256,
    "HEAP": 2048,
    "I/O": 16384,
}


class MemorySegment:
    def __init__(self, address: str | int | None, type: Literal["pointer", "value", "constant"]):
        self.address = address
        self.type = type
        self.isPointer = type == "pointer"
        self.isConstant = type == "constant"


memory_segments: dict[str, MemorySegment] = {
    "argument": MemorySegment("ARG", "pointer"),
    "local": MemorySegment("LCL", "pointer"),
    "static": MemorySegment(ram_areas["STATIC"], "value"),
    "constant": MemorySegment(None, "constant"),
    "this": MemorySegment("THIS", "pointer"),
    "that": MemorySegment("THAT", "pointer"),
    "pointer": MemorySegment(3, "value"),
    "temp": MemorySegment(5, "value"),
}


def create_labels():
    labels = {"eq": 0, "gt": 0, "lt": 0}

    def label(key: str):
        labels[key] += 1
        return (f"{key}{labels[key]//2}" if (labels[key] % 2 == 1) else f"{key}{labels[key]//2-1}").upper()
    return label


label = create_labels()
stack_commands: dict[str, Callable[[], list[str]]] = {
    "add": lambda: ["@SP", "AM=M-1", "D=M", "A=A-1", "D=D+M", "M=D"],
    "sub": lambda: ["@SP", "AM=M-1", "D=-M", "A=A-1", "D=D+M", "M=D"],
    "neg": lambda: ["@SP", "A=M-1", "M=-M"],
    "eq": lambda: ["@SP", "AM=M-1", "D=-M", "A=A-1", "D=D+M", "M=-1",
                   f"@{label("eq")}", "D;JEQ", "@SP", "A=M-1", "M=0", f"({label("eq")})"],
    "gt": lambda: ["@SP", "AM=M-1", "D=-M", "A=A-1", "D=D+M", "M=-1",
                   f"@{label("gt")}", "D;JGT", "@SP", "A=M-1", "M=0", f"({label("gt")})"],
    "lt": lambda: ["@SP", "AM=M-1", "D=-M", "A=A-1", "D=D+M", "M=-1",
                   f"@{label("lt")}", "D;JLT", "@SP", "A=M-1", "M=0", f"({label("lt")})"],
    "and": lambda: ["@SP", "AM=M-1", "D=M", "A=A-1", "D=D&M", "M=D"],
    "or": lambda: ["@SP", "AM=M-1", "D=M", "A=A-1", "D=D|M", "M=D"],
    "not": lambda: ["@SP", "A=M-1", "M=!M"]
}
memory_access_commands: dict[str, Callable[[str, int], list[str]]] = {
    "push": lambda s, i: [*([f"@{i}", "D=A"]
                            if memory_segments[s].isConstant else
                            [f"@{memory_segments[s].address}", *(["A=M"] if memory_segments[s].isPointer else []),
                             "D=A", f"@{i}", "D=D+A", "A=D", "D=M"]),
                          "@SP", "A=M", "M=D", "@SP", "M=M+1"],
    "pop": lambda s, i: [f"@{memory_segments[s].address}", *(["A=M"] if memory_segments[s].isPointer else []),
                         "D=A", f"@{i}", "D=D+A", "@SP", "A=M", "M=D",
                         "@SP", "AM=M-1", "D=M", "@SP", "A=M+1", "A=M", "M=D"]
}


asm_code: list[str] = []
for i, line in enumerate(vm_code):
    command = line.split(" ")[0]
    if (command in memory_access_commands):
        if (len(line.split(" ")) != 3):
            raise Exception(
                "Unexpected number of arguments for memory access command")
        segment = line.split(" ")[1]
        index = line.split(" ")[2]
        if (not index.isdigit()):
            raise Exception("Index must be integer digit")
        else:
            index = int(index)
        if (segment in memory_segments.keys()):
            asm_code.append(f"// {line}")
            asm_code.extend(memory_access_commands[command](segment, index))
        else:
            raise Exception(f"Unknown memory segment '{segment}'")
    elif (command in stack_commands):
        asm_code.append(f"// {line}")
        asm_code.extend(stack_commands[command]())
    else:
        raise Exception(f"unexpected command '{command}'")

with open("program.asm" if output_filename is None else output_filename, "w") as asm_file:
    for i, command in enumerate(asm_code):
        asm_file.write(f"{command}")
        if (i != len(asm_code)-1):
            asm_file.write("\n")
