import re

from Transformer.Transformer import Transformer

from Entities.Condition import Condition
from Entities.Rotation import Rotation

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

        self.rotation = None
        self.speed = None
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

            "de-speed": self._speed,

            # "camera-set-lid-old": self._start_closed_rotation


            "camera-tick-rotation": self._set_rotate,
            "loop-render": self._set_rendered,
            "loop-tick-delta": self._start_rotation,
            

            
        }

    def transform(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.switcher.get(key, self._other_transforms)(tsLog, tsClient, tsReq, key, value)

    def _other_transforms(self,  tsLog, tsClient, tsReq, key, value):
        pass

    def _block_repetition(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.block_repetition = int(value)
        
    def _comment(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.comment = value.strip()
        gain_match = re.findall("gain\s+(\d+.*$)", self.comment)
        if gain_match:
            self.gain = gain_match[0]
        else:
            self.gain = None
        first_word = re.findall("(?:^|(?:[.!?]\s))(\w+)", self.comment)
        if first_word:
            self.stimulus_type = first_word[0].lower()
        else:
            self.stimulus_type = None

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
        stimulus_type = self.stimulus_type if self.trial_type == "OPEN" else None
        self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, comment=self.comment, repetition=self.block_repetition, stimulus_type=stimulus_type)

    def _speed(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.speed = float(value)
        if self.condition_type == "PRE" and value != "0":
            self.condition.save()
            self.condition_type = self.trial_type
            gain = self.gain if self.condition_type == "CLOSED" else None
            stimulus_type = self.stimulus_type if self.trial_type == "OPEN" else None
            self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, fps=self.fps, bar_size=self.panel_angle, interval_size=self.interval_angle, comment=self.comment, repetition=self.block_repetition, gain=gain, stimulus_type=stimulus_type)
        elif self.condition_type in ["CLOSED", "OPEN"] and int(tsReq) > 1000000000000000000 and value == "0":
            self.condition.save()
            self.condition_type="POST"
            stimulus_type = self.stimulus_type if self.trial_type == "OPEN" else None
            self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, fps=self.fps, bar_size=self.panel_angle, interval_size=self.interval_angle, comment=self.comment, repetition=self.block_repetition, stimulus_type=stimulus_type)
        elif self.condition_type == "CLOSED" and int(tsReq) < 1000000000000000000:   # Start rotation FIXME: Should be in RopptationTranformer
            if isinstance(self.rotation, Rotation):
                self.rotation.save()
                self.rotation = None
            if isinstance(self.condition, Condition):
                self.rotation = Rotation.create(condition=self.condition, client_ts_ms=int(tsClient), fictrac_seq=int(tsReq), speed=self.speed)

    def _set_rotate(self, tsLog, tsClient, tsReq, key, value) -> None: # FIXME: should be in ROtaitonTransformer
        if isinstance(self.rotation, Rotation):
            self.rotation.angle = float(value)
    
    def _set_rendered(self, tsLog, tsClient, tsReq, key, value) -> None: # FIXME: should be in ROtaitonTransformer
        if isinstance(self.rotation, Rotation):
            self.rotation.rendered = True

    def _start_rotation(self, tsLog, tsClient, tsReq, key, value) -> None: # FIXME: should be in ROtaitonTransformer
        if isinstance(self.condition, Condition) and self.condition_type in ["PRE", "POST", "OPEN"]:
            if isinstance(self.rotation, Rotation):
                self.rotation.save()
                self.rotation = None
            self.rotation = Rotation.create(condition=self.condition, client_ts_ms=int(tsClient), speed=self.speed)
            

    def _condition_end(self, tsLog, tsClient, tsReq, key, value) -> None:
        assert self.condition_number == round((float(value)-self.trial_number) * 10), f"Error in condition {value}: should be {self.condition_number}"
        if isinstance(self.rotation, Rotation):
            self.rotation.save()
            self.rotation = None
        if isinstance(self.condition, Condition):
            self.condition.save()
            self.condition = None
            self.speed = None

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