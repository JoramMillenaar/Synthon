from abc import ABC

from src.base import AudioStream
from src.outputs import AudioPlaybackDecorator, AudioFileOutputDecorator


class DecoratorPipeline(ABC):
    def __init__(self):
        self._decorators = {}

    def build(self, audio_source: AudioStream):
        for decorator in self._decorators.values():
            audio_source = decorator(audio_source)
        return audio_source


class OutputPipeline(DecoratorPipeline):
    def enable_speaker_playback(self):
        self._decorators['playback'] = lambda s: AudioPlaybackDecorator(s)

    def enable_file_output(self, filename: str):
        self._decorators['fileStream'] = lambda s: AudioFileOutputDecorator(s, filename=filename)
