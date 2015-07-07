# Author: Robert T. McGibbon
# License: CC0 1.0 Universal: http://creativecommons.org/publicdomain/zero/1.0/

import sys
import os
import yaml
import glob
import shutil
from conda_build.config import config
import subprocess
import traceback

branch = None
if 'TRAVIS_BRANCH' in os.environ:
    branch = os.environ['TRAVIS_BRANCH']
if 'APPVEYOR_REPO_BRANCH' in os.environ:
    branch = os.environ['APPVEYOR_REPO_BRANCH']

if(branch):
    if branch == sys.argv[2]:
        with open(os.path.join(sys.argv[1], 'meta.yaml')) as f:
            name = yaml.load(f)['package']['name']
        binary_package_glob = os.path.join(config.bldpkgs_dir,
                                           '{0}*.tar.bz2'.format(name))
        binary_package = glob.glob(binary_package_glob)[0]
        shutil.move(binary_package, '.')
    
        token = os.environ['BINSTAR_TOKEN']
        cmd = ['binstar', '-t', token, 'upload', '--force']
        cmd.extend(glob.glob('*.tar.bz2'))
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            traceback.print_exc()
