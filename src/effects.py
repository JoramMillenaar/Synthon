import numpy as np

from src.base import AudioStream, AudioStreamDecorator


class FadeInStreamDecorator(AudioStreamDecorator):
    def __init__(self, stream: AudioStream):
        super().__init__(stream)
        self._fade_duration = .0
        self._elapsed = 0

    def set_fade_duration(self, value: float):
        self._fade_duration = value
        return self

    @property
    def _fade_samples(self):
        return int(self._fade_duration * self.sample_rate)

    @property
    def _fade_curve(self):
        return np.linspace(0, 1, self._fade_samples)

    def transform(self, stream_item):
        if self._elapsed <= self._fade_samples:
            fade_end = min(self._fade_samples - self._elapsed, len(stream_item))
            stream_item[:fade_end] *= self._fade_curve[self._elapsed:self._elapsed + fade_end]
            self._elapsed += len(stream_item)
        return stream_item


class FadeOutStreamDecorator(AudioStreamDecorator):
    is_infinite = False

    def __init__(self, stream: AudioStream):
        super().__init__(stream)
        self._fade_duration = .0
        self._elapsed = 0

    def set_fade_duration(self, value: float):
        self._fade_duration = value
        return self

    @property
    def _fade_samples(self):
        return int(self._fade_duration * self.sample_rate)

    @property
    def _fade_curve(self):
        return np.linspace(1, 0, self._fade_samples)

    def transform(self, stream_item):
        if self.is_closing:
            if self._elapsed < self._fade_samples:
                chunk_fade_length = min(self._fade_samples - self._elapsed, len(stream_item))
                fade_slice = self._fade_curve[self._elapsed:self._elapsed + chunk_fade_length]
                sub_chunk = stream_item[:chunk_fade_length] * fade_slice
                stream_item.fill(0)
                stream_item[:chunk_fade_length] += sub_chunk
                self._elapsed += chunk_fade_length
            else:
                stream_item.fill(0)
                self.close()
        return stream_item


class DelayAudioStreamDecorator(AudioStreamDecorator):
    is_infinite = False

    def __init__(self, stream: AudioStream):
        super().__init__(stream)
        self._delayed_duration = .0
        self._delay_buffer = np.array([], dtype=np.float32)

    def set_delay_duration(self, value: float):
        self._delayed_duration = value
        self._adjust_delay_buffer()
        return self

    @property
    def _delay_samples(self):
        return int(self.sample_rate * self._delayed_duration)

    @property
    def delay_buffer(self):
        self._adjust_delay_buffer()
        return self._delay_buffer

    def _adjust_delay_buffer(self):
        # TODO: is this magic needed now?
        required_size, current_size = self._delay_samples, len(self._delay_buffer)

        if current_size < required_size:
            self._delay_buffer = np.concatenate(
                [self._delay_buffer, np.zeros(required_size - current_size, dtype=np.float32)]
            )
        elif current_size > required_size:
            self._delay_buffer = self._delay_buffer[:required_size]

    def transform(self, stream_item):
        # TODO: clean this up
        self._delay_buffer = np.concatenate((self.delay_buffer, stream_item))
        output_chunk = self.delay_buffer[:self.chunk_size]
        self._delay_buffer = self.delay_buffer[self.chunk_size:]

        if self.is_closing or self.stream.is_closing or self.stream.is_closed:
            if len(self.delay_buffer) > 0:
                end = self.delay_buffer[:min(len(self.delay_buffer), self.chunk_size - len(output_chunk))]
                output_chunk = np.concatenate((output_chunk, end))
                self._delay_buffer = self.delay_buffer[self.chunk_size:]
            else:
                self.close()

        return output_chunk


class MultiplyAudioStreamDecorator(AudioStreamDecorator):
    def __init__(self, stream: AudioStream):
        super().__init__(stream)
        self._multiplier = 1

    def set_multiplier(self, value: float):
        self._multiplier = value
        return self

    def transform(self, stream_item):
        return stream_item * self._multiplier


class MergeStreamDecorator(AudioStreamDecorator):
    def __init__(self, stream: AudioStream, *other_streams: AudioStream):
        super().__init__(stream)
        self.other_streams = other_streams

    def transform(self, stream_item):
        return np.sum([stream_item, *[next(s) for s in self.other_streams]], axis=0)
