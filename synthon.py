import argparse
from src.builder import EffectPipeline, OutputPipeline
from src.midi import MidiInputHandler
from src.synth import Synthesizer


def parse_args():
    parser = argparse.ArgumentParser(description='Synthesizer and MIDI handler with effects.')

    # Adding arguments for the effect pipeline
    parser.add_argument('--multiplier', type=float, default=0.3, help='Effect multiplier')
    parser.add_argument('--fade_in', type=float, default=.2, help='Fade-in duration in seconds')
    parser.add_argument('--fade_out', type=float, default=.2, help='Fade-out duration in seconds')

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
    effects = EffectPipeline()
    effects.set_multiplier(args.multiplier)
    effects.set_fade_in_duration(seconds=args.fade_in)
    effects.set_fade_out_duration(seconds=args.fade_out)

    output = OutputPipeline()
    if not args.disable_speaker:
        output.enable_speaker_playback()

    if args.output:
        output.enable_file_output(args.output)

    # Setting up the synthesizer
    synth = Synthesizer(
        effect_pipeline=effects,
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
