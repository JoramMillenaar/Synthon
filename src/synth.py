from time import sleep

from mido import Message

from src.builder import EffectPipeline
from src.composer import AudioStreamComposer
from src.inputs import MidiSineWaveStream
from src.outputs import AudioPlaybackDecorator, AudioFileOutputDecorator


class Synthesizer:
    def __init__(self, sample_rate: int, chunk_size: int):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self._effects = None
        self.file_name = None
        self.composer = AudioStreamComposer(sample_rate, chunk_size)
        self.playback_enabled = False

    def set_effect_pipeline(self, effects: EffectPipeline):
        self._effects = effects
        return self

    def enable_speaker_output(self):
        self.playback_enabled = True
        return self

    def stream_to_file(self, filename: str):
        self.file_name = filename
        return self

    def handle_midi_message(self, message: Message):
        if message.type == 'note_on':
            sine_wave = MidiSineWaveStream(self.chunk_size, self.sample_rate)
            sine_wave.set_note(message.note).set_velocity(message.velocity)
            self.composer.add_stream(self._effects.build(sine_wave), note=message.note)
        elif message.type == 'note_off':
            self.composer.close_stream(message.note)

    def run(self):
        # TODO: clean this up
        print('Started the Synth!')
        output_stream = AudioPlaybackDecorator(self.composer) if self.playback_enabled else self.composer
        output_stream = AudioFileOutputDecorator(output_stream, self.file_name) if self.file_name else output_stream
        try:
            for index, _ in enumerate(output_stream):
                if not index % 10:
                    print('', end='\r')
        except KeyboardInterrupt:
            print('Synth stopped. Finishing things up...')
            self.close()

    def close(self):
        sleep(.1)  # Helps give the threads time to properly shut down

    def __del__(self):
        self.close()
