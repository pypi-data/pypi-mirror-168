from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='tghelper',
    version='0.0.2',
    description='Useful tools to work with TigerGraph in Python',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages('tghelper'),
    package_dir={'': 'src'},
    author="Louis Pienaar",
    author_email='lpienaar@gmail.com',
    keywords=['TigerGraph'],
    url='https://github.com/louisza/tghelper',
    download_url='https://pypi.org/project/tghelper/'
)

install_requires = ['pyTigerGraph'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
