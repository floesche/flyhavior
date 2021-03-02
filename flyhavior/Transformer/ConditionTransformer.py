from Transformer.Transformer import Transformer

from Entities.Condition import Condition

class ConditionTransformer(Transformer):

    def __init__(self, experiment) -> None:

        self.experiment = experiment

        self.block_repetition = None
        self.comment = None
        self.trial_number = None
        self.trial_type = None

        self.condition_number = None
        self.condition_type = None
        self.condition = None

        self.fps = None
        self.panel_angle = None
        self.interval_angle = None

        self.switcher = {
            "block-repetition": self._block_repetition,
            "comment": self._comment,
            
            "condition-type": self._condition_type,
            "condtiion-type": self._condition_type,

            "trial-start": self._trial_start,
            "trial-end": self._trial_end,

            "condition-start": self._condition_start,
            "condition-end": self._condition_end,

            # "openloop-start": self._openloop_start,
            # "closedloop-start": self_closedloop_start,

            "loop-set-fps": self._fps,
            "panels-panel-angle": self._panel_angle,
            "panels-interval-angle": self._interval_angle,

            "de-speed": self._speed
            
        }

    def transform(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.switcher.get(key, self._other_transforms)(tsLog, tsClient, tsReq, key, value)

    def _other_transforms(self,  tsLog, tsClient, tsReq, key, value):
        pass

    def _block_repetition(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.block_repetition = int(value)
        
    def _comment(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.comment = value

    def _condition_type(self, tsLog, tsClient, tsReq, key, value) -> None:
        if value == "open-loop":
            self.trial_type = "OPEN"
        elif value == "closed-loop":
            self.trial_type = "CLOSED"
        else:
            self.trial_type = None

    def _trial_start(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.trial_number = int(value)

    def _trial_end(self, tsLog, tsClient, tsReq, key, value) -> None:
        assert self.trial_number == int(value), f"Error in trial {value}: should be {self.trial_number}."

    def _condition_start(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.condition_number = round((float(value)-self.trial_number) * 10)
        self.condition_type = "PRE"
        self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type)

    def _speed(self, tsLog, tsClient, tsReq, key, value) -> None:
        if self.condition_type == "PRE" and value != "0":
            # End Pre
            self.condition.save()
            self.condition_type = self.trial_type
            self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, fps=self.fps, bar_size=self.panel_angle, interval_size=self.interval_angle)
        elif self.condition_type in ["CLOSED", "OPEN"] and int(tsReq) > 1000000000000000000 and value == "0":
            self.condition.save()
            self.condition_type="POST"
            self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, fps=self.fps, bar_size=self.panel_angle, interval_size=self.interval_angle)
    
    def _condition_end(self, tsLog, tsClient, tsReq, key, value) -> None:
        assert self.condition_number == round((float(value)-self.trial_number) * 10), f"Error in condition {value}: should be {self.condition_number}"
        if isinstance(self.condition, Condition):
            self.condition.save()
            self.condition = None

    def _fps(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.fps = float(value)
        if isinstance(self.condition, Condition):
            self.condition.fps = self.fps

    def _panel_angle(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.panel_angle = float(value)
        if isinstance(self.condition, Condition):
            self.condition.bar_size = self.panel_angle

    def _interval_angle(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.interval_angle = float(value)
        if isinstance(self.condition, Condition):
            self.condition.interval_size = self.interval_angle


    def get_keys(self):
        return self.switcher.keys()