# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cz_legacy']

package_data = \
{'': ['*']}

install_requires = \
['commitizen>=2.0.0']

setup_kwargs = {
    'name': 'cz-legacy',
    'version': '0.1.7',
    'description': 'Extends Conventional Commits Change Types with User-Defined Legacy Types for Commitizen',
    'long_description': '# cz_legacy\n\nCustom Commitizen parser for user-specified legacy change types. The parser utilizes the `cz_conventional_commits` pattern and extends with the tag mapping specified in the configuration file\n\nWhile old change types will appear in the Changelog, the user will be prevented from using them in new commits. This is the reverse of the [revert/chore logic](https://github.com/commitizen-tools/commitizen#why-are-revert-and-chore-valid-types-in-the-check-pattern-of-cz-conventional_commits-but-not-types-we-can-select) from commitizen that allows use of those commit types, but won\'t display them in the changelog\n\n## Alternatives\n\nThis customization only works when old commits use the `<change_type>: <message>` format that can be parsed by commitizen. If that doesn\'t fit your use case, you may want to try out [incremental](https://commitizen-tools.github.io/commitizen/changelog/#incremental) which (I think) prepends to an existing `CHANGELOG`\n\n## Usage\n\n### Install\n\nInstall the package from PyPi: `pip install cz_legacy` or from git: `pip install git+https://github.com/KyleKing/cz_legacy.git@main`\n\n### Configuration\n\nAt minimum, you must have the `name = "cz_legacy"` and `[tool.commitizen.cz_legacy_map]` in your configuration file. The below example is for TOML, you can also utilize a YAML or JSON file.\n\nBelow is an example of the three change legacy types Chg, Fix, and New, but the user can choose any tag names and associated mapping for the Changelog\n\n```toml\n[tool.commitizen]\nname = "cz_legacy"\n# Other tool.commitizen configuration options\n\n[tool.commitizen.cz_legacy_map]\nChg = "Change (old)"\nFix = "Fix (old)"\nNew = "New (old)"\n```\n\n### Pre-Commit\n\nTo use in pre-commit, add this to your `pre-commit-config.yml`\n\n```yaml\nrepos:\n  - repo: https://github.com/commitizen-tools/commitizen\n    rev: v2.11.1\n    hooks:\n      - id: commitizen\n        additional_dependencies: [cz_legacy]\n        stages: [commit-msg]\n```\n\n## Issues\n\nIf you have any feature requests, run into any bugs, or have questions, feel free to start a discussion or open an issue on Github at [https://github.com/kyleking/cz_legacy](https://github.com/kyleking/cz_legacy).\n\n## Background\n\nI couldn\'t find a good way of adding a few legacy change types from an old commit style to commitizen so I built a package to [extend the ConventionalCommitsCz](https://github.com/commitizen-tools/commitizen/blob/master/commitizen/cz/conventional_commits/conventional_commits.py) to [provide custom logic](https://commitizen-tools.github.io/commitizen/customization/#2-customize-through-customizing-a-class). For reference, these are the [default settings](https://github.com/commitizen-tools/commitizen/blob/master/commitizen/defaults.py)\n\n## Roadmap\n\nSee the `Open Issues` and `Milestones` for current status and [./docs/CODE_TAG_SUMMARY.md](./docs/CODE_TAG_SUMMARY.md) for annotations in the source code.\n\nFor release history, see the [./docs/CHANGELOG.md](./docs/CHANGELOG.md)\n\n## Contributing\n\nSee the Developer Guide, Contribution Guidelines, etc\n\n- [./docs/DEVELOPER_GUIDE.md](./docs/DEVELOPER_GUIDE.md)\n- [./docs/STYLE_GUIDE.md](./docs/STYLE_GUIDE.md)\n- [./docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md)\n- [./docs/CODE_OF_CONDUCT.md](./docs/CODE_OF_CONDUCT.md)\n- [./docs/SECURITY.md](./docs/SECURITY.md)\n\n## License\n\n[LICENSE](https://github.com/KyleKing/calcipy/tree/main/LICENSE)\n',
    'author': 'Kyle King',
    'author_email': 'dev.act.kyle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyleking/cz_legacy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
