import sys
import numpy as np

def parse_lattice(line):
    """
    从给定的行字符串中解析晶胞参数。
    """
    parts = line.split('unitcell [{')[1].split('}]')[0].strip()
    lattice_lines = parts.split('}, {')
    lattice = [list(map(float, line.strip('{} ').split())) for line in lattice_lines]
    return lattice

def xyz_to_cif(xyz_file):
    # 读取 XYZ 文件
    with open(xyz_file, 'r') as file:
        lines = file.readlines()
    
    # 获取原子数
    num_atoms = int(lines[0].strip())
    
    # 解析晶胞参数（从第二行获取）
    lattice_line = lines[1].strip()
    lattice = parse_lattice(lattice_line)

    # 解析原子坐标和电荷
    species = []
    coords = []
    charges = []
    
    for line in lines[2:num_atoms+2]:
        parts = line.split()
        species.append(parts[0])
        coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
        charges.append(float(parts[4]))

    # 返回电荷信息供后续使用
    return charges

def add_charges_to_cif(original_cif_file, cif_file, charges):
    """
    重新读取 CIF 文件，提取最后一个 loop_ 部分，添加电荷信息。
    """
    contents = []
    atom_site = []
    with open(original_cif_file, 'r') as file:
        lines = file.readlines()
    
    # 找到最后一个 loop_ 的位置
    loop_start_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('loop_'):
            loop_start_index = i
    
    if loop_start_index == -1:
        raise ValueError("No loop_ found in CIF file")
    
    # 提取最后一个 loop_ 后面的内容
    loop_lines = lines[loop_start_index + 1:]
    
    for index, line in enumerate(loop_lines):
        # 如果行以 "_" 开头，记录键和值
        if line.strip().startswith('_'):
            atom_site.append(line.strip())
        else:
            # 如果行不以 "_" 开头，追加到 contents
            contents.append(line.strip())

    # 创建新的 CIF 文件
    with open(cif_file, 'w') as file:
        # 重新写入原始内容，不包括最后一个 loop_ 部分
        for i, line in enumerate(lines):
            if i <= loop_start_index:
                file.write(line)
        
        # 重新写入新的 loop_ 部分
        for item in atom_site:
            file.write(f'{item}\n')
        file.write('_atom_site_charge\n')

        # 写入数据
        for i in range(len(contents)):
            file.write(f'{contents[i]}    {charges[i]:.6f}\n')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("使用方法: python chargexyz2cif.py <input.xyz> <original cif> <output.cif>")
    else:
        xyz_file = sys.argv[1]
        original_cif_file = sys.argv[2]
        cif_file = sys.argv[3]

        # 调用函数进行转换
        charges = xyz_to_cif(xyz_file)
        add_charges_to_cif(original_cif_file, cif_file, charges)
