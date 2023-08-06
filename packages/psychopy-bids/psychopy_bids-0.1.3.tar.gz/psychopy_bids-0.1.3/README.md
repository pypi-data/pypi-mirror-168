# psychopy_bids

A [PsychoPy](https://www.psychopy.org/) plugin to work with the [Brain Imaging Data Structure (BIDS)](https://bids-specification.readthedocs.io/)

## Installation

```bash
$ pip install psychopy_bids
```

## Usage

`psychopy_bids` can be used to create valid BIDS datasets by adding the possibility of using [task events](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html) in PsychoPy.

```python
from psychopy_bids import bids

handler = bids.BIDSHandler(dataset="example", subject="01", task="A")
handler.createDataset()

event_list = [{'trigger': bids.BIDSTaskEvent(onset=1.0, duration=0, trial_type="trigger")}]
participant_info = {'participant_id': handler.subject, 'age': 18}

handler.addTaskEvents(event_list, participant_info)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`psychopy_bids` was created by Christoph Anzengruber & Florian Schöngaßner. It is licensed under the terms of the GNU General Public License v3.0 license.

## Credits

`psychopy_bids` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
