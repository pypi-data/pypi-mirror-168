from distutils.core import  setup

packages = ['txdpy']# 唯一的包名

setup(name='txdpy',
    version='3.10.10',
    author='唐旭东',
    install_requires=['mmh3','pymysql','loguru','redis','lxml'],
    packages=packages,
    package_dir={'requests': 'requests'})