"""This module provides a class to save your TaskEvents in the BIDS data structure"""

import sys


class BIDSTaskEvent(object):
    """
        A BIDSTaskEvent describes timing and other properties of events recorded during a run.
        Events are, for example, stimuli presented to the participant or participant responses.

        Attributes
        ----------
        onset : int, float
            Onset (in seconds) of the event, measured from the beginning of the acquisition of the
            first data point stored in the corresponding task data file.
        duration : int, float, 'n/a'
            Duration of the event (measured from onset) in seconds.
        trial_type : str
            Primary categorisation of each trial to identify them as instances of the experimental
            conditions.
        sample : int
            Onset of the event according to the sampling scheme of the recorded modality.
        response_time : int, float, 'n/a'
            Response time measured in seconds.
        value : Any
            Marker value associated with the event.
        hed : str
            Hierarchical Event Descriptor (HED) Tag.
        stim_file : str
            Represents the location of the stimulus file (such as an image, video, or audio file)
            presented at the given onset time.
        identifier : str
            Represents the database identifier of the stimulus file presented at the given onset
            time.
        database : str
            Represents the database of the stimulus file presented at the given onset time.
    """

    def __init__(self,
                 onset,
                 duration,
                 trial_type=None,
                 sample=None,
                 response_time=None,
                 value=None,
                 hed=None,
                 stim_file=None,
                 identifier=None,
                 database=None):
        self.onset = onset
        self.duration = duration
        self.trial_type = trial_type
        self.sample = sample
        self.response_time = response_time
        self.value = value
        self.hed = hed
        self.stim_file = stim_file
        self.identifier = identifier
        self.database = database

# ----------------------------------------------------------------------------------------------- #

    def __repr__(self):
        values = [v for v in self.__dict__.values() if v is not None]
        return f"BIDSTaskEvent({str(values)[1:-1]})"

# ----------------------------------------------------------------------------------------------- #

    def from_dict(self, dictionary):
        """
        Converts a dictionary into a BIDSTaskEvent object.

        Parameters
        ----------
        dictionary : dict
            a dictionary representing a task event.

        Returns
        -------
        BIDSTaskEvent
            BIDSTaskEvent object representing all column names of a task event

        Examples
        --------
        >>> event = BIDSTaskEvent(0, 0)
        >>> event.from_dict({'onset': 1, 'duration': 1})
        BIDSTaskEvent(1, 1)
        """
        for key in dictionary.keys():
            setattr(self, key, dictionary[key])
        return self

# ----------------------------------------------------------------------------------------------- #

    def to_dict(self):
        """
        Converts a BIDSTaskEvent object to a dictionary.

        Returns
        -------
        dict
            Dictionary representing all column names of a task event

        Examples
        --------
        >>> BIDSTaskEvent(1, 1).to_dict()
        {'onset': 1, 'duration': 1, 'trial_type': None, 'sample': None, 'response_time': None,
        'value': None, 'hed': None, 'stim_file': None, 'identifier': None, 'database': None}
        """
        return {"onset": self.onset,
                "duration": self.duration,
                "trial_type": self.trial_type,
                "sample": self.sample,
                "response_time": self.response_time,
                "value": self.value,
                "hed": self.hed,
                "stim_file": self.stim_file,
                "identifier": self.identifier,
                "database": self.database}

# ----------------------------------------------------------------------------------------------- #

    @property
    def onset(self):
        """
        Onset (in seconds) of the event, measured from the beginning of the acquisition of the
        first data point stored in the corresponding task data file.
        """
        return self.__onset

    @onset.setter
    def onset(self, onset):
        if isinstance(onset, (int, float)):
            self.__onset = round(onset, 4)
        elif isinstance(onset, str):
            try:
                self.__onset = round(float(onset), 4)
            except ValueError:
                sys.exit("Property 'onset' MUST be a number")
        else:
            sys.exit("Property 'onset' MUST be a number")

