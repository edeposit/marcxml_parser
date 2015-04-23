MARX XML Parser
===============

This module is used to parse MARC XML and OAI documents. Module provides API
to query such records and also to create records from scratch.

Module also contains getters which allows highlevel queries over documents,
such as :meth:`.get_name` and :meth:`.get_authors`, which returns informations
scattered over multiple subfields.

Package is developed and maintained by `E-deposit`_ team.

.. _E-deposit: http://edeposit.nkp.cz/

Package structure
-----------------

Parser is split into multiple classes, which each have own responsibility. Most
important is class :class:`.MARCXMLRecord`, which contains
:class:`.MARCXMLParser`, :class:`.MARCXMLSerializer` and :class:`.MARCXMLQuery`.

File relations
++++++++++++++

Import relations of files in project:

.. image:: /_static/relations.png
    :width: 400px

Class relations
+++++++++++++++

Relations of the classes in project:

.. image:: /_static/class_relations.png
    :width: 400px

API
---

:doc:`/api/marcxml_parser`:

.. toctree::
    :maxdepth: 1

    /api/parser.rst
    /api/serializer.rst
    /api/query.rst
    /api/record.rst


:doc:`/api/structures/structures`:

.. toctree::
    :maxdepth: 1

    /api/structures/person.rst
    /api/structures/corporation.rst
    /api/structures/marcsubrecord.rst
    /api/structures/publication_type.rst


:doc:`/api/tools/tools`:

.. toctree::
    :maxdepth: 1

    /api/tools/resorted.rst

Usage example
-------------

.. toctree::
    :maxdepth: 2

    /example/example

Installation
============
Module is hosted at `PYPI <https://pypi.python.org/pypi/marcxml_parser>`_,
and can be easily installed using `PIP`_::

    sudo pip install marcxml_parser

.. _PIP: http://en.wikipedia.org/wiki/Pip_%28package_manager%29


Source code
-----------
Project is released as opensource (MIT) and source code can be found at
GitHub:

- https://github.com/edeposit/marcxml_parser


Unittests
---------
Almost every feature of the project is tested by unittests. You can run those
tests using provided ``run_tests.sh`` script, which can be found in the root
of the project.

Requirements
++++++++++++
This script expects that pytest_ is installed. In case you don't have it yet,
it can be easily installed using following command::

    pip install --user pytest

or for all users::

    sudo pip install pytest

.. _pytest: http://pytest.org/


Example
+++++++
::

    $ ./run_tests.sh
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6 -- py-1.4.26 -- pytest-2.6.4
    collected 66 items

    tests/test_module.py ..
    tests/test_parser.py ............
    tests/test_query.py ...............................
    tests/test_record.py .
    tests/test_serializer.py .......
    tests/structures/test__structures_module.py .
    tests/structures/test_corporation.py .
    tests/structures/test_marcsubrecord.py .
    tests/structures/test_person.py .
    tests/structures/test_publication_type.py .
    tests/tools/test_resorted.py ........

    ========================== 66 passed in 1.14 seconds ===========================


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
