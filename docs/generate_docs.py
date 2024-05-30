import os
import subprocess

def clean_apidocs(output_dir):
    """Remove all previously generated .rst files except index.rst."""
    for dirpath, dirnames, filenames in os.walk(output_dir):
        for fname in filenames:
            if fname.endswith('.rst') and fname != 'index.rst':
                os.remove(os.path.join(dirpath, fname))

def generate_apidocs(root_dir, output_dir):
    """Generate .rst files for all Python modules in the project."""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if any(fname.endswith('.py') for fname in filenames):
            subprocess.run(['sphinx-apidoc', '-o', output_dir, dirpath, '--force', '--module-first', '--separate'])

def update_modules(output_dir):
    """Update modules.rst to include references to all generated .rst files."""
    modules_file = os.path.join(output_dir, 'modules.rst')
    with open(modules_file, 'w') as f:
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 2\n\n")
        for dirpath, dirnames, filenames in os.walk(output_dir):
            for fname in filenames:
                if fname.endswith('.rst') and fname not in ['index.rst', 'modules.rst']:
                    relative_path = os.path.relpath(os.path.join(dirpath, fname), output_dir)
                    module_path = os.path.splitext(relative_path)[0].replace(os.path.sep, '/')
                    f.write(f"   {module_path}\n")

# def adjust_rst_files(output_dir, root_dir):
#     """Adjust the module paths in the .rst files to include the relative directory structure."""
#     for dirpath, dirnames, filenames in os.walk(output_dir):
#         for fname in filenames:
#             if fname.endswith('.rst') and fname not in ['index.rst', 'modules.rst']:
#                 file_path = os.path.join(dirpath, fname)
#                 with open(file_path, 'r') as f:
#                     lines = f.readlines()
#                 with open(file_path, 'w') as f:
#                     for line in lines:
#                         if line.startswith('.. automodule::'):
#                             module_path = os.path.relpath(dirpath, root_dir).replace(os.path.sep, '.') + '.' + line.split()[-1]
#                             f.write(f'.. automodule:: {module_path}\n')
#                         else:
#                             f.write(line)

if __name__ == "__main__":
    # Get the root directory (one level up from the script's location)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Output directory is the current directory (docs)
    output_dir = os.path.abspath(os.path.dirname(__file__))

    # Clean previously generated .rst files except index.rst
    clean_apidocs(output_dir)

    # Generate new .rst files
    generate_apidocs(root_dir, output_dir)

    # Adjust the module paths in the .rst files
    # adjust_rst_files(output_dir, root_dir)

    # Update modules.rst to include all modules
    update_modules(output_dir)
