

from rich.table import Table
from rich.syntax import Syntax
from rich.columns import Columns
from rich.panel import Panel

import logging
logger = logging.getLogger('rich')

def from_quaternion_to_asm(quaternion):
    match quaternion.operation:
        case "ADD":
            return f"{quaternion.result} = {quaternion.arg1} + {quaternion.arg2}"
        case "SUB":
            return f"{quaternion.result} = {quaternion.arg1} - {quaternion.arg2}"
        case "DIV":
            return f"{quaternion.result} = {quaternion.arg1} / {quaternion.arg2}"
        case "MUL":
            return f"{quaternion.result} = {quaternion.arg1} * {quaternion.arg2}"
        case "MOV":
            return f"{quaternion.result} = {quaternion.arg1}"
        case "MOD":
            return f"{quaternion.result} = {quaternion.arg1} % {quaternion.arg2}"
        case "JMP":
            return f"GOTO {quaternion.result}"
        case "JE":
            return f"IF {quaternion.arg1} == {quaternion.arg2} GOTO {quaternion.result}"
        case "JNE":
            return f"IF {quaternion.arg1} != {quaternion.arg2} GOTO {quaternion.result}"
        case "JG":
            return f"IF {quaternion.arg1} > {quaternion.arg2} GOTO {quaternion.result}"
        case "JL":
            return f"IF {quaternion.arg1} < {quaternion.arg2} GOTO {quaternion.result}"
        case "JGE":
            return f"IF {quaternion.arg1} >= {quaternion.arg2} GOTO {quaternion.result}"
        case "JLE":
            return f"IF {quaternion.arg1} <= {quaternion.arg2} GOTO {quaternion.result}"
        case "CALL":
            return f"CALL {quaternion.arg1}"
        case "PUSH":
            return f"PUSH {quaternion.arg1}"
        case "POP":
            return f"POP {quaternion.arg1}"
        case "RET":
            return "RET"
        case "INC":
            return f"{quaternion.result} = {quaternion.arg1} + 1"
        case "DEC":
            return f"{quaternion.result} = {quaternion.arg1} - 1"
        case "NEG":
            return f"{quaternion.result} = -{quaternion.arg1}"
        case "NOT":
            return f"{quaternion.result} = !{quaternion.arg1}"
    
def ref_from_memory(memory, ptr):
    if ptr == None:
        return "-"
    if isinstance(ptr, str):
        return ptr
    if ptr < 0 or ptr >= len(memory):
        return f"#{ptr}"
    return (
        f"${ptr}({memory[ptr].name})"
        if memory[ptr].name
        else f"${ptr}(={memory[ptr].value})"
    )

def transfer_ref(code, memory, labels):
    code.arg1 = ref_from_memory(memory, code.arg1)
    code.arg2 = ref_from_memory(memory, code.arg2)
    code.result = labels[code.result] if code.result in labels else ref_from_memory(memory, code.result)
    return code

def display_semantic_result(memory, codes, labels):
    logger.info(f"Memory: {memory}")
    logger.info(f"Code: {codes}")
    logger.info(f"Label: {labels}")

    label_tag = ["-" for _ in range(len(codes))]
    for label, row_index in labels.items():
        if not isinstance(row_index, int):
            continue
        label_tag[row_index] = label if label_tag[row_index] == '-' else label_tag[row_index] + f", {label}"

    result_table = Table(title="Semantic Result")
    result_table.add_column("Index", style="magenta")
    result_table.add_column("Label", style="magenta")
    result_table.add_column("OP", style="green")
    result_table.add_column("ARG1", style="green")
    result_table.add_column("ARG2", style="green")
    result_table.add_column("RESULT", style="green")


    for i, (label, code) in enumerate(zip(label_tag, codes)):
        result_table.add_row(
            str(i),
            label,
            ref_from_memory(memory, code.operation),
            ref_from_memory(memory, code.arg1),
            ref_from_memory(memory, code.arg2),
            ref_from_memory(memory, code.result),
        )

    memory_table = Table(title="Memory")
    memory_table.add_column("Pointer", style="magenta")
    memory_table.add_column("Name", style="magenta")
    memory_table.add_column("Value", style="green")
    memory_table.add_column("Type", style="green")
    memory_table.add_column("Size", style="green")
    for i, mem in enumerate(memory):
        memory_table.add_row(
            str(i), str(mem.name), str(mem.value), str(mem.type), str(mem.size)
        )

    ret = ''
    for code in codes:
        ret += from_quaternion_to_asm(transfer_ref(code, memory, labels)) + '\n'
    ret_format = Syntax(ret, "asm", line_numbers=True, word_wrap=True, code_width=60, start_line=0)
    panel = Panel(ret_format, title="Output code")
    

    return Columns([memory_table, result_table, panel])
