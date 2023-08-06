# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psychopy_bids',
 'psychopy_bids.bids',
 'psychopy_bids.bids_event',
 'psychopy_bids.bids_settings']

package_data = \
{'': ['*'],
 'psychopy_bids': ['png/*'],
 'psychopy_bids.bids': ['template/*'],
 'psychopy_bids.bids_event': ['classic/*', 'dark/*', 'light/*'],
 'psychopy_bids.bids_settings': ['classic/*', 'dark/*', 'light/*']}

install_requires = \
['PsychoPy>=2022.2.3,<2023.0.0', 'pandas>=1.4.3,<2.0.0']

entry_points = \
{'psychopy': ['bids = psychopy_bids.bids'],
 'psychopy.experiment.components': ['bids_event = psychopy_bids.bids_event'],
 'psychopy.experiment.routines': ['bids_settings = '
                                  'psychopy_bids.bids_settings']}

setup_kwargs = {
    'name': 'psychopy-bids',
    'version': '0.1.1',
    'description': 'A PsychoPy plugin to work with the Brain Imaging Data Structure (BIDS)',
    'long_description': '# psychopy_bids\n\nA [PsychoPy](https://www.psychopy.org/) plugin to work with the [Brain Imaging Data Structure (BIDS)](https://bids-specification.readthedocs.io/)\n\n## Installation\n\n```bash\n$ pip install psychopy_bids\n```\n\n## Usage\n\n`psychopy_bids` can be used to create valid BIDS datasets by adding the possibility of using [task events](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html) in PsychoPy.\n\n```python\nfrom psychopy_bids import bids\n\nhandler = bids.BIDSHandler(dataset="example", subject="01", task="A")\nhandler.createDataset()\n\nevent_list = [{\'trigger\': bids.BIDSTaskEvent(onset=1.0, duration=0, trial_type="trigger")}]\nparticipant_info = {\'participant_id\': handler.subject, \'age\': 18}\n\nhandler.addTaskEvents(event_list, participant_info)\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`psychopy_bids` was created by Christoph Anzengruber & Florian Schöngaßner. It is licensed under the terms of the GNU General Public License v3.0 license.\n\n## Credits\n\n`psychopy_bids` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Christoph Anzengruber & Florian Schöngaßner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
