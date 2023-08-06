# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['normal_form', 'normal_form.tests']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0',
 'loguru>=0.6.0,<0.7.0',
 'more-itertools>=8.14.0,<9.0.0',
 'python-sat[aiger,pblib]>=0.1.7-dev.15,<0.2.0',
 'tqdm>=4.64.0,<5.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'normal-form',
    'version': '0.1.4',
    'description': 'A Python package for working with Conjunctive Normal Form (CNFs) and Boolean Satisfiability',
    'long_description': '**A Python package for working with Conjunctive Normal Form (CNFs) and\nBoolean Satisfiability (SAT)**\n\n<a href="https://img.shields.io/github/license/vaibhavkarve/normal-form?style=flat-square"> <img src="https://img.shields.io/github/license/vaibhavkarve/normal-form?style=flat-square" alt="License"> </a>\n<a href="https://img.shields.io/badge/Python-v3.10-blue?style=flat-square"> <img src="https://img.shields.io/badge/Python-v3.10-blue?style=flat-square" alt="Python:v3.10"> </a>\n\nThis Python package is brought to you by [Vaibhav Karve](https://vaibhavkarve.github.io) and [Anil N.\nHirani](https://faculty.math.illinois.edu/~hirani/), Department of Mathematics, University of Illinois at\nUrbana-Champaign.\n\n`normal-form` recognizes variables, literals, clauses, and CNFs. The\npackage implements an interface to easily construct CNFs and SAT-check\nthem via third-part libraries [MINISAT](http://minisat.se/) and [PySAT](https://pysathq.github.io/).\n\nThis package is written in Python v3.10, and is publicly available\nunder the [GNU-GPL-v3.0 license](https://github.com/vaibhavkarve/normal-form/blob/main/LICENSE). It is set to be released on the [Python\nPackaging Index](https://pypi.org/) as an open-source scientific package written in the\nliterate programming style. We specifically chose to write this\npackage as a literate program, despite the verbosity of this style,\nwith the goal to create reproducible computational research.\n\n\n# Installation and usage\n\nTo get started on using this package,\n\n1.  Istall Python 3.10 or higher.\n2.  `python3.10 -m pip install normal-form`\n3.  Use it in a python script (or interactive REPL) as &#x2013;\n\n        from normal_form import cnf\n        from normal_form import sat\n\n        # This is the CNF (a ∨ b ∨ ¬c) ∧ (¬b ∨ c ∨ ¬d) ∧ (¬a ∨ d).\n        x1: cnf.Cnf = cnf.cnf([[1, 2, -3], [-2, 3, -4], [-1, 4]])\n\n        sat_x1: bool = sat.cnf_bruteforce_satcheck(x1)\n        print(sat_x1)  # prints: True because x1 is satisfiable.\n\n\n# Overview of modules\n\nThe package consists of the following modules.\n\n<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">\n\n\n<colgroup>\n<col  class="org-left" />\n\n<col  class="org-left" />\n</colgroup>\n<tbody>\n<tr>\n<td class="org-left"><b>Modules that act on Cnfs</b></td>\n<td class="org-left">&#xa0;</td>\n</tr>\n\n\n<tr>\n<td class="org-left"><a href="cnf"><code>cnf.py</code></a></td>\n<td class="org-left">Constructors and functions for sentences in conjunctive normal form</td>\n</tr>\n\n\n<tr>\n<td class="org-left"><a href="cnf_simplify"><code>cnf_simplify.py</code></a></td>\n<td class="org-left">Functions for simplifying Cnfs, for example (a∨b∨c) ∧ (a∨b∨&not; c) ⇝ (a ∨ b)</td>\n</tr>\n\n\n<tr>\n<td class="org-left"><a href="prop"><code>prop.py</code></a></td>\n<td class="org-left">Functions for propositional calculus &#x2013; conjunction, disjunction and negation</td>\n</tr>\n\n\n<tr>\n<td class="org-left"><b>Modules concerning SAT</b></td>\n<td class="org-left">&#xa0;</td>\n</tr>\n\n\n<tr>\n<td class="org-left"><a href="sat"><code>sat.py</code></a></td>\n<td class="org-left">Functions for sat-checking Cnfs</td>\n</tr>\n\n\n<tr>\n<td class="org-left"><a href="sxpr"><code>sxpr.py</code></a></td>\n<td class="org-left">Functions for working with s-expressions</td>\n</tr>\n\n\n<tr>\n<td class="org-left"><b>Test suite</b></td>\n<td class="org-left">&#xa0;</td>\n</tr>\n\n\n<tr>\n<td class="org-left"><code>tests/*</code></td>\n<td class="org-left">Unit- and property-based tests for each module</td>\n</tr>\n</tbody>\n</table>\n\n\n# Algorithms\n\nCurrently, `normal-form` implements the following algorithms &#x2013;\n\n-   For formulae in conjunctive normal forms (CNFs), it implements\n    variables, literals, clauses, Boolean formulae, and\n    truth-assignments. It includes an API for reading, parsing and\n    defining new instances.\n\n-   For satisfiability of CNFs, it contains a bruteforce algorithm, an\n    implementation that uses the open-source sat-solver [PySAT](https://pysathq.github.io/), and an\n    implementation using the [MiniSAT](http://minisat.se/) solver.\n\n\n# Principles\n\n`normal-form` has been written in the functional-programming style\nwith the following principles in mind &#x2013;\n\n-   Avoid classes as much as possible. Prefer defining functions\n    instead.\n\n-   Write small functions and then compose/map/filter them to create\n    more complex functions.\n\n-   Use lazy evaluation strategy whenever possible (using the [itertools](https://docs.python.org/3/library/itertools.html)\n    library).\n\n-   Add type hints wherever possible (checked using the [mypy](https://mypy.readthedocs.io/en/stable/) static\n    type-checker).\n\n-   Add unit-tests for each function (checked using the [pytest](https://docs.pytest.org/en/latest/)\n    framework). Further, add property-based testing wherever possible\n    (using the [hypothesis](https://hypothesis.readthedocs.io) framework).\n',
    'author': 'Vaibhav Karve',
    'author_email': 'vkarve@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://vaibhavkarve.github.io/normal-form/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
