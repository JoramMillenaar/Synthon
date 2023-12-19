<p align="center">
    <img src="logo.png" alt="drawing" width="250" />
</p>

# Synthon: The Dynamic Python Synthesizer 🎹🎶

Synthon transforms your MIDI inputs into a symphony of synthesized sounds, all powered by Python. Dive into a world
where digital audio meets creativity, with a synthesizer that's as versatile as it is powerful. Whether you're a
musician, a hobbyist, or an audio enthusiast, Synthon offers an immersive experience in sound synthesis.

## Key Highlights

- 🎚️ **Customizable Timbre**: Craft your unique sound with adjustable ADSR envelopes, vibrato, tremolo, and harmonics.
- 🎧 **Real-Time MIDI Support**: Connect any MIDI device and turn keystrokes into music.
- 🔊 **Robust Output Pipeline**: Direct your audio masterpiece to speakers or record it seamlessly.
- 🛠️ **Fine-Tune Your Experience**: Full control over sample rate, chunk size, and volume, all through an intuitive
  command-line interface.
- 📁 **Template-Based Configuration**: Easily set up and reuse configurations with JSON templates.
- 📁 **Save Your Creations**: Output your audio directly to a file for easy sharing and editing.

## Features

- **Output Pipeline**: Direct audio output to speakers or save it to a file.
- **Synthesizer**: High-quality sound generation with adjustable sample rate and chunk size.
- **MIDI Compatibility**: Use any MIDI input device to control the synthesizer.
- **Customizable Timbre**: Fine-tune the sound with adjustable ADSR envelope, vibrato, tremolo, and harmonics.
- **Template-Based Configuration**: Simplify setup using customizable JSON templates for different sound configurations.

## Getting Started

### Prerequisites

- Python 3.x
- MIDI input device (or use our companion project to turn your computer's keyboard into a MIDI device)

### Dependencies

```commandline
pip install mido sounddevice numpy
```

### Usage

Run `synthon.py` with the desired arguments or use a JSON template for quick setup. For example:

```commandline
python synthon.py --volume 0.5 --attack 0.01 --harmonic 2,0.5,None --harmonic 3,0.3,0.8
```

Or using a template:

```commandline
python synthon.py --template my_config.json
```

#### Command Line Arguments

- `--template`: Path to a JSON template file for predefined configurations (default: 'default.json').
- `--volume`: Set a note's volume (default: 0.3)
- `--sample_rate`: Sample rate for the synthesizer (default: 44100)
- `--chunk_size`: Chunk size for the synthesizer (default: 512)
- `--attack`, `--decay`, `--sustain-amplitude`, `--sustain`, `--release`: Configure the ADSR envelope.
- `--vibrato-rate`, `--vibrato-depth`: Configure the rate and depth of vibrato.
- `--tremolo-rate`, `--tremolo-depth`: Configure the rate and depth of tremolo.
- `--harmonic`: Add a harmonic in the format "multiple,amplitude,sustain duration (None for infinite)". Repeatable for
  multiple harmonics.
- `--disable_speaker`: Disable output to speaker.
- `--output`: Filename for the output file.
- `--port_name`: MIDI input port name (default: 'IAC Driver Bus 1').

### Templates

Templates are JSON files that pre-define configurations for Synthon. They can specify any command-line arguments. Place
your templates in the `templates` directory of the project root. By default, Synthon uses `default.json` from this
directory.

### No MIDI Keyboard?

If you don't have a MIDI keyboard, check out my [other project](https://github.com/jofoks/Virtual-MIDI-Keyboard) which
allows you to turn your computer's keyboard into a MIDI device.
