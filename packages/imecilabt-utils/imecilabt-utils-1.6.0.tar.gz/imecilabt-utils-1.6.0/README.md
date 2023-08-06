# Imec iLab.t utils

A collection of functions useful in various projects iLab.t projects.

These assorted utils are all lightweight and have no dependencies. 
This is all MIT license, so you are free to copy only what you need.

Overview:
- `sentry_utils.py` has `find_sentry_release_id` which is used to automatically find the sentry release. 
- `urn_util.py` contains function for working with a specific type (["geni"](https://groups.geni.net/geni/wiki/GeniApiIdentifiers)) of URN.
- `validation_utils.py` has functions to validate ssh keys, emails and UUIDs
- `utils.py` contains a wide range of useful functions:
   - `normalize_depenv` returns "staging" or "production"
   - `datetime_now` returns "now" as a timezone aware datetime. (naive datetimes are evil!)
   - `any_to_{opt_}bool` converts to bool
   - `duration_string_to_seconds` parses string like "3 days" into a number of seconds
   - `deep_update_dict` merges a dict into another
   - `strip_null_from_json_dict` strips None and empty lists/dicts from a dict (useful to clean up json) 

Links:
- Gitlab: https://gitlab.ilabt.imec.be/ilabt/imecilabt-py-utils
- PyPi: https://pypi.org/project/imecilabt-utils/
