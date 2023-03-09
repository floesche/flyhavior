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

        self.fictrac_frame = None

        self.rotation = None
        self.speed = None
        self.fps = None
        self.left_right = None
        self.panel_angle = None
        self.interval_angle = None

        self.fg_color = None
        self.bg_color = None

        self.brightness = None
        self.contrast = None

        self.start_orientation = None
        
        self.start_mask = 0
        self.end_mask = 0

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

            "de-panel-speed": self._speed,
            "de-rotate-to": self._rotate_to,
            "de-panels-oscillation": self._oscillation,

            "de-spatial-setup-fgcolor": self._fg_color,
            "de-spatial-setup-bgcolor": self._bg_color,

            "closedloop-gain": self._gain,
            "fictrac-frame": self._fictrac_frame,

            # "camera-set-lid-old": self._start_closed_rotation

            #"camera-tick-rotation": self._set_rotate, ## Old
            "panels-tick-rotation": self._set_rotate,
            "loop-render": self._set_rendered,
            "loop-tick-delta": self._start_rotation,
            
            "de-spatial-setup-mask-start": self._start_mask,
            "de-spatial-setup-mask-end": self._end_mask,
        }
        self.counter = 0

    def transform(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.switcher.get(key, self._other_transforms)(tsLog, tsClient, tsReq, key, value)

    def _other_transforms(self,  tsLog, tsClient, tsReq, key, value):
        pass

    def _block_repetition(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.block_repetition = int(value)
        
    def _gain(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.gain = float(value)

    def _rotate_to(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.start_orientation = float(value)

    def _comment(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.comment = value.strip()
        # gain_match = re.findall("gain\s+([-]?\d+.*$)", self.comment)
        # if gain_match:
        #     self.gain = gain_match[0]
        # else:
        #     self.gain = None
        first_word = re.findall("(?:^|(?:[.!?]\s))(\w+)", self.comment)
        if first_word:
            self.stimulus_type = first_word[0].lower()
        else:
            self.stimulus_type = None
        tlr = re.findall("left-right\s+(\d*)", self.comment)
        if tlr:
            self.left_right = int(tlr[0])

    def _fictrac_frame(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.fictrac_frame = int(value)

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
        self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, comment=self.comment, repetition=self.block_repetition, stimulus_type=stimulus_type, fg_color=self.fg_color, bg_color=self.bg_color, brightness = self.brightness, contrast = self.contrast, left_right=self.left_right)

    def _speed(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.speed = float(value)
        ## FIXME: This whole thing doesn't really work.
        if self.condition_type == "PRE": # and value != "0":
        #if self.condition_type == "PRE" and int(tsReq) < 1000000000000000000: # Maybe this works for closed loop protocol 12?
        #if self.condition_type == "PRE":
            if self.counter == 0:
                self.counter += 1
                return
            self.counter = 0
            self.condition.save()
            self.condition_type = self.trial_type
            gain = self.gain if self.condition_type == "CLOSED" else None
            stimulus_type = self.stimulus_type if self.trial_type == "OPEN" else None
            self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, fps=self.fps, bar_size=self.panel_angle, interval_size=self.interval_angle, comment=self.comment, repetition=self.block_repetition, gain=gain, stimulus_type=stimulus_type, start_orientation=self.start_orientation, fg_color=self.fg_color, bg_color=self.bg_color, brightness = self.brightness, contrast = self.contrast, left_right=self.left_right, start_mask = self.start_mask, end_mask = self.end_mask)
        elif self.condition_type in ["CLOSED", "OPEN"] and int(tsReq) > 1000000000000000000 and value == "0":
            self.condition.save()
            self.condition_type="POST"
            stimulus_type = self.stimulus_type if self.trial_type == "OPEN" else None
            self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, fps=self.fps, bar_size=self.panel_angle, interval_size=self.interval_angle, comment=self.comment, repetition=self.block_repetition, stimulus_type=stimulus_type, fg_color=self.fg_color, bg_color=self.bg_color, brightness = self.brightness, contrast = self.contrast, left_right=self.left_right, start_mask = self.start_mask, end_mask = self.end_mask)
        elif self.condition_type == "CLOSED" and int(tsReq) < 1000000000000000000:   # Start rotation FIXME: Should be in RotationTranformer
            if isinstance(self.rotation, Rotation):
                self.rotation.save()
                self.rotation = None
            if isinstance(self.condition, Condition):
                self.rotation = Rotation.create(condition=self.condition, client_ts_ms=int(tsClient), fictrac_seq=int(tsReq), speed=self.speed)
    
    def _oscillation(self, tsLog, tsClient, tsReq, key, value) -> None:
        if self.stimulus_type != "oscillation":
            return
        if self.condition_type == "PRE":
            if self.counter == 0:
                self.counter += 1
                return
            self.counter = 0
            self.speed = float(value)
            
            self.condition.save()
            self.condition_type = "OPEN"
            gain = None
            stimulus_type = self.stimulus_type
            self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, fps=self.fps, bar_size=self.panel_angle, interval_size=self.interval_angle, comment=self.comment, repetition=self.block_repetition, gain=gain, stimulus_type=stimulus_type, start_orientation=self.start_orientation, fg_color=self.fg_color, bg_color=self.bg_color, brightness = self.brightness, contrast = self.contrast, left_right=self.left_right, start_mask = self.start_mask, end_mask = self.end_mask)
        elif self.condition_type in ["OPEN"]:
            self.condition.save()
            self.condition_type="POST"
            self.speed = 0.0
            stimulus_type = self.stimulus_type
            self.condition = Condition.create(experiment=self.experiment, trial_number=self.trial_number, trial_type=self.trial_type, condition_number=self.condition_number, condition_type=self.condition_type, fps=self.fps, bar_size=self.panel_angle, interval_size=self.interval_angle, comment=self.comment, repetition=self.block_repetition, stimulus_type=stimulus_type, fg_color=self.fg_color, bg_color=self.bg_color, brightness = self.brightness, contrast = self.contrast, left_right=self.left_right, start_mask = self.start_mask, end_mask = self.end_mask)

    def _set_rotate(self, tsLog, tsClient, tsReq, key, value) -> None: # FIXME: should be in RotationTransformer
        if isinstance(self.rotation, Rotation):
            self.rotation.angle = float(value)
    
    def _set_rendered(self, tsLog, tsClient, tsReq, key, value) -> None: # FIXME: should be in RotationTransformer
        if isinstance(self.rotation, Rotation):
            self.rotation.rendered = True

    def _start_rotation(self, tsLog, tsClient, tsReq, key, value) -> None: # FIXME: should be in RotationTransformer
        if isinstance(self.condition, Condition) and self.condition_type in ["PRE", "POST", "OPEN"]:
            if isinstance(self.rotation, Rotation):
                self.rotation.save()
                self.rotation = None
            self.rotation = Rotation.create(condition=self.condition, client_ts_ms=int(tsClient), speed=self.speed, fictrac_seq=self.fictrac_frame)

    def _condition_end(self, tsLog, tsClient, tsReq, key, value) -> None:
        assert self.condition_number == round((float(value)-self.trial_number) * 10), f"Error in condition {value}: should be {self.condition_number}"
        if isinstance(self.rotation, Rotation):
            self.rotation.save()
            self.rotation = None
        if isinstance(self.condition, Condition):
            self.condition.save()
            self.condition = None
            self.speed = 0.0

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

    def _bg_color(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.bg_color = int(value)
        if self.brightness is not None:
            self.contrast = 1 #round((self.brightness - (self.bg_color >> 8)) / (self.brightness + (self.bg_color >> 8)), 1)
        if isinstance(self.condition, Condition):
            self.condition.bg_color = self.bg_color
            self.condition.contrast = self.contrast

    def _fg_color(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.fg_color = int(value)
        self.brightness = self.fg_color >> 8
        if self.bg_color is not None:
            self.contrast = 1 #round((self.brightness - (self.bg_color >> 8)) / (self.brightness + (self.bg_color >> 8)), 1)
        if isinstance(self.condition, Condition):
            self.condition.fg_color = self.fg_color
            self.condition.brightness = self.brightness
            self.condition.contrast = self.contrast
            
    def _start_mask(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.start_mask = float(value)
        if isinstance(self.condition, Condition):
            self.condition.start_mask = self.start_mask
            
    def _end_mask(self, tsLog, tsClient, tsReq, key, value) -> None:
        self.end_mask = float(value)
        if isinstance(self.condition, Condition):
            self.condition.end_mask = self.end_mask

    def get_keys(self):
        return self.switcher.keys()
