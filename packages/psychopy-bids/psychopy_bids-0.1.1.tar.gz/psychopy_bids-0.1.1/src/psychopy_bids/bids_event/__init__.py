#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    PsychoPy Builder component events
"""

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2021 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

# from os import path
from pathlib import Path

from psychopy.experiment.components import BaseComponent, _translate, Param

# from psychopy import prefs

# only use _localized values for label values, nothing functional:
_localized = {'name': _translate('Name')}

_localized.update({'onset': _translate('Onset'),
                   'bids_duration': _translate('Duration'),
                   'trial_type': _translate('Trial type'),
                   'sample': _translate('Sample'),
                   'response_time': _translate('Response time'),
                   'value': _translate('Value'),
                   'hed': _translate('HED'),
                   'stim_file': _translate('Stimulus file'),
                   'identifier': _translate('Identifier'),
                   'database': _translate('Database'),
                   'add_log': _translate('Add to log file'),
                   })


class BidsEventComponent(BaseComponent):
    """An event class for inserting arbitrary code into Builder experiments"""

    categories = ['BIDS']
    targets = ['PsychoPy']  # , 'PsychoJS'
    iconFile = Path(__file__).parent / 'BIDS.png'
    tooltip = _translate('BIDS event: logging of BIDS events')

    def __init__(self, exp, parentName, name='bidsEvent',
                 onset=0, bids_duration=1, trial_type=None,
                 sample=None, response_time=None,
                 value=None, hed=None,
                 stim_file=None, identifier=None, database=None,
                 add_log=False):
        self.type = 'BIDSevent'
        self.exp = exp  # so we can access the experiment if necessary
        self.parentName = parentName  # to access the routine too if needed
        self.params = {}
        self.depends = []
        super(BidsEventComponent, self).__init__(
            exp, parentName, name=name)

        self.exp.requireImport(importName='BIDSTaskEvent',
                               importFrom='bids')

        # onset,duration,trial_type,sample,response_time,value,HED,stim_file,identifier,database

        _allow3 = ['constant']  # , 'set every repeat']  # list

        # Basic params
        self.order += ['onset', 'bids_duration', 'trial_type', 'response_time']

        hnt = _translate(
            "Onset (in seconds) of the event, measured from the beginning of the acquisition of the first data point"
            " stored in the corresponding task data file.")
        self.params['onset'] = Param(
            onset, valType='num', inputType="single", allowedTypes=[], categ='Basic',
            updates='constant', allowedUpdates=_allow3[:],  # copy the list
            hint=hnt,
            label=_localized['onset'])
        hnt = _translate(
            "Duration of the event (measured from onset) in seconds. Must always be either zero or positive (or n/a"
            " if unavailable).")
        self.params['bids_duration'] = Param(
            bids_duration, valType='num', inputType="single", allowedTypes=[], categ='Basic',
            updates='constant', allowedUpdates=_allow3[:],  # copy the list
            hint=hnt,
            label=_localized['bids_duration'])
        hnt = _translate(
            "Primary categorisation of each trial to identify them as instances of the experimental conditions.")
        self.params['trial_type'] = Param(
            trial_type, valType='str', inputType="single", allowedTypes=[], categ='Basic',
            updates='constant', allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized['trial_type'])
        hnt = _translate(
            "Response time measured in seconds.")
        self.params['response_time'] = Param(
            response_time, valType='num', inputType="single", allowedTypes=[], categ='Basic',
            updates='constant', allowedUpdates=_allow3[:],  # copy the list
            hint=hnt,
            label=_localized['response_time'])

        # Data params
        hnt = _translate(
            "Should the event be saved in the log file too?")
        self.params['add_log'] = Param(
            add_log, valType='bool', inputType="bool", categ='Data',
            hint=hnt,
            label=_translate("Add event to log"))

        # Stim params
        self.order += ['stim_file', 'identifier', 'database']

        hnt = _translate(
            "Represents the location of the stimulus file. The values correspond to a path relative to /stimuli.")
        self.params['stim_file'] = Param(
            stim_file, valType='str', inputType="single", allowedTypes=[], categ='Stim',
            updates='constant', allowedUpdates=_allow3[:],
            hint=hnt,
            label=_localized['stim_file'])
        hnt = _translate(
            "References within a database")
        self.params['identifier'] = Param(
            identifier, valType='str', inputType="single", allowedTypes=[], categ='Stim',
            updates='constant', allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized['identifier'])
        hnt = _translate(
            "References to a database")
        self.params['database'] = Param(
            database, valType='str', inputType="single", allowedTypes=[], categ='Stim',
            updates='constant', allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized['database'])

        # more params
        self.order += ['sample', 'value', 'hed']

        hnt = _translate(
            "Onset of the event according to the sampling scheme of the recorded modality (that is, referring to the"
            " raw data file that the events.tsv file accompanies).")
        self.params['sample'] = Param(
            sample, valType='num', inputType="single", allowedTypes=[], categ='More',
            updates='constant', allowedUpdates=_allow3[:],  # copy the list
            hint=hnt,
            label=_localized['sample'])
        hnt = _translate(
            "Marker value associated with the event (for example, the value of a TTL trigger that was recorded at the"
            " onset of the event).")
        self.params['value'] = Param(
            value, valType='str', inputType="single", allowedTypes=[], categ='More',
            updates='constant', allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized['value'])
        hnt = _translate(
            "Hierarchical Event Descriptor (HED) Tag")
        self.params['hed'] = Param(
            hed, valType='str', inputType="single", allowedTypes=[], categ='More',
            updates='constant', allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized['hed'])

        # these inherited params are harmless but might as well trim:
        for parameter in ('startType', 'startVal', 'startEstim', 'stopVal',
                          'stopType', 'durationEstim',
                          'saveStartStop', 'syncScreenRefresh'):
            if parameter in self.params:
                del self.params[parameter]

    def writeStartCode(self, buff):
        """ write code in the start of the experimental code """
        # inits = self.params

        code = (
            "bidsLogLevel = 24\n"
            "logging.addLevel('BIDS', 24)\n"
        )
        if self.params['add_log']:
            buff.writeIndentedLines(code)

    def writeRoutineEndCode(self, buff):
        """
         write code
        """
        init_params = self.params
        params = ["trial_type", "sample", "response_time", "value", "hed", "stim_file", "identifier", "database"]
        # what loop are we in (or thisExp)?
        if len(self.exp.flow._loopList):
            curr_loop = self.exp.flow._loopList[-1]  # last (outer-most) loop
        else:
            curr_loop = self.exp._expHandler

        if 'Stair' in curr_loop.type:
            add_data_func = 'addOtherData'
        else:
            add_data_func = 'addData'

        loop = curr_loop.params['name']
        name = self.params['name']
        code = (
            "bids_event = BIDSTaskEvent( onset=%(onset)s,\n"
        )
        for parameter in params:
            if init_params[parameter] != 'None':
                code += (
                    " " + parameter + "=%(" + parameter + ")s,"
                )

        code += (
            " duration=%(bids_duration)s)\n"
        )
        buff.writeIndentedLines(code % init_params)
        code = (
            f"{loop}.{add_data_func}('{name}.event', bids_event)\n"
        )
        buff.writeIndentedLines(code)

        if self.params['add_log']:
            code = (
                "logging.log(level=24, msg=bids_event.to_dict())\n"
            )

            buff.writeIndentedLines(code)
