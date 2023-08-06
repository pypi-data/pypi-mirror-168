# Speedboot
[![PyPI Latest Release](https://img.shields.io/pypi/v/speedboot.svg)](https://pypi.org/project/speedboot/)
[![License](https://img.shields.io/pypi/l/speedboot.svg)](https://github.com/fcgrolleau/speedboot/blob/main/LICENSE)
[![Python](https://img.shields.io/static/v1?label=made%20with&message=Python&color=blue&style=for-the-badge&logo=Python&logoColor=white)](#)

This library lets you boostrap vector-valued statistics fast as it uses parallel processing.  Ploting as well as computation of bias-corrected and accelerated confidence intervals are available. <img src="figures/logo.png" align="right" alt="" width="160" />

### Installation
```
pip install speedboot
```

### Implementation
```python
from speedboot import speedboot

sb_object = speedboot(data=n_sample, stats_fun=estimators)
sb_object.fit(R=999, par=True, seed=1)
sb_object.plot()
sb_object.emp_ci()
```
See a quick demo in <a href="https://github.com/fcgrolleau/speedboot/blob/main/speedboot/demo.ipynb">demo.ipynb</a>.
See baby simulations in <a href="https://github.com/fcgrolleau/speedboot/blob/main/speedboot/simulations.ipynb">simulations.ipynb</a>.

### History
Release history is available on <a href="https://pypi.org/project/speedboot/">PyPI</a>.
