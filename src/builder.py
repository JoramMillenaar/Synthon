from src.effects import FadeInStreamDecorator, FadeOutStreamDecorator, DelayAudioStreamDecorator, MultiplyAudioStreamDecorator
from src.base import AudioStream


class EffectPipeline:
    # TODO: handle states better

    def __init__(self, ):
        self._decorators = {}

    def build(self, audio_source: AudioStream):
        for decorator in self._decorators.values():
            audio_source = decorator(audio_source)
        return audio_source

    def set_fade_in_duration(self, seconds: float):
        self._decorators['fadeIn'] = lambda s: FadeInStreamDecorator(s).set_fade_duration(seconds)

    def set_fade_out_duration(self, seconds: float):
        self._decorators['fadeOut'] = lambda s: FadeOutStreamDecorator(s).set_fade_duration(seconds)

    def set_delay_duration(self, seconds: float):
        self._decorators['delay'] = lambda s: DelayAudioStreamDecorator(s).set_delay_duration(seconds)

    def set_multiplier(self, value: float):
        self._decorators['multiply'] = lambda s: MultiplyAudioStreamDecorator(s).set_multiplier(value)
