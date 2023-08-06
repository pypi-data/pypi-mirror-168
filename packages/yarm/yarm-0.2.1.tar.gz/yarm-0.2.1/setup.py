# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yarm',
 'yarm.templates',
 'yarm.tests_data',
 'yarm.tests_data.test_queries_options',
 'yarm.tests_data.test_validate_complete_config_valid',
 'yarm.tests_data.test_validate_slugify']

package_data = \
{'': ['*'],
 'yarm.tests_data': ['test_config_bad_options/*',
                     'test_config_bad_yaml/*',
                     'test_create_tables/*',
                     'test_df_input_options/*',
                     'test_df_tables_config_options/*',
                     'test_df_tables_config_options/output/*',
                     'test_overwrite_file/*',
                     'test_prep_config_copies_files/*',
                     'test_report_aborts_invalid_config_no_edits/*',
                     'test_validate_export_tables_only/*',
                     'test_validate_export_tables_only/output/*',
                     'test_validate_fails_check_is_file/*',
                     'test_validate_missing_required_key/*',
                     'test_validate_need_export_tables_or_queries/*',
                     'test_validate_tables_config_valid_mwe/*',
                     'test_verbose_levels/*',
                     'valid_config/*'],
 'yarm.tests_data.test_queries_options': ['output/*'],
 'yarm.tests_data.test_validate_complete_config_valid': ['OUTPUT/*'],
 'yarm.tests_data.test_validate_slugify': ['output/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.1',
 'matplotlib>=3.5.3,<4.0.0',
 'nob>=0.8.2,<0.9.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.3,<2.0.0',
 'path>=16.4.0,<17.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'strictyaml>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['yarm = yarm.__main__:cli']}

setup_kwargs = {
    'name': 'yarm',
    'version': '0.2.1',
    'description': 'Yarm',
    'long_description': '# yarm\n\nYarm: Yet Another Report Maker.\n\n[![PyPI](https://img.shields.io/pypi/v/yarm.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/yarm.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/yarm)][python version]\n[![License](https://img.shields.io/pypi/l/yarm)][license]\n\n[![Read the documentation at https://yarm.readthedocs.io/](https://img.shields.io/readthedocs/yarm/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/billalive/yarm/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/billalive/yarm/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/yarm/\n[status]: https://pypi.org/project/yarm/\n[python version]: https://pypi.org/project/yarm\n[read the docs]: https://yarm.readthedocs.io/\n[tests]: https://github.com/billalive/yarm/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/billalive/yarm\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\nYarm makes it easy for you to create **recurring reports** by:\n\n- Importing **multiple spreadsheets and CSVs** into a temporary database.\n- Offering **easy** options for **common data cleaning** tasks (e.g. `replace`, `slugify_columns`, `pivot`)\n- Running **SQL queries** (or, for [pandas] fans, [custom **Python** code][postprocess]) on all this data.\n- **Exporting the results** as a new **spreadsheet**, **CSV**, or even SQLite **database**.\n- All configured in a [simple **YAML file**][config] for easy **reuse**. Download fresh data, `yarm run`, and you\'re done.\n\n## Basic Usage\n\n### First Time You Run a New Report\n\n- Collect your XLSX and/or CSV data files into a directory for this report.\n\n- Initialize a new YAML config file:\n\n```console\n$ yarm new\n```\n\n- Edit the YAML config file (see below).\n\n  - Configure your input spreadsheets and CSV files as tables.\n  - Write one or more [SELECT] queries on these tables to create output sheets.\n  - (Optional) Need advanced manipulation of your data? Write [pandas] code in a separate `.py` file.\n\n- Run the report:\n\n```yaml\n$ yarm run\n```\n\n- Send the output spreadsheet to your boss/client/head of state. Was it really that easy?\n\n### Every Subsequent Time\n\n- Collect fresh data. Save it over the old files.\n\n- Run the report.\n\n```yaml\n$ yarm run -f\n```\n\n- Send the output spreadsheet.\n\n- Take the afternoon off.\n\n## Advanced Usage\n\nPlease see the extensive [documentation][read the docs] for more details and features.\n\n## Example Report Config File\n\nYou configure a report in a [single YAML file][config].\n\nEach query becomes a separate sheet in your output spreadsheet.\n\nThis example config file is moderately complex. Your report can be much simpler; you might have only one or two tables and a single query. (Or you might have ten queries, each with a [custom postprocess function][postprocess]...)\n\n```yaml\n---\noutput:\n  dir: Output\n  basename: Sales_Report\n\n# Optional input options (more are available):\ninput:\n  slugify_columns: true\n  lowercase_columns: true\n\n# Set up your data sources:\ntables_config:\n  # CSV file: the easiest data source.\n  products:\n    - path: Products.csv\n\n  # Spreadsheet: You need both the path and the sheet name.\n  orders:\n    - path: Orders.xlsx\n      sheet: Orders\n\n  # You can import different sheets as separate tables.\n  order_details:\n    - path: Orders.xlsx\n      sheet: Order Details\n\n  # You can combine multiple data sources into a single table,\n  # as long as their columns can be merged.\n  tax:\n    - path: Sales Tax Rates Northeast.xlsx\n      sheet: NY\n    - path: Sales Tax Rates Northeast.xlsx\n      sheet: PA\n    - path: TAXES_SOUTH.csv\n\n# Set up your output spreadsheet:\nqueries:\n  - name: Order Details with Product Names\n    sql: SELECT * FROM order_details as od JOIN products as p ON od.product_id = p.id;\n\n  - name: Orders With Sales Tax\n    sql: >\n      SELECT orders.*,\n      tax.rate\n      FROM orders\n      JOIN tax\n      ON orders.billing_state = tax.state\n      ;\n    # These query results will need a Python function to complete this sheet:\n    postprocess: calculate_tax\n    # But first, we can do simple regex replacements right here:\n    replace:\n      billing_state:\n        Virginia: VA\n        West Virginia: WV\n\n# Since we need that custom function calculate_tax(), we\'ll\n# write it in a separate Python file.\nimport:\n  - path: custom.py\n```\n\nRead more about [basic configuration][config] and [advanced options][options].\n\n## Custom Postprocessing Code\n\nIf the power of SQL and make-it-easy options like `slugify_columns` aren\'t enough for you, you can write a [custom postprocess function][postprocess] for any query you like.\n\n## Status: Alpha (Try It!)\n\nYarm is currently in **alpha**. Core features are **working** and thoroughly [documented][read the docs].\n\nI rely on `yarm` for my own recurring reports.\n\nIf you are desperate to stop doing a recurring report by hand, give _yarm_ a try.\n\nIf something breaks, or if you have any suggestions or comments, please [file an issue]. I\'d love to hear what you think.\n\nFor upcoming features, see the [Roadmap].\n\n## Requirements\n\n- Python 3.7 or later\n- A terminal\n- One or more spreadsheets that you want to query\n- Something to do with all this impending free time...\n\n## Installation\n\nYou can install _yarm_ via [pip] from [PyPI]:\n\n```console\n$ pip install yarm\n```\n\nBut since _yarm_ is a command line tool, you may prefer the excellent [pipx]:\n\n```console\n$ pipx install yarm\n```\n\n## Documentation\n\nComplete, _extensive_ documentation is at [yarm.readthedocs.io][read the docs].\n\nDive right in.\n\n## Is `yarm` for You?\n\nThis tool has a clear focus: Make it **easy** to run and **rerun reports** from the **command line** that query **multiple sources** of tabular data.\n\nOnce you set up the initial configuration file, the workflow for future reports is simple. Download fresh data over the old files, then rerun the report.\n\nThis means that `yarm` is **not** a tool for data **exploration**.\n\nTrue, you may still want `yarm` to **prepare** your data for exploration. Once you get used to listing a few data sources, setting a few options, and spitting out a nice, clean SQLite database or set of CSV files to play with, you may get hooked.\n\nBut for iterative tinkering with your data, you\'re going to need other tools.\n\n### Other Open Source Tools You Might Prefer\n\n- [sqlitebrowser]: An excellent GUI for exploring your SQLite database. I sometimes use this to **figure out my queries** before I save them into my config file.\n\n- [Jupyter Lab]: If you find your SQL queries getting more and more arcane and complex, it\'s probably time to learn [pandas], and that means unleashing the power of this [interactive "notebook"][jupyter lab]. Some reports are so complex that they really deserve to be run step-by-step, with immediate output after every command. Jupyter Lab makes that absurdly easy... and repeatable.\n\n- [SQL Notebook]: A newer offering that I haven\'t used yet, but it looks like an interesting GUI combination of sqlitebrowser and a "Jupyter-style notebook interface". Could be very powerful.\n\n- For quick, **one-off** data manipulations on the **command line**, you can reach for excellent tools like [jq] for JSON, [mlr] for CSV, and even [htmlq] for HTML. But once the command gets long and complex enough that you want to save it to a script, you might start missing SQL queries and `yarm` features like `slugify_columns: true`.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [Apache 2.0 license][license],\n_Yarm_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems, please [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/billalive/yarm/issues\n[pip]: https://pip.pypa.io/\n[pipx]: https://pypa.github.io/pipx/\n[matplotlib]: https://matplotlib.org/\n[pandas]: https://pandas.pydata.org/\n[jupyter lab]: https://jupyter.org/try\n[select]: https://www.sqlite.org/lang_select.html\n[sqlitebrowser]: https://sqlitebrowser.org/\n[sql notebook]: https://sqlnotebook.com/\n[jq]: https://stedolan.github.io/jq/\n[mlr]: https://miller.readthedocs.io/en/latest/\n[htmlq]: https://github.com/mgdm/htmlq\n[config]: https://yarm.readthedocs.io/en/latest/config/\n[options]: https://yarm.readthedocs.io/en/latest/config/options.html\n[postprocess]: https://yarm.readthedocs.io/en/latest/postprocess.html\n[roadmap]: https://yarm.readthedocs.io/en/latest/roadmap.html\n\n<!-- github-only -->\n\n[license]: https://github.com/billalive/yarm/blob/main/LICENSE\n[contributor guide]: https://github.com/billalive/yarm/blob/main/CONTRIBUTING.md\n[command-line reference]: https://yarm.readthedocs.io/en/latest/usage.html\n',
    'author': 'Bill Alive',
    'author_email': 'public+git@billalive.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/billalive/yarm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
