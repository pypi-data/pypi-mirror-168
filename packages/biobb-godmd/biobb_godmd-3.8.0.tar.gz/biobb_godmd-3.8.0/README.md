[![](https://readthedocs.org/projects/biobb-godmd/badge/?version=latest)](https://biobb-godmd.readthedocs.io/en/latest/?badge=latest)
[![](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](https://anaconda.org/bioconda/biobb_godmd)
[![](https://img.shields.io/badge/docker-Quay.io-blue)](https://quay.io/repository/biocontainers/biobb_godmd)
[![](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# biobb_godmd

### Introduction
biobb_godmd is a BioBB category for the GOdMD tool.
biobb_godmd allows the calculation of protein conformational transitions using the GOdMD tool.
Biobb (BioExcel building blocks) packages are Python building blocks that
create new layer of compatibility and interoperability over popular
bioinformatics tools.
The latest documentation of this package can be found in our readthedocs site:
[latest API documentation](http://biobb_godmd.readthedocs.io/en/latest/).

### Version
v3.8.0 2022.3

### Installation
Using PIP:

> **Important:** PIP only installs the package. All the dependencies must be installed separately. To perform a complete installation, please use ANACONDA or DOCKER.

* Installation:


        pip install "biobb_godmd>=3.7.0"


* Usage: [Python API documentation](https://biobb-godmd.readthedocs.io/en/latest/modules.html)

Using ANACONDA:

* Installation:


        conda install -c bioconda "biobb_godmd>=3.7.0"


* Usage: With conda installation BioBBs can be used with the [Python API documentation](https://biobb-godmd.readthedocs.io/en/latest/modules.html) and the [Command Line documentation](https://biobb-godmd.readthedocs.io/en/latest/command_line.html)

Using DOCKER:

* Installation:


        docker pull quay.io/biocontainers/biobb_godmd:3.8.0--pyhdfd78af_0


* Usage:


        docker run quay.io/biocontainers/biobb_godmd:3.8.0--pyhdfd78af_0


[//]: # (Using SINGULARITY:)

[//]: # (**MacOS users**: it's strongly recommended to avoid Singularity and use **Docker** as containerization system.)

[//]: # (* Installation:)


[//]: # (singularity pull --name biobb_godmd.sif shub://bioexcel/biobb_godmd)


[//]: # (* Usage:)


[//]: # (singularity exec biobb_godmd.sif)


The command list and specification can be found at the [Command Line documentation](https://biobb-godmd.readthedocs.io/en/latest/command_line.html).

### Copyright & Licensing
This software has been developed in the [MMB group](http://mmb.irbbarcelona.org) at the [BSC](http://www.bsc.es/) & [IRB](https://www.irbbarcelona.org/) for the [European BioExcel](http://bioexcel.eu/), funded by the European Commission (EU H2020 [823830](http://cordis.europa.eu/projects/823830), EU H2020 [675728](http://cordis.europa.eu/projects/675728)).

* (c) 2015-2022 [Barcelona Supercomputing Center](https://www.bsc.es/)
* (c) 2015-2022 [Institute for Research in Biomedicine](https://www.irbbarcelona.org/)

Licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), see the file LICENSE for details.

![](https://bioexcel.eu/wp-content/uploads/2019/04/Bioexcell_logo_1080px_transp.png "Bioexcel")
