# Base image
FROM python:3.7

# 1. Base packages
# 2. Packages for testing
# 3. Packages needed for icet
# 4. Packages for setting up documentation
RUN \
  apt-get update -qy && \
  apt-get upgrade -qy && \
  apt-get install -qy \
    doxygen \
    graphviz \
    pandoc \
    zip
# Packages for testing
# Packages needed for icet
# Packages for building documentation
RUN \
  pip3 install --upgrade \
    pip \
  && \
  pip3 install --upgrade \
    coverage \
    flake8 \
    mypy \
    nbmake \
    pytest \
    setuptools_scm \
    twine \
  && \
  pip3 install --upgrade \
    ase \
    mip==1.13.0 \
    numba \
    numpy \
    pandas \
    scikit-learn \
    scipy \
    spglib \
    xdoctest \
  && \
  pip3 install --upgrade \
    breathe \
    cloud_sptheme \
    nbsphinx \
    sphinx \
    sphinx-rtd-theme \
    sphinx_autodoc_typehints \
    sphinx_sitemap \
    sphinxcontrib-bibtex \
  && \
  pip3 install --upgrade \
    jinja2==3.0.3
