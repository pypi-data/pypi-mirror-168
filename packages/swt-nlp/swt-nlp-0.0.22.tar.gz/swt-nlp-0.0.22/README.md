# SWT-NLP PACKAGE

### HOW TO BUILD A PACKAGE TO PYPI
prerequisite
``` shell
pip install setuptools wheel tqdm twine
```

build and upload package
```
# preparing tar.gz package 
python setup.py sdist
# uploading package to pypi server
python -m twine upload dist/{package.tar.gz}  --verbose
```

install package
``` shell
# install latest version
pip install swt-nlp --upgrade
# specific version with no cache
pip install swt-nlp==0.0.11  --no-cache-dir
```

install package by wheel
``` shell
# build wheel 
python setup.py bdist_wheel

# install package by wheel 
# use --force-reinstall if needed
pip install dist/{package.whl}
```

