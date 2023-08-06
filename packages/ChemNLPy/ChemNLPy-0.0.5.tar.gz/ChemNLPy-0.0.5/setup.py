import setuptools

with open('README.md', 'r', encoding='utf-8')as f:
    long_description = f.read()

setuptools.setup(
    name='ChemNLPy',
    version='0.0.5',
    author='zbc',
    author_email='zbc@mail.ustc.edu.cn',
    description='Chemical NLP for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=['chem_nlpy'],
    install_requires=['requests'],
    include_package_data=True,
    entry_points={
        'console_scripts': [

        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
