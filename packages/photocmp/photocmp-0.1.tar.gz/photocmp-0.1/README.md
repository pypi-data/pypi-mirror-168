# photocmp
Compare pictures with standard metrics.

## Installation
The project will be published on PyPI as soon as it gets more mature.

In the meantime, it can be installed trough pip as follows
```
python3 setup.py sdist bdist_wheel
pip install dist/photocmp-x.y.tar.gz
```
where `x.y` must replaced with the right version number.

## Command-line tool
The `photocompare` can be used from the shell.
The main usage is:
```
photocompare reference otherset
```
where `reference` is the reference set and `otherset` is the one it
will be compared against (additional sets can be specified as well).
Enter `photocompare -h` for additional help.

## Supported metrics
- [X] MSE
- [X] PSNR
- [X] SSIM
- [ ] Delta E
- [ ] LPIPS
- [ ] Frechet?
