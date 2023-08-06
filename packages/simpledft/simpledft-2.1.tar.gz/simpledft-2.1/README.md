![simpledft logo](https://gitlab.com/wangenau/simpledft/-/raw/main/logo/simpledft_logo.png)

# SimpleDFT
[![language](https://img.shields.io/badge/language-Python3-green)](https://www.python.org)
[![license](https://img.shields.io/badge/license-APACHE2-lightgrey)](https://gitlab.com/wangenau/simpledft/-/blob/main/LICENSE)

SimpleDFT is a simple plane wave density functional theory (DFT) code.
It is a Python implementation of the [DFT++](https://arxiv.org/abs/cond-mat/9909130) pragmas proposed by Thomas Arias et al.
Also, it serves as the minimalistic prototype for the [eminus](https://gitlab.com/wangenau/eminus) code,
which was introduced in the [master thesis](https://www.researchgate.net/publication/356537762_Domain-averaged_Fermi_holes_A_self-interaction_correction_perspective) of Wanja Timm Schulze to explain theory and software development compactly.
There is also a version written in Julia, called [SimpleDFT.jl](https://gitlab.com/wangenau/simpledft.jl).

**Note: From version 2.0 on, the implementation will slightly deviate from the master thesis to be in line with eminus.**

| SimpleDFT | Description |
| --------- | ----------- |
| Language | Python 3 |
| License | Apache 2.0 |
| Dependencies | Only NumPy |
| Basis set| Plane waves (PW) |
| DFT | Restricted Kohn-Sham (RKS) |

# Installation
The package and all necessary dependencies can be installed using pip

```terminal
pip install simpledft
```

# Examples
Example calculations, i.e., the H atom, He atom, and H2 molecule can be executed with

```terminal
python examples.py
```

# Simplifications
This code is about implementing plane wave DFT as simple as possible, while still being general.
To classify the shortcomings from a fully-fletched DFT code, the most important simplifications are listed below
* Restricted Kohn-Sham DFT only, no open-shell systems
* LDA only, no functionals using gradients
* All-electron Coulomb potential, no pseudopotentials to only treat valence electrons
* Gamma-point only, no band paths
* Steepest descent only, no sophisticated minimizations
* Random starting guess only, no calculated guess of the density
