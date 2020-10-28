import os, sys, sysconfig

from setuptools import Extension, setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext

def get_ext_filename_without_platform_suffix(filename):
    name, ext = os.path.splitext(filename)
    ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')

    if ext_suffix == ext:
        return filename

    ext_suffix = ext_suffix.replace(ext, '')
    idx = name.find(ext_suffix)

    if idx == -1:
        return filename
    else:
        return name[:idx] + ext

class BuildExtWithoutPlatformSuffix(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        return get_ext_filename_without_platform_suffix(filename)

CMDCLS = {      
                'build_ext': BuildExtWithoutPlatformSuffix
         }

ext_modules = [Extension('phASER.read_variant_map',['phASER/_read_variant_map.py'])]

setup(
  name          = 'phASER', #'phASER Read Variant Mapper',
  packages      = ['phASER'],
  scripts       = ['phaser/phaser.py','phaser/call_read_variant_map.py', 'phaser_gene_ae/phaser_gene_ae.py'],
  #cmdclass      = CMDCLS,
  ext_modules   = cythonize(ext_modules,compiler_directives={'language_level' : "3"}),
)
