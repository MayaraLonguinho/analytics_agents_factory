import os
import re
import sys
import string

EXCLUDED_FILES = {
    "__init__.py", "Dockerfile", "docker-compose.yml", ".env.example", 
    "README.md", "requirements.txt", "requirements-dev.txt", "pytest.ini", 
    ".gitignore", "registry.yaml", "apply_prefixes.py"
}

EXCLUDED_DIRS = {
    ".git", ".venv", ".pytest_cache", "__pycache__", ".obsidian", 
    "scratch", "e_generated_projects"
}

def get_next_prefix(used_prefixes):
    def generate_all_prefixes():
        for char in string.ascii_lowercase:
            yield char
        for char1 in string.ascii_lowercase:
            for char2 in string.ascii_lowercase:
                yield char1 + char2
                
    for prefix in generate_all_prefixes():
        if prefix not in used_prefixes:
            return prefix
    return "zzz"

def get_new_path(old_path, rename_map):
    parts = old_path.split(os.sep)
    new_parts = []
    current_old_path = ""
    for i, part in enumerate(parts):
        if i == 0:
            current_old_path = part
            if part == "":
                pass
            else:
                new_parts.append(part)
            continue
            
        current_old_path = current_old_path + os.sep + part if current_old_path else part
        
        if old_path.startswith(os.sep) and i == 1 and not current_old_path.startswith(os.sep):
            current_old_path = os.sep + current_old_path
            
        if current_old_path in rename_map:
            new_parts.append(rename_map[current_old_path])
        else:
            new_parts.append(part)
            
    prefix = os.sep if old_path.startswith(os.sep) else ""
    return prefix + os.sep.join(new_parts)

def rename_in_directory(dir_path):
    rename_map = {}
    
    for root, dirs, files in os.walk(dir_path, topdown=False):
        skip = False
        for ex in EXCLUDED_DIRS:
            if os.sep + ex + os.sep in root or root.endswith(os.sep + ex):
                skip = True
                break
        if skip:
            continue
            
        valid_dirs = [d for d in dirs if d not in EXCLUDED_DIRS]
        valid_files = [f for f in files if f not in EXCLUDED_FILES]
        
        items = valid_dirs + valid_files
        
        used_prefixes = set()
        unprefixed = []
        
        for item in items:
            match = re.match(r'^([a-z]{1,2})_', item)
            if match:
                used_prefixes.add(match.group(1))
            else:
                unprefixed.append(item)
                
        unprefixed.sort()
        
        item_to_new_name = {}
        for item in unprefixed:
            prefix = get_next_prefix(used_prefixes)
            used_prefixes.add(prefix)
            new_name = f"{prefix}_{item}"
            item_to_new_name[item] = new_name
            
        for item, new_name in item_to_new_name.items():
            old_abs = os.path.join(root, item)
            new_abs = os.path.join(root, new_name)
            os.rename(old_abs, new_abs)
            rename_map[old_abs] = new_name
            
    return rename_map

def get_module_path(filepath, base_dir):
    rel_path = os.path.relpath(filepath, base_dir)
    if rel_path.endswith('.py'):
        rel_path = rel_path[:-3]
    return rel_path.replace(os.sep, '.')

if __name__ == "__main__":
    base_dir = os.path.abspath(os.getcwd())
    print("Renaming files and folders...")
    
    all_old_files = []
    for root, dirs, files in os.walk(base_dir):
        skip = False
        for ex in EXCLUDED_DIRS:
            if os.sep + ex + os.sep in root or root.endswith(os.sep + ex):
                skip = True
                break
        if skip:
            continue
        for file in files:
            if file.endswith('.py') or file.endswith('.yaml') or file.endswith('.md'):
                all_old_files.append(os.path.join(root, file))
                
    rename_map = rename_in_directory(base_dir)
    print(f"Total renamed items: {len(rename_map)}")
    
    module_replacements = []
    path_replacements = []
    
    for old_file in all_old_files:
        new_file = get_new_path(old_file, rename_map)
        if old_file != new_file:
            old_mod = get_module_path(old_file, base_dir)
            new_mod = get_module_path(new_file, base_dir)
            
            old_dir = os.path.dirname(old_file)
            new_dir = os.path.dirname(new_file)
            old_dir_mod = get_module_path(old_dir, base_dir)
            new_dir_mod = get_module_path(new_dir, base_dir)
            
            if old_mod != new_mod:
                module_replacements.append((old_mod, new_mod))
            if old_dir_mod != new_dir_mod:
                module_replacements.append((old_dir_mod, new_dir_mod))
                
            old_rel = os.path.relpath(old_file, base_dir)
            new_rel = os.path.relpath(new_file, base_dir)
            path_replacements.append((old_rel, new_rel))
            
            old_rel_dir = os.path.relpath(old_dir, base_dir)
            new_rel_dir = os.path.relpath(new_dir, base_dir)
            path_replacements.append((old_rel_dir, new_rel_dir))
            
    module_replacements = list(set(module_replacements))
    module_replacements.sort(key=lambda x: len(x[0]), reverse=True)
    
    path_replacements = list(set(path_replacements))
    path_replacements.sort(key=lambda x: len(x[0]), reverse=True)
    
    print("Updating file contents...")
    for root, dirs, files in os.walk(base_dir):
        skip = False
        for ex in EXCLUDED_DIRS:
            if os.sep + ex + os.sep in root or root.endswith(os.sep + ex):
                skip = True
                break
        if skip:
            continue
            
        for file in files:
            if file.endswith('.py') or file.endswith('.yaml') or file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception:
                    continue
                    
                new_content = content
                
                for old_mod, new_mod in module_replacements:
                    if file.endswith('.py'):
                        new_content = re.sub(r'\b' + re.escape(old_mod) + r'\b', new_mod, new_content)
                        old_basename = old_mod.split('.')[-1]
                        new_basename = new_mod.split('.')[-1]
                        if old_basename != new_basename:
                            new_content = re.sub(r'from \.' + re.escape(old_basename) + r'\b', r'from .' + new_basename, new_content)
                            new_content = re.sub(r'from \.\.' + re.escape(old_basename) + r'\b', r'from ..' + new_basename, new_content)
                            
                for old_rel, new_rel in path_replacements:
                    new_content = new_content.replace(old_rel, new_rel)
                    
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

    print("Updating pytest.ini...")
    pytest_ini_path = os.path.join(base_dir, 'pytest.ini')
    with open(pytest_ini_path, 'w') as f:
        f.write("[pytest]\npython_files = *test*.py\n")
        
    print("Done.")
