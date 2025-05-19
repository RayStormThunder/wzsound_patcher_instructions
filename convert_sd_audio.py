import subprocess
import os

def convert_to_rwav(input_audio, output_rwav):
	tool_path = os.path.join("RWAVTool.exe")  # Update if different
	subprocess.run([tool_path, input_audio, output_rwav], check=True)
