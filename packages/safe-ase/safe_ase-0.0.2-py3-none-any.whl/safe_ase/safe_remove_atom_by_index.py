from ase.atoms import Atoms
import copy

def safe_remove_atom_by_index(structure:Atoms, index:int) -> Atoms:
    copied_structure = copy.deepcopy(structure)
    copied_structure.pop(index)
    return copied_structure
