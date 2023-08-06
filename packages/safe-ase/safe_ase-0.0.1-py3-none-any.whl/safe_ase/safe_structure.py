import copy
from ase.atoms import Atoms


def safe_structure(struct_dict:dict, key:str) -> Atoms:
    return copy.deepcopy(struct_dict[key])