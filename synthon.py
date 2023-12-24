import argparse

from src.dataclasses import Timbre, ADSRProfile, Vibrato, Tremolo, Harmonic
from src.effects import MultiplyAudioStreamDecorator
from src.midi import MidiInputHandler
from src.notes import MusicNoteFactory
from src.outputs import AudioPlaybackDecorator, AudioFileOutputDecorator
from src.services import load_template
from src.synth import SynthesizerStream


def parse_args():
    parser = argparse.ArgumentParser(description='Synthesizer and MIDI handler with effects.')

    parser.add_argument('--template', type=str, help='JSON template file (e.g. "default.json")')

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

    parser, user_args = parser, parser.parse_args()
    user_args, unknown = parser.parse_known_args()
    provided_args = {arg for arg in vars(user_args) if getattr(user_args, arg) != parser.get_default(arg)}

    # Load template if specified
    if user_args.template:
        template_settings = load_template(user_args.template)
        for key, value in template_settings.items():
            if key not in provided_args:
                setattr(user_args, key, value)

    return user_args


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


def create_timbre(args):
    return Timbre(
        envelope=ADSRProfile(
            attack=args.attack,
            decay=args.decay,
            sustain_amplitude=args.sustain_amplitude,
            sustain=args.sustain,
            release=args.release,
            sustain_till_close=not args.sustain,
        ),
        vibrato=Vibrato(rate=args.vibrato_rate,
                        depth=args.vibrato_depth) if args.vibrato_rate and args.vibrato_depth else None,
        tremolo=Tremolo(rate=args.tremolo_rate,
                        depth=args.tremolo_depth) if args.tremolo_rate and args.tremolo_depth else None,
        harmonics=tuple(_parse_harmonics(args))
    )


def main():
    args = parse_args()

    note_factory = MusicNoteFactory(
        sample_rate=args.sample_rate,
        chunk_size=args.chunk_size,
        timbre=create_timbre(args)
    )

    stream = SynthesizerStream(
        note_factory=note_factory,
        midi_handler=MidiInputHandler(port_name=args.port_name),
        sample_rate=args.sample_rate,
        chunk_size=args.chunk_size
    )
    stream = MultiplyAudioStreamDecorator(stream, multiplier=args.volume)
    if not args.disable_speaker:
        stream = AudioPlaybackDecorator(stream)

    if args.output:
        stream = AudioFileOutputDecorator(stream, filename=args.output)

    print('Started the Synth!')
    stream.run()


if __name__ == "__main__":
    main()
