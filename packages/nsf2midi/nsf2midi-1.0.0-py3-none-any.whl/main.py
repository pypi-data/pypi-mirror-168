from asyncio.windows_events import NULL
import os
import re
import argparse
from mido import Message, MidiFile, MidiTrack, MetaMessage

parser = argparse.ArgumentParser(
    description='python main.py input.nsf output.mid 0')
parser.add_argument("input", help='nsf file name')
parser.add_argument("output", help='midi file name')
parser.add_argument("index", help='index of song, start from zero')
args = parser.parse_args()
temp_file = args.input + '.tmp.txt'
os.system('FamiStudio {i} famistudio-txt-export {temp} -nsf-import-song:{n}'.format(
    i=args.input, n=args.index, temp=temp_file))

txt_file = open(temp_file, 'r')
lines = txt_file.readlines()
txt_file.close()
# os.remove(temp_file)

midi_file = MidiFile()


def low_val(note):
    note = note[:2]
    if False == note.endswith("#"):
        note = note[0]
    if note == "C":
        return 0
    if note == "C#":
        return 1
    if note == "D":
        return 2
    if note == "D#":
        return 3
    if note == "E":
        return 4
    if note == "F":
        return 5
    if note == "F#":
        return 6
    if note == "G":
        return 7
    if note == "G#":
        return 8
    if note == "A":
        return 9
    if note == "A#":
        return 10
    if note == "B":
        return 11


def note_value(note):
    return low_val(note) + int(note[-1:])*12


def build_note(line):
    match_note = re.search('Value="(.*?)"', line)
    match_duration = re.search('Duration="(.*?)"', line)
    match_start = re.search('Note Time="(.*?)"', line)
    if match_note:
        note = match_note.group(1)
        duration_val = int(match_duration.group(1))
        start_time_val = int(match_start.group(1)) + pattern_index*256
        note_val = note_value(note)
        global current_time
        midi_track.append(Message('note_on', note=note_val,
                                  velocity=127, time=(start_time_val - current_time)*16))
        midi_track.append(Message('note_off', note=note_val,
                                  velocity=127, time=duration_val * 16))
        current_time = start_time_val  + duration_val


def build_channel(line):
    match_name = re.search('Channel Type="(.*?)"', line)
    name = match_name.group(1)
    global midi_track
    midi_track = MidiTrack()
    midi_track.append(MetaMessage('track_name', name=name, time=0))
#    midi_track.append(MetaMessage(
#        'set_tempo', tempo=int(600000/128*100), time=0))
    midi_file.tracks.append(midi_track)
    global current_time
    current_time = 0

for line in lines:
    if line.startswith('\t\tChannel Type='):
        print("new channel")
        global pattern_index
        pattern_index = -1
        build_channel(line)
    elif line.startswith('\t\t\tPattern Name='):
        pattern_index = pattern_index + 1
    elif line.startswith('\t\t\t\tNote Time='):
        build_note(line)

#
midi_file.save(args.output)
