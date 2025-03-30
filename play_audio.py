import subprocess
import numpy as np
import pyaudio
import sys
import os
import struct

def read_value(data, offset, length, endian='<', fmt='I'):
	"""
	Reads and unpacks a value from binary data and returns both value and raw hex.
	"""
	raw_bytes = data[offset:offset+length]
	value = struct.unpack(endian + fmt, raw_bytes)[0]
	hex_string = ' '.join(f'{byte:02X}' for byte in raw_bytes)
	return value, hex_string

def parse_pcm_metadata(filepath):
	with open(filepath, 'rb') as f:
		data = f.read()

	# Define metadata locations
	metadata_info = {
		'channels':    {'offset': 0x14, 'length': 4, 'endian': '>', 'fmt': 'I'},
		'looped':      {'offset': 0x18, 'length': 4, 'endian': '>', 'fmt': 'I'},
		'sample_rate': {'offset': 0x2C, 'length': 2, 'endian': '>', 'fmt': 'H'},
		'loop_start':  {'offset': 0x30, 'length': 4, 'endian': '>', 'fmt': 'I'},
		'num_samples': {'offset': 0x34, 'length': 4, 'endian': '>', 'fmt': 'I'},
	}

	# Extract and interpret metadata
	values = {}
	hex_data = {}

	for key, info in metadata_info.items():
		value, hex_str = read_value(data, info['offset'], info['length'], info['endian'], info['fmt'])
		values[key] = value
		hex_data[key] = hex_str

	# Interpret special values
	channels = 1 if values['channels'] == 0x60 else 2 if values['channels'] == 0x80 else None
	looped = True if values['looped'] == 0xA0 else False if values['looped'] == 0x80 else None

	# Print results
	print(f"Channels: {channels} (raw: {hex_data['channels']})")
	print(f"Looped: {looped} (raw: {hex_data['looped']})")
	print(f"Sample Rate: {values['sample_rate']} Hz (raw: {hex_data['sample_rate']})")
	print(f"Loop Start Sample: {values['loop_start']} (raw: {hex_data['loop_start']})")
	print(f"Total Samples: {values['num_samples']} (raw: {hex_data['num_samples']})")

	return {
		'channels': channels,
		'looped': looped,
		'sample_rate': values['sample_rate'],
		'loop_start': values['loop_start'],
		'num_samples': values['num_samples'],
	}

def fix_audio(filepath, meta):
	channels = meta['channels']
	looped = meta['looped']
	sample_rate = meta['sample_rate']
	loop_start = meta['loop_start']
	num_samples = meta['num_samples']

	with open(filepath, 'rb') as f:
		raw_data = f.read()[0xE0:]  # Skip metadata/header

	# Always read as big-endian 16-bit mono data
	audio_array = np.frombuffer(raw_data, dtype='>i2')

	if channels == 2:
		# Read as mono and split into stereo (fake split)
		midpoint = len(audio_array) // 2
		first_half = audio_array[:midpoint]
		second_half = audio_array[midpoint:]

		if len(first_half) != len(second_half):
			second_half = np.pad(second_half, (0, 1), mode='constant')

		audio_array = np.column_stack((first_half, second_half))
		print(f"Modified stereo shape: {audio_array.shape}")

	else:
		# Mono: reshape to (samples, 1) to keep consistent shape
		audio_array = audio_array.reshape(-1, 1)
		print(f"Mono shape: {audio_array.shape}")

	# Convert to little-endian for PyAudio and output file
	byte_data = audio_array.astype('<i2').tobytes()
	return byte_data


def loop_audio(byte_data, meta, amount_of_loops):
	channels = meta['channels']
	loop_start = meta['loop_start']
	num_samples = meta['num_samples']

	if not meta['looped'] or amount_of_loops < 1:
		return byte_data  # Nothing to loop

	# Convert bytes back into NumPy array
	audio_array = np.frombuffer(byte_data, dtype='<i2')

	if channels == 2:
		if len(audio_array) % 2 != 0:
			audio_array = audio_array[:-1]
		audio_array = audio_array.reshape(-1, 2)
	else:
		audio_array = audio_array.reshape(-1, 1)

	# Ensure loop points are in range
	loop_start = min(loop_start, audio_array.shape[0])
	loop_end = min(num_samples, audio_array.shape[0])

	# Get the loop section
	loop_section = audio_array[loop_start:loop_end]

	# Append it N times
	looped_array = np.vstack([audio_array] + [loop_section] * amount_of_loops)

	return looped_array.astype('<i2').tobytes()

def play_pcm_audio(filepath):
	meta = parse_pcm_metadata(filepath)

	channels = meta['channels']
	looped = meta['looped']
	sample_rate = meta['sample_rate']
	loop_start = meta['loop_start']
	num_samples = meta['num_samples']

	byte_data = fix_audio(filepath, meta)
	
	if looped == True:
		byte_data = loop_audio(byte_data, meta, 3)

	# Play the audio
	p = pyaudio.PyAudio()
	print(f"Opening stream with format={pyaudio.paInt16}, channels={channels}, rate={sample_rate}")
	print(f"Types: channels={type(channels)}, rate={type(sample_rate)}")
	stream = p.open(format=pyaudio.paInt16,
					channels=2 if channels == 2 else 1,
					rate=sample_rate,
					output=True)

	stream.write(byte_data)

	stream.stop_stream()
	stream.close()
	p.terminate()
