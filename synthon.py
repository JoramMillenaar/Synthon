import argparse

from src.builder import OutputPipeline
from src.dataclasses import Timbre, ADSRProfile, Vibrato, Tremolo, Harmonic
from src.midi import MidiInputHandler
from src.notes import MusicNoteFactory
from src.synth import Synthesizer


def parse_args():
    parser = argparse.ArgumentParser(description='Synthesizer and MIDI handler with effects.')

    # Synth configuration
    parser.add_argument('--volume', type=float, default=0.3, help='Set output volume of a note')
    parser.add_argument('--sample-rate', type=int, default=44100, help='Sample rate for the synthesizer')
    parser.add_argument('--chunk_size', type=int, default=512, help='Chunk size for the synthesizer')

    # Timbre configuration
    parser.add_argument('--attack', type=float, default=0.1, help='Attack time for ADSR envelope')
    parser.add_argument('--decay', type=float, default=0.4, help='Decay time for ADSR envelope')
    parser.add_argument('--sustain-amplitude', type=float, default=0.7, help='Sustain amplitude for ADSR envelope')
    parser.add_argument('--sustain', type=float, help='Optional sustain time for ADSR envelope')
    parser.add_argument('--release', type=float, default=0.5, help='Release time for ADSR envelope')

    parser.add_argument('--vibrato-rate', type=float, default=5.5, help='Rate of vibrato')
    parser.add_argument('--vibrato-depth', type=float, default=0.06, help='Depth of vibrato')

    parser.add_argument('--tremolo-rate', type=float, default=4.0, help='Rate of tremolo')
    parser.add_argument('--tremolo-depth', type=float, default=0.1, help='Depth of tremolo')

    parser.add_argument('--harmonic', action='append', default=['2,0.5,None', '3,0.3,.8'],
                        help='Add a harmonic in the format "multiple,amplitude,sustain duration (None for infinite)".'
                             ' Default is; --harmonic 2,0.5,None --harmonic 3,0.3,.8'
                        )

    # Toggle options
    parser.add_argument('--disable-speaker', action='store_true', help='Disable output to speaker')
    parser.add_argument('--output', type=str, help='Filename for the output file')

    # MIDI handler argument
    parser.add_argument('--port-name', type=str, default='IAC Driver Bus 1', help='MIDI input port name')

    return parser.parse_args()


def _parse_harmonics(args):
    harmonics = []
    if args.harmonic:
        for h in args.harmonic:
            multiple, amplitude, sustain = h.split(',')
            harmonics.append(
                Harmonic(
                    multiple=int(multiple),
                    amplitude=float(amplitude),
                    sustain=None if sustain == 'None' else float(sustain)
                )
            )
    return harmonics


def main():
    args = parse_args()

    timbre = Timbre(
        envelope=ADSRProfile(
            attack=args.attack,
            decay=args.decay,
            sustain_amplitude=args.sustain_amplitude,
            sustain=args.sustain,
            release=args.release,
            sustain_till_close=not args.sustain,
        ),
        vibrato=Vibrato(
            rate=args.vibrato_rate,
            depth=args.vibrato_depth,
        ),
        tremolo=Tremolo(
            rate=args.tremolo_rate,
            depth=args.tremolo_depth,
        ),
        harmonics=tuple(_parse_harmonics(args))
    )

    note_factory = MusicNoteFactory(sample_rate=args.sample_rate, chunk_size=args.chunk_size, timbre=timbre)

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
