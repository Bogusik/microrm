from distutils.core import setup
setup(
    name = 'mirorm',
    packages = ['microrm'],
    version = '0.1',
    license='MIT',
    description = 'Small ORM library to use with asyncpg',
    author = 'Bohuslav Semenov',
    author_email = 'semenov0310@gmail.com',
    url = 'https://github.com/Bogusik/microrm',
    download_url = 'https://github.com/Bogusik/microrm/archive/v_01.tar.gz',
    keywords = ['asyncpg', 'orm', 'async'],
    install_requires=[
            'asyncpg'
        ],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    ],
)