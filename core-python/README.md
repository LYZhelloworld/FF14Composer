# FF14Composer (Python)
## How to Use
Download and run `ff14composer.py`. You should see a small black window.

Key configurations (you cannot change it in current version without changing the source code):
* ZXCVBNM = CDEFGAB
* SD GHJ = C# D# F# G# A#
* Comma = C +1 octave (C+ for short)
* Shift = +1 octave
* Ctrl = -1 octave
(Please note that Ctrl+, does not work due to some unknown bug.)

## Recording
Now you can record the notes with the program. The notes will be shown in the command line interface.

Every time you press the Enter key, the recorded notes will be displayed.

Press Backspace to erase ALL recorded notes (but not including the ones on the CLI).

## Instruments
You can choose 4 kinds of preset instruments (with MIDI instrument ID) and different position of middle C:
* Harp (46), C5
* Grand piano (0), C4
* Steel guitar (25), C4
* Pizzicato, C5

Change the commented code to switch instruments. You can also change it to your settings.
