# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lxzbiotools']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0',
 'matplotlib>=3.6.0,<4.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['lxzbiotools = lxzbiotools.lxzbiotools:app',
                     'utils = lxzbiotools.utils:app']}

setup_kwargs = {
    'name': 'lxzbiotools',
    'version': '0.5.2',
    'description': "Xingze Li's Bioinformatics Analysis Scripts",
    'long_description': "## Introduction\n\n**lxzbiotools** contains some bioinformation data processing scripts.\n\nObviously, it is not perfect, so it will be updated later until it is strong enough\n\n## Install\n\n```\npip3 install lxzbiotools\n```\n\n## Use\n\n```bash\n$ python3 ~/lxzbiotools/lxzbiotools/lxzbiotools.py  --help\n\n Usage: lxzbiotools.py [OPTIONS] COMMAND [ARGS]...\n\n Xingze Li's bioinformatics analysis scripts.\n emali: lixingzee@gmail.com\n\n╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell.        │\n│                                                              [default: None]                                    │\n│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy   │\n│                                                              it or customize the installation.                  │\n│                                                              [default: None]                                    │\n│ --help                                                       Show this message and exit.                        │\n╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ cds2pep         Convert cds file to pep file                                                                    │\n│ excel2txt       Convert excel file to txt file                                                                  │\n│ fa2fq           Convert a fasta file to a fastq file                                                            │\n│ fq2fa           Convert a fastq file to a fasta file                                                            │\n│ genstats        single or multiple genome information statistics                                                │\n│ gfa2fa          Convert gfa file to fasta file                                                                  │\n│ gff             Simplify gff3 file for WGD event analysis                                                       │\n│ len             Get the length of each sequence                                                                 │\n│ rds             Read a multi-FASTA file sequence and remove duplicates (by MD5 hash)                            │\n│ run             Parallelized running tasks                                                                      │\n│ seq             Extract sequences by sequence name or keyword                                                   │\n│ tolf            Convert multi-line fasta to one-line fasta                                                      │\n╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n\n```\n",
    'author': 'Xingze_Li',
    'author_email': 'lixingzee@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
