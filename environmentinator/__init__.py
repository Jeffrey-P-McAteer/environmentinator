
# This file is the entire environmentor library.
# It does not depend on anything beyond the python
# standard library version 3.7+ or so and an internet connection
# or other source of packages available to `python -m pip`.

import os
import sys
import subprocess
import importlib
import inspect
import shutil

def ensure_module(module_name, package_name=None):
  '''
    Returns the imported module `module_name` if it exists,
    if not uses `pip` to install `package_name` and returns the imported module `module_name`.

    `package_name` may be multiple packages seperated by whitespace,
    for eg AI libraries where soft-dependencies
    would be good to install at the same time even though you will never
    explicitly import them (eg you want to use the module `torch` but installing the packages
    `torch torchvision torchaudio` will ensure the module `torch`'s vision APIs are available.)

    Packages are installed to the folder `.py-env/{MAJOR}_{MINOR}/{PACKAGE_NAME}` relative
    to the code that calls `environmentinator.ensure_module`. This folder is added to `sys.path` during imports,
    but we do not modify environment variables. If you need sub-processes to see the same imported
    packages, do something clever like `os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)` before spawning
    your sub-processes.

    If you use a lot of code under version control ensure that `.py-env` is in your `.gitignore` file.

    ## Example Uses

    ```python
      import environmentinator
      json5 = environmentinator.ensure_module('json5')
      # equivelant to manual environment setup + "import json5"
      my_var = json5.loads('{"not": "valid", /* json */ }')
    ```

  '''
  if not isinstance(module_name, str):
    raise Exception('module_name must be a string, got {}'.format(module_name))

  if package_name is None:
    package_name = module_name

  if not isinstance(package_name, str):
    raise Exception('package_name must be a string, got {}'.format(package_name))
  
  vers_major = sys.version_info[0]
  vers_minor = sys.version_info[1]

  callee_file = __file__
  try:
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    callee_file = module.__file__
  except:
    pass

  env_target = os.path.join(os.path.dirname(callee_file), '.py-env', '{}_{}'.format(vers_major, vers_minor))
  os.makedirs(env_target, mode=0o777, exist_ok=True)
  if not env_target in sys.path:
    sys.path.append(env_target)

  try:
    return importlib.import_module(module_name)
  except:
    subprocess.run([
      sys.executable, '-m', 'pip', 'install', '--target={}'.format(env_target), *(package_name.split())
    ])

  return importlib.import_module(module_name)

def delete_all_environmentinator_modules():
  '''
    Deletes the folder `.py-env/{MAJOR}_{MINOR}` relative to the code that calls `environmentinator.delete_all_environmentinator_modules`
  '''
  vers_major = sys.version_info[0]
  vers_minor = sys.version_info[1]

  callee_file = __file__
  try:
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    callee_file = module.__file__
  except:
    pass

  env_target = os.path.join(os.path.dirname(callee_file), '.py-env', '{}_{}'.format(vers_major, vers_minor))
  if os.path.exists(env_target):
    shutil.rmtree(env_target)

def ensure_py_version(comparison_chars, major_version, minor_version, addtl_runtime_locations=[]):
    '''
      TODO unimplemented!
    '''
    raise Exception('TODO unimplemented!')




