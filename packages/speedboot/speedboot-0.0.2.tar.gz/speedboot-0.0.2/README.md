# Speedboot
This library lets you boostrap vector-valued statistics fast as it uses parallel processing. Ploting estimates' distribution and computation of various confidence intervals are available. <img src="figures/logo.png" align="right" alt="" width="160" />

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

### History
Release history is available on <a href="https://pypi.org/project/speedboot/">PyPI</a>.
