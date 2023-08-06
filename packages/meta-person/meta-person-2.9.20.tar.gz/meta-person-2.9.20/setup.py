from setuptools import setup, find_packages

requirements = [
    'opencv-python',
    'setuptools',
    'tensorrt',
    'pycuda',
    'numpy',
    'pillow',
]

__version__ = 'V2.09.20'

setup(
    name='meta-person',
    version=__version__,
    author='CachCheng',
    author_email='tkggpdc2007@163.com',
    url='https://github.com/CachCheng/cvperson',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    description='Meta Person Toolkit',
    license='Apache-2.0',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    zip_safe=True,
    include_package_data=True,
    install_requires=requirements,
)
