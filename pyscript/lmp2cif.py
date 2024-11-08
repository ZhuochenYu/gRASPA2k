import os
import sys
from ase import Atoms
from ase.io import read, write

atm = {
    "1": "H", "2": "He", "3": "Li", "4": "Be", "5": "B", "6": "C", "7": "N",
    "8": "O", "9": "F", "10": "Ne", "11": "Na", "12": "Mg", "13": "Al", "14": "Si",
    "15": "P", "16": "S", "17": "Cl", "18": "Ar", "19": "K", "20": "Ca", "21": "Sc",
    "22": "Ti", "23": "V", "24": "Cr", "25": "Mn", "26": "Fe", "27": "Co", "28": "Ni",
    "29": "Cu", "30": "Zn", "31": "Ga", "32": "Ge", "33": "As", "34": "Se", "35": "Br",
    "36": "Kr", "37": "Rb", "38": "Sr", "39": "Y", "40": "Zr", "41": "Nb", "42": "Mo",
    "43": "Tc", "44": "Ru", "45": "Rh", "46": "Pd", "47": "Ag", "48": "Cd", "49": "In",
    "50": "Sn", "51": "Sb", "52": "Te", "53": "I", "54": "Xe", "55": "Cs", "56": "Ba",
    "57": "La", "58": "Ce", "59": "Pr", "60": "Nd", "61": "Pm", "62": "Sm", "63": "Eu",
    "64": "Gd", "65": "Tb", "66": "Dy", "67": "Ho", "68": "Er", "69": "Tm", "70": "Yb",
    "71": "Lu", "72": "Hf", "73": "Ta", "74": "W", "75": "Re", "76": "Os", "77": "Ir",
    "78": "Pt", "79": "Au", "80": "Hg", "81": "Tl", "82": "Pb", "83": "Bi", "84": "Po",
    "85": "At", "86": "Rn"
}

atmmass = {
    "1": "1.008", "2": "4.0026", "3": "6.94", "4": "9.0122", "5": "10.81", "6": "12.011", "7": "14.007",
    "8": "15.999", "9": "18.998", "10": "20.180", "11": "22.990", "12": "24.305", "13": "26.982", "14": "28.085",
    "15": "30.974", "16": "32.06", "17": "35.45", "18": "39.948", "19": "39.098", "20": "40.078", "21": "44.956",
    "22": "47.867", "23": "50.942", "24": "51.996", "25": "54.938", "26": "55.845", "27": "58.933", "28": "58.693",
    "29": "63.546", "30": "65.38", "31": "69.723", "32": "72.630", "33": "74.922", "34": "78.971", "35": "79.904",
    "36": "83.798", "37": "85.468", "38": "87.62", "39": "88.906", "40": "91.244", "41": "92.906", "42": "95.95",
    "43": "98", "44": "101.07", "45": "102.91", "46": "106.42", "47": "107.87", "48": "112.41", "49": "114.82",
    "50": "118.71", "51": "121.76", "52": "127.60", "53": "126.90", "54": "131.29", "55": "132.91", "56": "137.33",
    "57": "138.91", "58": "140.12", "59": "140.91", "60": "144.24", "61": "145", "62": "150.36", "63": "151.96",
    "64": "157.25", "65": "158.93", "66": "162.50", "67": "164.93", "68": "167.26", "69": "168.93", "70": "173.05",
    "71": "174.97", "72": "178.49", "73": "180.95", "74": "183.84", "75": "186.21", "76": "190.23", "77": "192.22",
    "78": "195.08", "79": "196.97", "80": "200.59", "81": "204.38", "82": "207.2", "83": "208.98", "84": "209",
    "85": "210", "86": "222", "Lw": "0"
}

def round_and_trim(num):
    rounded_num = round(num, 3)
    return str(rounded_num).rstrip('0').rstrip('.')

def process_file(file_path):
    with open(file_path, 'r') as f:
        contents = f.readlines()

    atm_number = int(contents[1].split()[0])
    atm_types = int(contents[11].split()[0])
    
    for i, line in enumerate(contents):
        if "Masses" in line:
            masses_line = i
            break
    start_line = int(masses_line) + 2
    end_line = start_line + atm_types
    mass_content = contents[start_line:end_line]

    for i, line in enumerate(contents):
        if "Atoms" in line:
            atoms_line = i
            break
    start_line2 = int(atoms_line) + 2
    end_line2 = start_line2 + atm_number
    atoms_content = contents[start_line2:end_line2]

    atmmass_inverse = {value: key for key, value in atmmass.items()}
    new_atoms_content = []

    for line in atoms_content:
        target_value = round_and_trim(float(mass_content[int(line.split()[2]) - 1].split()[1]))
        line_parts = line.split()
        line_parts[2] = atmmass_inverse[target_value]
        line = ' '.join(line_parts)
        new_atoms_content.append(line)

    output_file_path = file_path.replace('result_', 'new_result_')
    with open(output_file_path, 'w') as f:
        rm = sum(1 for line in new_atoms_content if line.split()[2] == 'Lw')
        for i in range(17):
            if i == 1:
                line = str(int(contents[1].split()[0]) - rm) + ' ' + contents[1].split()[1]
                f.write(line + '\n')
            else:
                f.write(contents[i])
        f.write('Masses\n\n')
        for line in mass_content:
            f.write(line)
        f.write('\nAtoms\n')
        for line in new_atoms_content:
            if line.split()[2] != 'Lw':
                f.write(line + '\n')

    lammps_atoms = read(output_file_path, format='lammps-data')
    cif_output_path = output_file_path.replace('new_result_', 'result_').replace('.data', '.cif')
    write(cif_output_path, lammps_atoms)

def main(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.startswith('result_') and file_name.endswith('.data'):
            file_path = os.path.join(folder_path, file_name)
            process_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        main(folder_path)

