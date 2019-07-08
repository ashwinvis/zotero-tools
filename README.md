Getting started
---------------

Create a file `_creds.py` containing your Zotero and GitHub credentials. Modify
the values of the following variables:

```python
USERID = "my_zotero_id"
KEY = "super_secret_zotero_key"
GITHUB_ACCESS_TOKEN = "supersecret_github_personal_access_token_read_only"
```

Run `fix.py` with or without `dry_run=True`.
