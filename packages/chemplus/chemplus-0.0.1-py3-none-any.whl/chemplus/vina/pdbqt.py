from chemplus.vina import rot_bond_helper
from chemplus import draw
import os
import glob
import subprocess
from joblib import Parallel, delayed
from tqdm import tqdm
from sys import platform
from rdkit import Chem

if platform == "linux" or platform == "linux2":
    search_location = os.path.expanduser('~') + "/bio/mgltools/bin/pythonsh"
elif platform == "win32":
    search_location = "C:/Program Files*/MGLTools*/python.exe"

try:
    mgl_python_default = glob.glob(search_location)[0]
except:
    print("MGLTools python not found. Please set the variable explicitly when calling the function")
    mgl_python_default = None

pl4_py = os.path.dirname(os.path.realpath(__file__)) + os.sep + "scripts/prepare_ligand4.py"
        
def pdb_to_pdbqt(pdb_file, pdbqt_file, mgl_python=mgl_python_default, overwrite=True, silent=False):  
    if not os.path.exists(mgl_python):
        raise Exception("MGL python is not exists")
        
    if not overwrite and os.path.exists(pdbqt_file):
         return
    
    pdb_name = os.path.basename(pdb_file).split('.')[0]
    
    bashCmd = [mgl_python, pl4_py, '-l', pdb_file, '-o', pdbqt_file]
    process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        output, error = process.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        if not silent:
            print('\nTimeoutExpired:', pdb_name)
        process.kill()
        output, error = process.communicate()
        return pdb_name

    if error:
        if not silent:
            print('\nError:', pdb_name, "-", error)
        return pdb_name

    return 1

def pdb_dir_to_pdbqt(pdb_dir, pdbqt_dir, cpu_count=2, mgl_python=mgl_python_default, overwrite=True, silent=False):
    if not os.path.exists(pdb_dir):
        raise Exception("PDB folder is not exists")

    if not os.path.exists(mgl_python):
        raise Exception("MGL python is not exists")

    if not os.path.exists(pdbqt_dir):
        os.makedirs(pdbqt_dir)

    exit_codes = Parallel(n_jobs=cpu_count, verbose=0)(delayed(pdb_to_pdbqt)(pdb_file, pdbqt_dir + os.sep + os.path.basename(pdb_file).split('.')[0] + ".pdbqt", mgl_python, overwrite, silent) for pdb_file in tqdm(glob.glob(pdb_dir + os.sep + '*.pdb')))

    pdb_num = len(exit_codes)
    bad_pdb_list = []
    converted_pdb_num = 0

    for code in exit_codes:
        if code == 1:
            converted_pdb_num += 1
        elif type(code) is str:
            bad_pdb_list.append(code)

    return pdb_num, converted_pdb_num, bad_pdb_list

def get_rotbond_atoms_pdb(pdb_file):    
    mol = Chem.MolFromPDBFile(pdb_file, removeHs=False)
    
    rot_bonds = rot_bond_helper.get_rot_bonds(mol)
    rot_bonds_atoms = []
    
    for bond in rot_bonds:
        first_atom = mol.GetBondWithIdx(bond).GetBeginAtom().GetPDBResidueInfo().GetSerialNumber()
        second_atom = mol.GetBondWithIdx(bond).GetEndAtom().GetPDBResidueInfo().GetSerialNumber()
        rot_bonds_atoms.append((first_atom, second_atom))
        
    return rot_bonds_atoms

def get_rotbond_atoms_pdbqt(pdbqt_file):
    lines = open(pdbqt_file).readlines()
    rotbond_lines = lines[2:lines.index("ROOT\n")]
    
    rot_bonds_atoms = []

    for line in rotbond_lines:
        if line[13] != "A":
            continue
        atoms_info = line[32:].split()
    
        first_atom = int(atoms_info[0].split("_")[1])
        second_atom = int(atoms_info[2].split("_")[1])
        rot_bonds_atoms.append((first_atom, second_atom))
        
    return rot_bonds_atoms

def rot_bonds_check(pdbqt_list, original_list, silent=True):
    errors = ([], [])
    
    for atom_pair in pdbqt_list:
        #non-rotatable bond is rotatable        
        if atom_pair not in original_list and (atom_pair[1], atom_pair[0]) not in original_list:
            error=True
            if not silent:
                print("ERROR: non-rotatable bond between atoms", atom_pair, "is rotatable")
            errors[0].append(atom_pair)
    
    for atom_pair in original_list:
        #rotatable bond is not rotatable
        if atom_pair not in pdbqt_list and (atom_pair[1], atom_pair[0]) not in pdbqt_list:
            warning=True
            if not silent:
                print("WARNING: rotatable bond between atoms", atom_pair, "is non-rotatable")
            errors[1].append(atom_pair)
    
    return errors

