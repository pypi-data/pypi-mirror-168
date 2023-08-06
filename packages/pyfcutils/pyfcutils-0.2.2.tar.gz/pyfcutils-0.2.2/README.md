# pyfcutils

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/legend-exp/pyfcutils?logo=git)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/legend-exp/pyfcutils/pyfcutils/main?label=main%20branch&logo=github)](https://github.com/legend-exp/pyfcutils/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Codecov](https://img.shields.io/codecov/c/github/legend-exp/pyfcutils?logo=codecov)](https://app.codecov.io/gh/legend-exp/pyfcutils)
![GitHub issues](https://img.shields.io/github/issues/legend-exp/pyfcutils?logo=github)
![GitHub pull requests](https://img.shields.io/github/issues-pr/legend-exp/pyfcutils?logo=github)
![License](https://img.shields.io/github/license/legend-exp/pyfcutils)

pyfcutils offers a wrapper (via Cython) around the fcio library, with
simplified accessors to the config and event data.

```console
$ pip install git+https://github.com/legend-exp/pyfcutils@main # version identifier after '@'
```

The `example` folder contains examples of how to easily display FlashCam
waveforms and related data (timestamp, baseline estimate etc).
