# 将test_loader的所有smiles导出
# --------------------------------------
test_loader_smiles = []
for batch_id, batch_data in enumerate(test_loader):
    atom_feat, AM_bond_feat, node_color_feat, d, labels, masks, relativeenergys, num_atom_list, angle_group_num, num_confs_list,smiles = batch_data
    test_loader_smiles += smiles

str_ = '\n'
with open("./data/drugs/test_loader_smiles.smi", "w") as f:
    f.write(str_.join(test_loader_smiles))
    
# ===================================================

用conformator处理，得到初始构象sdf文件
# 将test_loader的所有smiles导出
# --------------------------------------
test_loader_smiles = []
for batch_id, batch_data in enumerate(test_loader):
    atom_feat, AM_bond_feat, node_color_feat, d, labels, masks, relativeenergys, num_atom_list, angle_group_num, num_confs_list,smiles = batch_data
    test_loader_smiles += smiles

str_ = '\n'
with open("./data/drugs/test_loader_smiles.smi", "w") as f:
    f.write(str_.join(test_loader_smiles))
    
# ===================================================

用conformator处理，得到初始构象sdf文件

# 将smiles 与 构象合并，保存为pickle文件
# ----------------------------------------------------------
from utils_others import get_suppl_from_sdf
from utils import load_smiles
from utils import count_console

# 读取构象
suppl = get_suppl_from_sdf("./data/drugs/test_loader_smiles.sdf")
# 合并
smiles_path_console = "./data/drugs/test_loader_smiles_console.txt"
valid_idx = count_console(smiles_path_console)
print(len(valid_idx))

set(range(1077))-set(valid_idx)   
# idx = 800
test_loader_smiles.pop(800)
# 'COc1cc2c(cc1OC)-c1c3c(cc4c1[C@@H](C2)N(C)CC4)OCO3'

dic = list(zip(test_loader_smiles, suppl))

# 保存到pkl文件中
pickle_.save("./data/drugs/test_loader_smol.pkl", dict(dic))

# 加载保存的mol
list_rd = pickle_.load("./data/drugs/test_loader_smol.pkl")
# ==============================================================
# 将smiles 与 构象合并，保存为pickle文件
# ----------------------------------------------------------
from utils_others import get_suppl_from_sdf
from utils import load_smiles
from utils import count_console

# 读取构象
suppl = get_suppl_from_sdf("./data/drugs/test_loader_smiles.sdf")
# 合并
smiles_path_console = "./data/drugs/test_loader_smiles_console.txt"
valid_idx = count_console(smiles_path_console)
print(len(valid_idx))

set(range(1077))-set(valid_idx)   
# idx = 800
test_loader_smiles.pop(800)
# 'COc1cc2c(cc1OC)-c1c3c(cc4c1[C@@H](C2)N(C)CC4)OCO3'

dic = list(zip(test_loader_smiles, suppl))

# 给每个mol添加他的smiles属性
for (smiles, mol) in dic:
    mol.smiles=smiles  

# 保存到pkl文件中
pickle_.save("./data/drugs/test_loader_mol.pkl", [i[1] for i in dic])

# 加载保存的mol
list_rd = pickle_.load("./data/drugs/test_loader_mol.pkl")
# ==============================================================