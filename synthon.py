import argparse

from src.builder import OutputPipeline
from src.midi import MidiInputHandler
from src.notes import MusicNoteFactory
from src.synth import Synthesizer
from src.timbres import default_timbre


def parse_args():
    parser = argparse.ArgumentParser(description='Synthesizer and MIDI handler with effects.')

    parser.add_argument('--volume', type=float, default=0.3, help='Set output volume of a note')
    parser.add_argument('--sample_rate', type=int, default=44100, help='Sample rate for the synthesizer')
    parser.add_argument('--chunk_size', type=int, default=512, help='Chunk size for the synthesizer')

    # Toggle options
    parser.add_argument('--disable_speaker', action='store_true', help='Disable output to speaker')
    parser.add_argument('--output', type=str, help='Filename for the output file')

    # MIDI handler argument
    parser.add_argument('--port_name', type=str, default='IAC Driver Bus 1', help='MIDI input port name')

    return parser.parse_args()


def main():
    args = parse_args()

    note_factory = MusicNoteFactory(sample_rate=args.sample_rate, chunk_size=args.chunk_size, timbre=default_timbre)

    output = OutputPipeline()
    if not args.disable_speaker:
        output.enable_speaker_playback()

    if args.output:
        output.enable_file_output(args.output)

    synth = Synthesizer(
        volume=args.volume,
        note_factory=note_factory,
        output_pipeline=output,
        sample_rate=args.sample_rate,
        chunk_size=args.chunk_size
    )

    midi_handler = MidiInputHandler(port_name=args.port_name)
    midi_handler.register_observer(synth.handle_midi_message, channel=0)

    print('Started the Synth!')
    synth.run()


if __name__ == "__main__":
    main()
