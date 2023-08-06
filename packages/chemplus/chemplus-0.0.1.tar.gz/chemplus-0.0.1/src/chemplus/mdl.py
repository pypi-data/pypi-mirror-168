from rdkit import Chem

def mol_adjust_hpolar(mol):
    mol = Chem.RemoveHs(mol)
    polar_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() != 'C']
    if len(polar_atoms):
        mol = Chem.AddHs(mol, onlyOnAtoms=polar_atoms)
        
    return mol
