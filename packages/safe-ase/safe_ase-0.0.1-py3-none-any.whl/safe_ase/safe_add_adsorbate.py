from ase.build import add_adsorbate
from ase.atoms import Atoms
import copy

def safe_add_adsorbate(base:Atoms, base_index:int, ads:Atoms, ads_index:int, bond_length:float) -> Atoms:
    base_position = (base[base_index].position[0], base[base_index].position[1])
    copied_base = copy.deepcopy(base)
    copied_ads = copy.deepcopy(ads)
    add_adsorbate(copied_base, copied_ads, position=base_position, height=bond_length, mol_index=ads_index)
    return copied_base