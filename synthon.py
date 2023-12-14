import argparse

from src.builder import NoteAudioStreamBuilder, OutputPipeline
from src.midi import MidiInputHandler
from src.synth import Synthesizer


def parse_args():
    parser = argparse.ArgumentParser(description='Synthesizer and MIDI handler with effects.')

    # Adding arguments for the effect pipeline
    parser.add_argument('--volume', type=float, default=0.3, help='Set output volume of a note')

    parser.add_argument('--attack', type=float, default=0.1, help='Duration of the attack of a note')
    parser.add_argument('--decay', type=float, default=0.3, help='Duration of the decay of a note')
    parser.add_argument('--sustain-volume', type=float, default=0.7, help='Volume of the sustain part of a note')
    parser.add_argument('--release', type=float, default=0.3, help='Duration of the release of a note')

    # Arguments for the synthesizer
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

    # Setting up the effect pipeline
    note_pipeline = NoteAudioStreamBuilder(sample_rate=args.sample_rate, chunk_size=args.chunk_size)
    note_pipeline.set_volume(args.volume)
    note_pipeline.set_adsr(
        attack_time=args.attack,
        decay_time=args.decay,
        sustain_level=args.sustain_volume,
        release_time=args.release,
    )
    note_pipeline.set_harmonics({0.5: 0.1, 2: 0.8, 3: 0.7, 5: 0.3, 6: 0.1})

    output = OutputPipeline()
    if not args.disable_speaker:
        output.enable_speaker_playback()

    if args.output:
        output.enable_file_output(args.output)

    # Setting up the synthesizer
    synth = Synthesizer(
        effect_pipeline=note_pipeline,
        output_pipeline=output,
        sample_rate=args.sample_rate,
        chunk_size=args.chunk_size
    )

    # Setting up the MIDI handler
    midi_handler = MidiInputHandler(port_name=args.port_name)
    midi_handler.register_observer(synth.handle_midi_message, channel=0)

    print('Started the Synth!')
    synth.run()


if __name__ == "__main__":
    main()
