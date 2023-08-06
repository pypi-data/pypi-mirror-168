from setuptools import setup

setup(
    name='enhanced_dir',
    version='0.2.73',
    description='An enhanced version of dir, which gives more details',
    py_modules=['enhanced_dir'],
    install_requires=['matplotlib', 'seaborn'],
    package_dir={'': 'src'},
)