pip install hatch

Update
pyproject.toml

Change
version = "0.0.4"

hatch build

Get token
https://pypi.org/manage/account/token/?selected_project=celltypegenomics

twine upload --verbose dist/*