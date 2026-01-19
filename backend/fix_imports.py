import os
import re

def fix_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    patterns = [
        (r'^from deps', 'from app.deps'),
        (r'^from models', 'from app.models'),
        (r'^from db', 'from app.db'),
        (r'^from crud', 'from app.crud'),
        (r'^from auth', 'from app.auth'),
        (r'^from routers', 'from app.routers'),
    ]
    
    for old_pattern, new in patterns:
        content = re.sub(old_pattern, new, content, flags=re.MULTILINE)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed: {file_path}')

# Walk through all Python files in app directory
for root, dirs, files in os.walk('app'):
    if '__pycache__' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            fix_imports(os.path.join(root, file))

print('All imports fixed!')
