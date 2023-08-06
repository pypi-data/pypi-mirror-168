from typing import Union

MIN_MEM_GI = 1
MAX_MEM_GI = 256
MIN_MEM_MI = 128
MAX_MEM_MI = 999


def betweenOrEqual(value: int, lower: int, upper: int) -> bool:
    return lower <= value <= upper


def parseCPU(cpu: str) -> str:
    # CPU is sent to operator as '(CPU_CORES * 1000)m'
    # See composeCPU function

    return int(int(cpu[:-1]) / 1000)


def composeCPU(cpu: Union[int, str]) -> str:
    if isinstance(cpu, str):
        cpu = parseCPU(cpu)

    return f"{cpu * 1000}m"


def parseMemory(memory: str) -> str:
    suffix = memory[-2:]

    if suffix not in ["Gi", "Mi"]:
        raise ValueError("Memory must end with Gi or Mi")

    return memory


def composeMemory(memory: str) -> str:
    memory = memory.strip()
    suffix = memory[-2:]
    number = int(memory[:-2].strip())

    if suffix.lower() not in ["gi", "mi"]:
        raise ValueError("Memory must end with Gi or Mi")

    if suffix.lower() == "gi" and not betweenOrEqual(number, MIN_MEM_GI, MAX_MEM_GI):
        raise ValueError(
            f"Memory value is invalid for Gi: value must be between {MIN_MEM_GI} and {MAX_MEM_GI}"
        )

    if suffix.lower() == "mi" and not betweenOrEqual(number, MIN_MEM_MI, MAX_MEM_MI):
        raise ValueError(
            f"Memory value is invalid for Mi: value must be between {MIN_MEM_MI} and {MAX_MEM_MI}"
        )

    return str(number) + suffix.capitalize()
