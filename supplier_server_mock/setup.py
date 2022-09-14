import setuptools

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='Supplier API mock server',
    version='1.5.2',
    author='Tiqets Team',
    author_email='connections@tiqets.com',
    description='Mock Server with Supplier API implementation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    entry_points='''
        [console_scripts]
        supplier_server=supplier_server.app:run
    ''',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=requirements,
)
