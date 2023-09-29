
# This file is the entire environmentor library.
# It does not depend on anything beyond the python
# standard library version 3.7+ or so and an internet connection
# or other source of packages available to `python -m pip`.




import os
import sys
import subprocess
import importlib


def ensure_module(module_name, package_name=None):
  if package_name is None:
    package_name = module_name

  vers_major = sys.version_info[0]
  vers_minor = sys.version_info[1]

  env_target = os.path.join(os.path.dirname(__file__), '.py-env', '{}_{}'.format(vers_major, vers_minor))
  os.makedirs(env_target, mode=0o777, exist_ok=True)
  if not env_target in sys.path:
    sys.path.append(env_target)

  try:
    return importlib.import_module(module_name)
  except:
    subprocess.run([
      sys.executable, '-m', 'pip', 'install', f'--target={env_target}', *(package_name.split())
    ])

  return importlib.import_module(module_name)


def ensure_py_version(comparison_chars, major_version, minor_version, addtl_runtime_locations=[]):

    raise Exception('TODO unimplemented!')