# ----------------------------------------------------------------------------------------------- #

    @property
    def duration(self):
        """
        Duration of the event (measured from onset) in seconds.
        """
        return self.__duration

    @duration.setter
    def duration(self, duration):
        msg = "Property 'duration' MUST be either zero or positive (or n/a if unavailable)"
        if isinstance(duration, str):
            if duration == 'n/a':
                self.__duration = duration
            else:
                try:
                    self.__duration = round(float(duration), 4)
                except ValueError:
                    sys.exit(msg)
        elif ((isinstance(duration, (int, float))) and (duration >= 0)):
            self.__duration = round(duration, 4)
        else:
            sys.exit(msg)

# ----------------------------------------------------------------------------------------------- #

    @property
    def trial_type(self):
        """
        Primary categorisation of each trial to identify them as instances of the experimental
        conditions.
        """
        return self.__trial_type

    @trial_type.setter
    def trial_type(self, trial_type):
        if trial_type:
            if isinstance(trial_type, str):
                self.__trial_type = trial_type
            else:
                sys.exit("Property 'trial_type' MUST be a string")
        else:
            self.__trial_type = None

# ----------------------------------------------------------------------------------------------- #

    @property
    def sample(self):
        """
        Onset of the event according to the sampling scheme of the recorded modality.
        """
        return self.__sample

    @sample.setter
    def sample(self, sample):
        if sample:
            if isinstance(sample, int):
                self.__sample = sample
            elif isinstance(sample, str):
                try:
                    self.__onset = int(sample)
                except ValueError:
                    sys.exit("Property 'sample' MUST be an integer")
                else:
                    sys.exit("Property 'sample' MUST be an integer")
        else:
            self.__sample = None

# ----------------------------------------------------------------------------------------------- #

    @property
    def response_time(self):
        """
        Response time measured in seconds.
        """
        return self.__response_time

    @response_time.setter
    def response_time(self, response_time):
        if response_time:
            msg = "Property 'response_time' MUST be a number (or n/a if unavailable)"
            if isinstance(response_time, str):
                if response_time == 'n/a':
                    self.__response_time = response_time
                else:
                    try:
                        self.__response_time = round(float(response_time), 4)
                    except ValueError:
                        sys.exit(msg)
            elif isinstance(response_time, (int, float)):
                self.__response_time = round(response_time, 4)
            else:
                sys.exit(msg)
        else:
            self.__response_time = None

# ----------------------------------------------------------------------------------------------- #

    @property
    def value(self):
        """
        Marker value associated with the event.
        """
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        else:
            self.__value = None

# ----------------------------------------------------------------------------------------------- #

    @property
    def hed(self):
        """
        Hierarchical Event Descriptor (HED) Tag.
        """
        return self.__hed

    @hed.setter
    def hed(self, hed):
        if hed:
            if isinstance(hed, str):
                self.__hed = hed
            else:
                sys.exit("Property 'hed' MUST be a string")
        else:
            self.__hed = None

# ----------------------------------------------------------------------------------------------- #

    @property
    def stim_file(self):
        """
        Represents the location of the stimulus file (such as an image, video, or audio file)
        presented at the given onset time.
        """
        return self.__stim_file

    @stim_file.setter
    def stim_file(self, stim_file):
        if stim_file:
            if isinstance(stim_file, str):
                self.__stim_file = stim_file
            else:
                sys.exit("Property 'stim_file' MUST be a string")
        else:
            self.__stim_file = None

# ----------------------------------------------------------------------------------------------- #

    @property
    def identifier(self):
        """
        Represents the database identifier of the stimulus file presented at the given onset time.
        """
        return self.__identifier

    @identifier.setter
    def identifier(self, identifier):
        if identifier:
            if isinstance(identifier, str):
                self.__identifier = identifier
            else:
                sys.exit("Property 'identifier' MUST be a string")
        else:
            self.__identifier = None

# ----------------------------------------------------------------------------------------------- #

    @property
    def database(self):
        """
        Represents the database of the stimulus file presented at the given onset time.
        """
        return self.__database

    @database.setter
    def database(self, database):
        if database:
            if isinstance(database, str):
                self.__database = database
            else:
                sys.exit("Property 'database' MUST be a string")
        else:
            self.__database = None
