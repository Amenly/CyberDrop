import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
]

REQUIREMENTS = ['requests', 'beautifulsoup4', 'lxml']

setuptools.setup(
    name='cyberdrop',
    version='1.2.0',
    author='Amenly',
    author_email='uamenly@protonmail.com',
    description='A command line tool written in Python for downloading images and videos from CyberDrop albums',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Amenly/CyberDrop',
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
    keywords=['cyberdrop', 'scraper', 'download', 'photos', 'videos'],
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': ['cyberdrop=cyberdrop.cyberdrop:main']
    }
)
