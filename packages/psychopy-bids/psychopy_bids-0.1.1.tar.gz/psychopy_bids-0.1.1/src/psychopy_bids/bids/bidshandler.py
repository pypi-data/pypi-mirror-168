"""
    This module provides a class to handle the communication between the PsychoPy ExperimentHandler
    and the BIDS data structure
"""

import os
import glob
import json
import sys
import shutil
import platform
import re
import warnings

from ast import literal_eval
from datetime import datetime

import pandas as pd
import numpy as np

from . import BIDSTaskEvent


class BIDSHandler():
    """
        A class to handle the BIDSTaskEvents saved in the PsychoPy ExperimentHandler.

        Attributes
        ----------
        `dataset` : str
            A set of neuroimaging and behavioral data acquired for a purpose of a particular study.
        `subject` : str
            A person or animal participating in the study.
        `task` : int
            A set of structured activities performed by the participant.
        `session` : int
            A logical grouping of neuroimaging and behavioral data consistent across subjects.
        `data_type` : str
            A functional group of different types of data.
        `acq` : str
            Custom label to distinguish different conditions present during multiple runs of the
            same task
        """

    def __init__(self, dataset, subject, task, session=None, data_type='beh', acq=None):
        self.dataset = dataset
        self.subject = subject
        self.task = task
        self.session = session
        self.data_type = data_type
        self.acq = acq

# ----------------------------------------------------------------------------------------------- #

    def addJSONSidecar(self, event_file, existing_file=None, exp=None):
        """
        Add an accompanying JSON sidecar file for task event file documentation.

        Parameters
        ----------
        `event_file` : str
            path of the accompanying task event file.
        `existing_file` : str
            path to an existing sidecar JSON file.
        `exp` : ExperimentHandler
            a set of structured activities performed by the participant.

        Examples
        --------
        >>> handler.addJSONSidecar("sub-01_ses-1_task-simple_run-1_events.tsv", "temp.json", exp)
        """
        # Create a framework for the sidecar file
        if existing_file and existing_file != "":
            with open(existing_file, mode="r", encoding="utf-8") as json_reader:
                try:
                    sidecar = json.load(json_reader)
                except ValueError:
                    sys.exit("File MUST be a valid JSON file")
        else:
            sidecar = {}
            df = pd.read_csv(event_file, sep='\t')
            column_names = df.columns.values
            for name in column_names:
                sidecar[name] = {"LongName": "", "Description": ""}

        # Add Stimulus presentation details
        osSystem = f"{platform.system()} {platform.release()}"
        if exp and exp.extraInfo['psychopyVersion']:
            sidecar["StimulusPresentation"] = {"OperationgSystem": osSystem,
                                               "SoftwareName": "PsychoPy",
                                               "SoftwareRRID": "SCR_006571",
                                               "SoftwareVersion": exp.extraInfo['psychopyVersion']}
        else:
            sidecar["StimulusPresentation"] = {"OperationgSystem": osSystem}

        # Save the file in the same folder as the .tsv file
        file_pth = event_file.split('.')[0]
        if not os.path.exists(f'{file_pth}.json'):
            with open(f'{file_pth}.json', mode="w", encoding="utf-8") as json_file:
                json.dump(sidecar, json_file)

# ----------------------------------------------------------------------------------------------- #

    def addStimuliFolder(self, event_file):
        """
        Add a stimuli folder (under the root folder of the dataset)

        Parameters
        ----------
        `event_file` : str
            path of the accompanying task event file.

        Examples
        --------
        >>> handler.addStimuliFolder("sub-01_ses-1_task-simple_run-1_events.tsv")
        """
        df = pd.read_csv(event_file, sep='\t')
        if 'stim_file' in df.columns:
            stimuli = list(df['stim_file'].dropna().unique())
            if not os.path.exists(f'{self.dataset}{os.sep}stimuli'):
                os.makedirs(f'{self.dataset}{os.sep}stimuli')
            for st in stimuli:
                if os.path.isfile(st):
                    shutil.copyfile(st, f'{self.dataset}{os.sep}stimuli{os.sep}{st}')
                else:
                    warnings.warn(f"File {st} does not exist!")

