from distutils.core import setup
setup(
    name = 'microrm',
    packages = ['microrm'],
    version = '0.1.6',
    license='MIT',
    description = 'Small ORM library to use with asyncpg',
    author = 'Bohuslav Semenov',
    author_email = 'semenov0310@gmail.com',
    url = 'https://github.com/Bogusik/microrm',
    download_url = 'https://github.com/Bogusik/microrm/archive/v_016.tar.gz',
    keywords = ['asyncpg', 'orm', 'async'],
    install_requires=[
            'asyncpg'
        ],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Operating System :: OS Independent",
    'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)