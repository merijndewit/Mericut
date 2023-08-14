from dataclasses import dataclass

@dataclass
class MericodeSlicingOptions:
    calculatePathOrder : bool = True
    cutting : bool = False

    def __init__(self):
        pass