def fix_pdbqt(pdbqt_file, bad_bonds_list):
    lines = open(pdbqt_file).readlines()
    rb_section_end_index = lines.index("ROOT\n")
    rotbond_lines = lines[2:rb_section_end_index]
    
    counter = 0

    for i in range(len(rotbond_lines)):
        line = rotbond_lines[i]
        if line[13] != "A":
            continue
            
        atoms_info = line[32:].split()
        first_atom = int(atoms_info[0].split("_")[1])
        second_atom = int(atoms_info[2].split("_")[1])
        
        if (first_atom, second_atom) in bad_bonds_list or (second_atom, first_atom) in bad_bonds_list:
            rotbond_lines[i] = "REMARK       I" + line[14:]
        else:
            counter += 1
            rotbond_num = str(counter)
            rotbond_lines[i] = "REMARK" + (5 - len(rotbond_num)) * " " + rotbond_num + line[11:]
    
    lines[2:rb_section_end_index] = rotbond_lines
    
    old_rotbond_num = lines[0].split()[1]
    torsdof_line_index = lines.index("TORSDOF " + old_rotbond_num + "\n")
    lines[torsdof_line_index] = "TORSDOF " + str(counter) + "\n"
    lines[0] = "REMARK  " + str(counter) + " active torsions:\n"
    
    open(pdbqt_file, "w").writelines(lines)
    
    return

def check_pdbqt_rot_bonds(pdbqt_file, pdb_file, silent=True, fix_bad_pdbqt=False):
    mol_name = os.path.basename(pdbqt_file).split(".")[0]
        
    rotbonds_pdbqt = get_rotbond_atoms_pdbqt(pdbqt_file)
    
    try:
        rotbonds_pdb = get_rotbond_atoms_pdb(pdb_file)
    except AttributeError:
        raise
    
    bad_rb, missed_rb = rot_bonds_check(rotbonds_pdbqt, rotbonds_pdb, silent)
    if bad_rb:
        if not silent:
            print("Mol:", mol_name)
            print("***")
    elif missed_rb:
        if not silent:
            print("Mol:", mol_name)
            print("***")
    
    if bad_rb and fix_bad_pdbqt:
        fix_pdbqt(pdbqt_file, bad_rb)
    
    return bad_rb, missed_rb

def check_pdbqt_rot_bonds_image(mol_name, pdbqt_dir, pdb_dir, silent=True, fix_bad_pdbqt=False, png_file=None):
    pdbqt_file = pdbqt_dir + os.sep + mol_name + ".pdbqt"
    if not os.path.exists(pdbqt_file):
        return "PDBQT doesn't exists"
    
    pdb_file = pdb_dir + os.sep + mol_name + ".pdb"
    
    try:
        bad_rb, missed_rb = check_pdbqt_rot_bonds(pdbqt_file, pdb_file, silent, fix_bad_pdbqt)
    except AttributeError:
        return "PDB is broken"
    
    if bad_rb or missed_rb:
        return draw.draw_bad_rot_bonds(pdb_file, bad_rb, missed_rb, png_file)

def check_pdbqt_dir_rot_bonds(pdbqt_dir, pdb_dir, silent=True, fix_bad_pdbqt=False, check_images_dir=None):
    
    if not os.path.exists(pdbqt_dir):
        raise Exception("PDBQT folder is not exists")
        
    if not os.path.exists(pdb_dir):
        raise Exception("PDB folder is not exists")
    
    if check_images_dir and not os.path.exists(check_images_dir):
        os.makedirs(check_images_dir)
    
    bad_pdbqt_list = []
    missed_rb_pdbqt_list = []
    
    for pdbqt_file in tqdm(glob.glob(pdbqt_dir + os.sep + "*.pdbqt")):
        mol_name = os.path.basename(pdbqt_file).split(".")[0]

        pdb_file = pdb_dir + os.sep + mol_name + ".pdb"

        try:
            bad_rb, missed_rb = check_pdbqt_rot_bonds(pdbqt_file, pdb_file, silent, fix_bad_pdbqt)
        except AttributeError:
            return "PDB is broken"
        
        if bad_rb:
            bad_pdbqt_list.append(mol_name)
        elif missed_rb:
            missed_rb_pdbqt_list.append(mol_name)
            
        if (bad_rb or missed_rb) and check_images_dir:
            image_path = check_images_dir + os.sep + mol_name + ".png"
            draw.draw_bad_rot_bonds(pdb_file, bad_rb, missed_rb, image_path)
    
    return bad_pdbqt_list, missed_rb_pdbqt_list

def filter_pdbqt(pdbqt_dir, silent=False, delete_overnrb_pdbqt=True):
    
    if not os.path.exists(pdbqt_dir):
        raise Exception("PDBQT folder is not exists")
    
    overnrb_pdbqt_list = []
    
    for pdbqt_file in tqdm(glob.glob(pdbqt_dir + os.sep + "*.pdbqt")):
        mol_name = os.path.basename(pdbqt_file).split(".")[0]
        
        pdbqt_stream = open(pdbqt_file)
        while True:
            line = pdbqt_stream.readline()
            if "active torsions:" in line:
                pdbqt_stream.close()
                break
        rotbonds_num = int(line.split()[1])
        
        if rotbonds_num > 20:
            overnrb_pdbqt_list.append(mol_name)
            if not silent:
                print(mol_name, "contains", rotbonds_num, "rotatable bonds")
            if delete_overnrb_pdbqt:
                os.remove(pdbqt_file)
        
    return overnrb_pdbqt_list