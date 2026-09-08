import os
import glob

def replace_in_files(pattern_to_replace, replacement, directory, extension="*.py"):
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension[-3:]):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                if pattern_to_replace in content:
                    content = content.replace(pattern_to_replace, replacement)
                    with open(filepath, 'w') as f:
                        f.write(content)
                    print(f"Fixed {filepath}")

replace_in_files("a_platform.f_mcp.a_registry", "a_platform.f_mcp", "a_platform")
replace_in_files("a_platform.f_mcp.a_registry", "a_platform.f_mcp", "c_tests")

replace_in_files("a_platform.c_brain.memory", "a_platform.c_brain.e_memory", "a_platform")
replace_in_files("a_platform.c_brain.memory", "a_platform.c_brain.e_memory", "c_tests")

