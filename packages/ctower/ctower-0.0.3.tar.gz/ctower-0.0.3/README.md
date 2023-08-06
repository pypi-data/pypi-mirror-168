# ctower
Control Tower CLI application.

## Poetry
```bash
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```

```bash
pip install ctower
ctower apply strongly-recommended
```

## Tasks
- upload to pypi
- logic for enabling controls
    - enable singular control to ou
    - sync one account to other
        - --strict to mirror the controls
        - nothing to just merge apply 
- ? maybe prompting
- show accounts under ous
- 