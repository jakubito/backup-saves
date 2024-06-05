import os
import json
import shutil
import datetime

config_path = os.path.join(os.path.dirname(__file__), 'config.json')

if not os.path.isfile(config_path):
    raise FileNotFoundError('Config file does not exist')

config_file = open(config_path, encoding='utf-8')
config = json.load(config_file)

if not 'entries' in config:
    raise ValueError('"entries" is missing')

for entry in config['entries']:
    if not 'name' in entry:
        raise ValueError('"name" is missing')
    if not 'source_dir' in entry:
        raise ValueError('"source_dir" is missing')
    if not 'backup_dirs' in entry:
        raise ValueError('"backup_dirs" is missing')

    name = entry['name']
    source_dir = entry['source_dir']
    backup_dirs = entry['backup_dirs']

    if not os.path.isdir(source_dir):
        print(f'Skipping "{source_dir}"')
        continue

    for backup_dir in backup_dirs:
        if not os.path.isdir(backup_dir):
            raise NotADirectoryError(f'Backup dir "{source_dir}" does not exist')

    timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y%m%dT%H%M%SZ')
    backup_name = f'{name}-backup_{timestamp}'
    temp_backup_path_noext = os.path.join(os.path.dirname(__file__), backup_name)
    temp_backup_path = f'{temp_backup_path_noext}.zip'

    shutil.make_archive(temp_backup_path_noext, 'zip', source_dir)
    
    for backup_dir in backup_dirs:
        shutil.copy(temp_backup_path, backup_dir)
        print(f'{backup_name} copied to "{backup_dir}"')

    os.remove(temp_backup_path)
