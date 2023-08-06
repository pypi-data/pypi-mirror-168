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
    'version': '0.5.4',
    'description': "Xingze Li's Bioinformatics Analysis Tools",
    'long_description': '## Project description\n\n**lxzbiotools** is a bioinformatics data processing tools.\n\n## Features\n\n+ `cds2pep`         Convert cds file to pep \n+ `excel2txt`       Convert file format form excel to txt\n+ `fa2fq`           Change fasta file to fastq file\n+ `fq2fa`           Change fastq file to fasta file\n+ `genstats`        One or more genome informatics statistics\n+ `gfa2fa`          Convert gfa file to fasta file\n+ `gff`             Simplify gff3 file for WGD event analysis\n+ `length`          Get the length of each sequences\n+ `rds`             Read a multi-FASTA file sequence and remove duplicates\n+ `parallel`        Parallelized running tasks\n+ `extseq`          Extract sequences by sequence name or keyword \n+ `m2ofa`           Convert multi-line fasta to one-line fasta           \n+ `movefile`        Randomly allocate files to a specified number of folders \n\n## QuickStart\n\n\n### Install\n\n```\npip3 install lxzbiotools\n```\n\n### Update\n\n```\npip3 install -U lxzbiotools\n```\n\n### Use\n\n```bash\n$ lxzbiotools --help\n\n Usage: lxzbiotools.py [OPTIONS] COMMAND [ARGS]...\n```\n\n\n## Version update content\n+ *2022-09-22* version **0.5.4** add **movefile** (Randomly allocate files to a specified number of folders)\n\n## Bug report \n\n+ Issues and bugs report to **lixingzee@gmail.com**\n\n+ github: *https://github.com/lxingze/lxzbiotools*\n\n',
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
