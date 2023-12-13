from time import sleep

from mido import Message

from src.builder import NoteProfilePipeline, OutputPipeline
from src.composer import AudioStreamComposer
from src.inputs import SineWaveStream
from src.services import midi_note_to_frequency


class Synthesizer:
    def __init__(self,
                 effect_pipeline: NoteProfilePipeline = NoteProfilePipeline(),
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
        sine_wave = SineWaveStream(chunk_size=self.chunk_size, sample_rate=self.sample_rate)
        sine_wave.set_volume(velocity / 127).set_frequency(midi_note_to_frequency(note))
        return self.effect_pipeline.build(sine_wave)

    def handle_midi_message(self, message: Message):
        if message.type == 'note_on':
            stream = self._create_sound_stream(message.note, message.velocity)
            self.composer.add_stream(stream, identifier=message.note)
        elif message.type == 'note_off':
            self.composer.close_stream(identifier=message.note)

    def run(self):
        try:
            for _ in self.output_pipeline.build(self.composer):
                pass
        except KeyboardInterrupt:
            sleep(.1)  # Helps give the threads time to properly shut down
