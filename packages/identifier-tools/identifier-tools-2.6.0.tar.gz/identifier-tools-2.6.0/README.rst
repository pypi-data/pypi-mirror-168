Identifier Tools
################

Library that helps working with different subject identifier types. Purpose of this library is to validate string
if it matches the identifier format and if possible calculate checksum if it is correct for identifier.

Identifier format checking is based on European Central Bank - `List of national identifiers
<https://www.ecb.europa.eu/stats/money/aggregates/anacredit/shared/pdf/List_of_national_identifiers.xlsx>`_ spreadsheet.

Identifier format is extended by identifiers issued by Národná banka Slovenska - `Národné voľby a špecifiká v projekte
AnaCredit <https://www.nbs.sk/sk/dohlad-nad-financnym-trhom-prakticke-informacie/zoznamy-subjektov-registre-a-formulare/registre/register-bankovych-uverov-a-zaruk-rbuz/projekt-anacredit>`_.

Curentlly supported identifiers for checksum calculation: IČO, IČO NI, LEI, NIČ, all available identifiers and their
format is listed in file `identifier_tools/formats.py <identifier_tools/formats.py>`_.

Identifier Tools library has support for ISO 7064 standard that is used to validate NIČ, LEI, IBAN among other things...
Read more at wikipedia: https://en.wikipedia.org/wiki/ISO_7064


Installation
------------

Install the released version::

    pip install identifier-tools

Development
-----------

**We look forward to any kind of improvements and support for new identifiers.**

If you do add support for any identifier, checksum, etc. please add a link to the specific documentation that was
used for implementation, so we can reference to it.

Clone a repository locally and make sure you work in your own branch and once you are happy with the functionality
create pull request. All new code should be covered with tests. We try to use test driven development for the project.

**If you find a bug feel free to create an issue with description**, how ever we appreciate even more if you create failing test.

Release
-------

Release is done via `twine <https://pypi.org/project/twine/>`_. The whole package is uploaded in the form of .dist file.

To create .dist file use command::

    python setup.py sdist bdist_wheel

Now our binary .dist file is created, now we need to upload it using the below command::

    python -m twine dist/*

Alternatively if you want to selfhost in a custom PyPI repo you can also upload there as well::

    python -m twine upload--repository-url https://gitlab.com/custom/repo/path dist/* --cert /custom/cert


Testing
=======

Tests are written in pytest and stored in tests directory. Library has 100% test coverage.
**If you found an error, write a failing test first.**

Run the tests by following command::

    pytest identifier_tools