# ----------------------------------------------------------------------------------------------- #

    def addTaskEvents(self, events, participant_info):
        """
        Add all task events of one task to the subject folder.

        Parameters
        ----------
        `task` : ExperimentHandler
            a set of structured activities performed by the participant.
        `participant_info` : dict
            a dictionary describing properties of each participant (such as age, sex, etc.)

        Return
        ------
        `file_name` : str
            path of the created tsv event file.

        Examples
        --------
        >>> event_list = [{'trigger': bids.BIDSTaskEvent(onset=1.0, duration=0}]
        >>> participant_info = {'participant_id': handler.subject, 'age': 18}
        >>> handler.addTaskEvents(event_list, participant_info)
        """
        participants_file = f'{self.dataset}{os.sep}participants.tsv'
        participant_info['participant_id'] = self.subject

        # Create the header of the tsv file and add the first subject
        if os.path.getsize(participants_file) == 0:
            df = pd.DataFrame()
            # Create dict for participants information
            participants = {}
            df = pd.concat([df, pd.DataFrame([participant_info])])
            for info in participant_info:
                participants.update({info: {"LongName": "", "Description": ""}})
            with open(f"{self.dataset}{os.sep}participants.json",
                      mode="w",
                      encoding="utf-8") as json_file:
                json.dump(participants, json_file)
            df.to_csv(participants_file, sep='\t', index=False)

        # Update the participants.tsv file
        else:
            df = pd.read_csv(participants_file, sep='\t')
            if self.subject not in df['participant_id'].tolist():
                df = df.append(participant_info, ignore_index=True)
                df = df.fillna('n/a')
                df.to_csv(participants_file, sep='\t', index=False)

        # Write the task events from the Experiment-Handler to the .tsv-file
        bids_events = []
        for entry in events:
            ev = [e.to_dict() for e in list(entry.values()) if isinstance(e, BIDSTaskEvent)]
            bids_events.extend(ev)

        # Set the path of the folder and the file
        if self.session:
            pth = (f'{self.dataset}{os.sep}'
                   f'{self.subject}{os.sep}'
                   f'{self.session}{os.sep}'
                   f'{self.data_type}')
        else:
            pth = f'{self.dataset}{os.sep}{self.subject}{os.sep}{self.data_type}'

        if not os.path.exists(pth):
            os.makedirs(pth)

        if self.session:
            file = f'{pth}{os.sep}{self.subject}_{self.session}_{self.task}'
        else:
            file = f'{pth}{os.sep}{self.subject}_{self.task}'

        if self.acq:
            file = "_".join([file, self.acq])

        run = len(glob.glob(f"{file}*_events.tsv")) + 1
        file_name = f'{file}_run-{run}_events.tsv'

        # Drop the empty columns and change None values to 'n/a'
        df = pd.DataFrame(bids_events)
        df.fillna(value=np.nan)
        df.dropna(how='all', axis=1, inplace=True)
        df = df.fillna('n/a')

        # Arrange the columns so that onset and duration are at the first two columns
        df = df[(['onset', 'duration'] + [col for col in df if col not in ['onset', 'duration']])]

        df.to_csv(file_name, sep='\t', index=False)
        return file_name

# ----------------------------------------------------------------------------------------------- #

    def createDataset(self):
        """
        Creates the rudimentary body of a new dataset.

        Examples
        --------
        >>> handler.createDataset()
        """
        if not os.path.exists(self.dataset):
            os.makedirs(self.dataset)
            with open(f'{self.dataset}{os.sep}participants.tsv', mode="w", encoding="utf-8"):
                pass

            bidsdir = sys.modules['psychopy_bids.bids'].__path__[0]
            readme_src = os.path.normpath(os.path.join(bidsdir, 'template', 'README'))
            readme_dest = os.path.join(self.dataset, 'README')
            shutil.copyfile(readme_src, readme_dest)
            ds_desc_src = os.path.normpath(os.path.join(bidsdir,
                                                        'template',
                                                        'dataset_description.json'))
            ds_desc_dest = os.path.join(self.dataset, 'dataset_description.json')
            shutil.copyfile(ds_desc_src, ds_desc_dest)

            with open(f'{self.dataset}{os.sep}CHANGES', mode="w", encoding="utf-8") as f:
                current_time = datetime.now()
                f.write(f"1.0.0 {current_time.year}-{current_time.month}-{current_time.day}\n")
                f.write(" - First initialization of the data set.\n")

