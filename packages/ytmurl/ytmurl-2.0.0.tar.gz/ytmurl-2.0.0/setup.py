import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ytmurl',
    author='Jack Zhu',
    author_email='jzwenxuan@gmail.com',
    description='From search keywords to MP3 URL with YouTube Music',
    keywords='example, pypi, package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JZ-Wenxuan/ytmurl',
    project_urls={
        'Documentation': 'https://github.com/JZ-Wenxuan/ytmurl',
        'Bug Reports':
        'https://github.com/JZ-Wenxuan/ytmurl/issues',
        'Source Code': 'https://github.com/JZ-Wenxuan/ytmurl',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=['ytmusicapi', 'yt_dlp'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'ytmurl=ytmurl:main',
        ],
    },
)
