from time import sleep

from mido import Message

from src.builder import EffectPipeline, OutputPipeline
from src.composer import AudioStreamComposer
from src.inputs import NoteStream


class Synthesizer:
    def __init__(self,
                 effect_pipeline: EffectPipeline = EffectPipeline(),
                 output_pipeline: OutputPipeline = OutputPipeline(),
                 sample_rate: int = 44100,
                 chunk_size: int = 512
                 ):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.effect_pipeline = effect_pipeline
        self.output_pipeline = output_pipeline
        self.composer = AudioStreamComposer(sample_rate, chunk_size)

    def _create_sound_stream(self, note: int, velocity: int):
        stream = NoteStream(self.chunk_size, self.sample_rate)
        stream.set_note(note)
        stream.set_velocity(velocity)
        harmonics = ((2, 0.6), (3, 0.4), (4, 0.2))
        stream.add_harmonic_profile(harmonics)
        return stream

    def handle_midi_message(self, message: Message):
        if message.type == 'note_on':
            stream = self._create_sound_stream(message.note, message.velocity)
            self.composer.add_stream(self.effect_pipeline.build(stream), identifier=message.note)
        elif message.type == 'note_off':
            self.composer.close_stream(identifier=message.note)

    def run(self):
        try:
            for _ in self.output_pipeline.build(self.composer):
                pass
        except KeyboardInterrupt:
            sleep(.1)  # Helps give the threads time to properly shut down
