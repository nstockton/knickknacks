# Knickknacks

Small, reusable, miscellaneous pieces of code.

## License And Credits

Knickknacks is licensed under the terms of the [MIT License.](https://raw.githubusercontent.com/nstockton/knickknacks/master/LICENSE.txt "Knickknacks License")

### Running From Source

Install the [Python interpreter,](https://python.org "Python Home Page") and make sure it's in your path before running this package.

After Python is installed, execute the following commands from the top level directory of this repository to install the module dependencies.
```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade --require-hashes --requirement requirements-uv.txt
uv sync
pre-commit install -t pre-commit
pre-commit install -t pre-push
```
