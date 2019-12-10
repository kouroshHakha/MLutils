"""A script that maps old modules to new modules for pickle compatible imports and re-saves the
data"""
import pickle
import sys
import torch
from pathlib import Path
from importlib import import_module

from utils.pdb import register_pdb_hook
from utils.file import read_yaml
from utils.importlib import import_class

register_pdb_hook()

config_file = Path(__file__).parent / 'compatibilty.yaml'
module_specs = read_yaml(config_file)
import_as = module_specs['import_as']
from_import = module_specs['from_import']

for key, val in import_as.items():
    sys.modules[key] = import_module(val)

for key, val in from_import.items():
    sys.modules[key] = import_class(val)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
for work_dir in Path('data').iterdir():
    if work_dir.is_dir():
        for file in work_dir.iterdir():
            try:
                if file.name.endswith('.tar'):
                    torch.save(torch.load(file, map_location=torch.device('cpu')), file)
                    print(f'[success] {file}')
                elif file.name.endswith('.pickle'):
                    with open(str(file), 'rb') as f:
                        content = pickle.load(f)
                    with open(str(file), 'wb') as f:
                        pickle.dump(content, f)
                    print(f'[success] {file}')

            except Exception as e:
                print(f'[failed] {file}')
                print(f'{e}')
