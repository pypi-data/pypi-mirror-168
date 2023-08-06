#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    PsychoPy routine for settings if BIDS class
"""

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2021 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).
#


from pathlib import Path
from psychopy.localization import _translate
from psychopy.experiment import Param
from psychopy.experiment.routines._base import BaseStandaloneRoutine

_localized = {}

_localized.update({
    'path': _translate('Path')})


class BidsExportRoutine(BaseStandaloneRoutine):
    """An event class for inserting arbitrary code into Builder experiments"""

    categories = ['BIDS']
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'BIDS.png'
    tooltip = _translate('BIDS export: creates BIDS structure, writes tsv file and update further files')

    def __init__(self, exp, name='bids',
                 experiment_bids="bids",
                 data_type="beh",
                 acq="",
                 event_json=""
                 ):
        # Initialise base routine
        BaseStandaloneRoutine.__init__(self, exp, name=name)

        self.exp.requireImport(importName='BIDSHandler',
                               importFrom='bids')

        self.type = 'BIDSexport'

        # params
        # self.params = {}

        # Basic params
        self.order += [
            'data_type',
            'experiment_bids',
            'acq',
            'event_json'
        ]

        self.params['name'].hint = _translate("Name of the task. No two tasks should have the same name.")
        self.params['name'].label = _translate('task name')

        hnt = _translate("Name of the experiment (parent folder), if this (task) is part of a larger one.")
        self.params['experiment_bids'] = Param(
            experiment_bids, valType='str', inputType="single", categ="Basic", allowedTypes=[],
            canBePath=False,
            hint=hnt,
            label=_translate("experiment name"))

        hnt = _translate("BIDS defined data type")
        self.params['data_type'] = Param(
            data_type, valType='str', inputType="choice", categ='Basic',
            allowedVals=['func', 'dwi', 'fmap', 'anat', 'perf', 'meg', 'eeg', 'ieeg', 'beh', 'pet', 'micr'],
            hint=hnt,
            label=_translate("data type"))

        hnt = _translate("Custom label to distinguish different conditions present during"
                         " multiple runs of the same task")
        self.params['acq'] = Param(
            acq, valType='str', inputType="single", categ='Basic',
            allowedVals=[],
            canBePath=False,
            hint=hnt,
            label=_translate("acquisition mode"))

        hnt = _translate("Name of the default event JSON file. Will be copied into each subject folder.")
        self.params['event_json'] = Param(
            event_json, valType='str', inputType="single", categ='Basic',
            allowedVals=[],
            hint=hnt,
            label=_translate('event JSON'))

        # these inherited params are harmless but might as well trim:
        for parameter in ('startType', 'startVal', 'startEstim', 'stopVal',
                          'stopType', 'durationEstim',
                          'saveStartStop', 'syncScreenRefresh'):
            if parameter in self.params:
                del self.params[parameter]

    def writeStartCode(self, buff):
        """ Code for the start of the experiment """
        inits = self.params

        code = (
            "# create initial folder structure\n"
            "if expInfo['session']:\n"
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "bids_handler = BIDSHandler(dataset=%(experiment_bids)s,\n"
            " subject=expInfo['participant'], task=expInfo['expName'],\n"
            " session=expInfo['session'], data_type=%(data_type)s, acq=%(acq)s)\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "else:"
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "bids_handler = BIDSHandler(dataset=%(experiment_bids)s,\n"
            " subject=expInfo['participant'], task=expInfo['expName'],\n"
            " data_type=%(data_type)s, acq=%(acq)s)\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "bids_handler.createDataset()\n"
        )
        buff.writeIndentedLines(code % inits)

    def writeRoutineEndCode(self, buff):
        """write code at the end of the experiment"""
        inits = self.params

        code = (
            "# get participant_info and events from the ExperimentHandler\n"
            "ignore_list = ['participant', 'session', 'date', 'expName', 'psychopyVersion', 'OS', 'frameRate']\n"
            "participant_info = {key: thisExp.extraInfo[key] for key in thisExp.extraInfo if key not in ignore_list}\n"
            "# write tsv file and update\n"
            "event_file = bids_handler.addTaskEvents(thisExp.getAllEntries(), participant_info)\n"
            "bids_handler.addJSONSidecar(event_file, %(event_json)s, thisExp)\n"
            "bids_handler.addStimuliFolder(event_file)\n"
        )
        buff.writeIndentedLines(code % inits)
