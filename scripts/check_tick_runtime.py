"""Check the project SDK without importing its native exit handler or credentials."""
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / 'work/python-deps/gm/__version__.py'
MINIMUM = (3, 0, 187)

def main():
    if not VERSION_FILE.is_file():
        print(json.dumps({'ok': False, 'reason': 'project gm SDK is missing'}))
        return 1
    tree = ast.parse(VERSION_FILE.read_text(encoding='utf-8'))
    version = next(ast.literal_eval(n.value) for n in tree.body
                   if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == '__version__' for t in n.targets))
    actual = tuple(int(v) for v in version.split('.')[:3])
    ok = actual >= MINIMUM
    print(json.dumps({'ok': ok, 'gm_sdk': version, 'required_minimum': '.'.join(map(str, MINIMUM)),
                      'python': sys.executable, 'credentials_read': False}))
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
