from time import sleep

from mido import Message

from src.builder import EffectPipeline, OutputPipeline
from src.composer import AudioStreamComposer
from src.inputs import MidiSineWaveStream


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

    def handle_midi_message(self, message: Message):
        if message.type == 'note_on':
            sine_wave = MidiSineWaveStream(self.chunk_size, self.sample_rate)
            sine_wave.set_note(message.note).set_velocity(message.velocity)
            self.composer.add_stream(self.effect_pipeline.build(sine_wave), identifier=message.note)
        elif message.type == 'note_off':
            self.composer.close_stream(identifier=message.note)

    def run(self):
        try:
            for _ in self.output_pipeline.build(self.composer):
                pass
        except KeyboardInterrupt:
            sleep(.1)  # Helps give the threads time to properly shut down