# ----------------------------------------------------------------------------------------------- #

    def parseLog(self, file, level='BIDS', regex=None):
        """
        Updates a task with all task events (from a specific log file).

        Parameters
        ----------
            `file` : str
                file path of the log file.
            `level` : str
                level name of the bids task events.
            `regex` : str
                regular expression to parse the message string

        Return
        ------
            `events` : list
                a list of events like presented stimuli or participant responses

        Examples
        --------
        >>> events = handler.parseLog("simple.log", "BIDS")
        """

        events = []
        with open(file, mode="r", encoding="utf-8") as log_file:
            for line in log_file.readlines():
                event = re.split(r' \t|[ ]+', line, maxsplit=2)
                if event[1] == level:
                    if regex:
                        d = (dict(re.findall(regex, event[2])))
                    else:
                        d = {k: v for k, v in literal_eval(event[2]).items() if v is not None}
                    bids_event = BIDSTaskEvent(0, 0)
                    events.append({'bids_event': bids_event.from_dict(d)})
        return events

# ----------------------------------------------------------------------------------------------- #

    @property
    def dataset(self):
        """
        A set of neuroimaging and behavioral data acquired for a purpose of a particular study.
        """
        return self.__dataset

    @dataset.setter
    def dataset(self, dataset):
        self.__dataset = str(dataset)

    @property
    def subject(self):
        """
        A participant identifier of the form sub-<label>, matching a participant entity found in
        the dataset.
        """
        return self.__subject

    @subject.setter
    def subject(self, subject):
        match = re.match('^sub-[0-9a-zA-Z]+$', str(subject))
        if match:
            self.__subject = subject
        else:
            subject = re.sub('[^A-Za-z0-9]+', '', str(subject))
            self.__subject = f'sub-{subject}'

    @property
    def task(self):
        """
        A set of structured activities performed by the participant.
        """
        return self.__task

    @task.setter
    def task(self, task):
        regex = re.compile('^task-[0-9a-zA-Z]+$', re.I)
        match = regex.match(str(task))
        if match:
            self.__task = task
        else:
            task = re.sub('[^A-Za-z0-9]+', '', str(task))
            self.__task = f'task-{task}'

    @property
    def session(self):
        """
        A logical grouping of neuroimaging and behavioral data consistent across subjects.
        """
        return self.__session

    @session.setter
    def session(self, session):
        if session:
            regex = re.compile('^ses-[0-9a-zA-Z]+$', re.I)
            match = regex.match(str(session))
            if match:
                self.__session = session
            else:
                session = re.sub('[^A-Za-z0-9]+', '', str(session))
                self.__session = f'ses-{session}'
        else:
            self.__session = None

    @property
    def data_type(self):
        """
        A functional group of different types of data.
        """
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        dt = ['anat', 'beh', 'dwi', 'eeg', 'fmap', 'func', 'ieeg', 'meg', 'micr', 'perf', 'pet']
        msg = f"<data_type> MUST be one of the following: {dt}"
        if str(data_type) in dt:
            self.__data_type = str(data_type)
        else:
            sys.exit(msg)

    @property
    def acq(self):
        """
        A label to distinguish a different set of parameters used for acquiring the same modality.
        """
        return self.__acq

    @acq.setter
    def acq(self, acq):
        if acq:
            regex = re.compile('^acq-[0-9a-zA-Z]+$', re.I)
            match = regex.match(str(acq))
            if match:
                self.__acq = acq
            else:
                acq = re.sub('[^A-Za-z0-9]+', '', str(acq))
                self.__acq = f'acq-{acq}'
        else:
            self.__acq = None
