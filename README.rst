# Command Wrapper

### Install

```
$> pip install -i https://testpypi.python.org/pypi sparkgeo-utils
```

### Config File

The tool reads from a default `commands.json` file that contains JSON describing the different commands that are wrapped. Use `--help` to see all the available base commands.

### Rebuild and Upload

After a new change is made, the package must be re-built and uploaded to `testpypi`. However make sure the version number is bumped first.

```
$> sudo python setup.py sdist install
$> sudo python setup.py sdist develop  <- So it can be tested locally before hand, not required though.
```

Once the package has been tested (manually or through unittests) then it can be uploaded.

```
$> python setup.py sdist upload -r https://testpypi.python.org/pypi
```