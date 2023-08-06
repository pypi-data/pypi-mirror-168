from ase.atoms import Atoms
import copy

def safe_euler_rotation(structure:Atoms, phi:float, theta:float, psi:float) -> Atoms:
    copied_structure = copy.deepcopy(structure)
    copied_structure.euler_rotate(phi, theta, psi)
    return copied_structure