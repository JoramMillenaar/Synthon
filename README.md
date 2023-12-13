<p align="center">
    <img src="logo.png" alt="drawing" width="250" />
</p>

# Synthon

Synthon is a Python-based synthesizer that seamlessly converts MIDI messages into rich synthesizer sounds. It leverages a custom-built effect pipeline, a sophisticated output handling system, and a MIDI input handler to create an immersive audio experience.

## Features

- **Effect Pipeline**: Customize your sound with effects like fade-in, fade-out, and an effect multiplier.
- **Output Pipeline**: Direct audio output to speakers or save it to a file.
- **Synthesizer**: High-quality sound generation with adjustable sample rate and chunk size.
- **MIDI Compatibility**: Use any MIDI input device to control the synthesizer.

## Getting Started

### Prerequisites

- Python 3.x
- MIDI input device (or use our companion project to turn your computer's keyboard into a MIDI device)

### Dependencies
```
pip install mido sounddevice numpy
```


### Usage

Run `synthon.py` with the desired arguments. For example:

```
python synthon.py --volume 0.5 --attack 0.01
```

#### Command Line Arguments

- `--volume`: Set a note's volume (default: 0.3)
- `--attack`: Duration of the attack of a note (default: 0.1)
- `--decay`: Duration of the decay of a note (default: 0.3)
- `--sustain-volume`: Relative volume of the sustain part of a note (default: 0.7)
- `--release`: Duration of the release of a note (default: 0.3)
- `--sample_rate`: Sample rate for the synthesizer (default: 44100)
- `--chunk_size`: Chunk size for the synthesizer (default: 512)
- `--disable_speaker`: Disable output to speaker
- `--output`: Filename for the output file
- `--port_name`: MIDI input port name (default: 'IAC Driver Bus 1')

### No MIDI Keyboard?

If you don't have a MIDI keyboard, check out my [other project](https://github.com/jofoks/Virtual-MIDI-Keyboard) which allows you to turn your computer's keyboard into a MIDI device.
