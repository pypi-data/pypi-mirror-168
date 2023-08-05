from setuptools import setup, find_packages

setup(
    name='Ginobifold',
    packages=find_packages(),
    include_package_data=True,
    version='0.1.2',
    description='Simplified Af2 inference code',
    author='Kexin Zhang',
    author_email='zhangkx2022@shanghaitech.edu.cn',
    license='MIT',
    keywords=['computational biology', "protein"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)
