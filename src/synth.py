from time import sleep
from typing import Iterator

from mido import Message

from src.base import AudioStream
from src.composer import AudioStreamComposer
from src.midi import MidiInputHandler
from src.notes import MusicNoteFactory
from src.services import midi_note_to_frequency


class SynthesizerStream(AudioStream):
    def __init__(self,
                 note_factory: MusicNoteFactory,
                 midi_handler: MidiInputHandler,
                 channel: int = 0,
                 sample_rate: int = 44100,
                 chunk_size: int = 512
                 ):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.note_factory = note_factory
        self.midi_handler = midi_handler
        self.midi_handler.register_observer(self.handle_midi_message, channel=channel)

        self.composer = AudioStreamComposer(sample_rate, chunk_size)

    def _create_sound_stream(self, note: int, velocity: int):
        return self.note_factory.create_note(
            frequency=midi_note_to_frequency(note), amplitude=velocity / 127
        )

    def handle_midi_message(self, message: Message):
        if message.type == 'note_on':
            stream = self._create_sound_stream(message.note, message.velocity)
            self.composer.add_stream(stream, identifier=message.note)
        elif message.type == 'note_off':
            self.composer.close_stream(identifier=message.note)

    def iterable(self) -> Iterator:
        return self.composer

    def close(self):
        sleep(.1)  # Helps give the threads time to properly shut down
        super().close()
