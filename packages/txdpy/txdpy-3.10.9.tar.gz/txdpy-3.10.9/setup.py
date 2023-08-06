from distutils.core import  setup

packages = ['txdpy']# 唯一的包名

setup(name='txdpy',
    version='3.10.9',
    author='唐旭东',
    install_requires=['mmh3','PyMySQL','loguru','redis'],
    packages=packages,
    package_dir={'requests': 'requests'})