import subprocess

print(subprocess.check_call(['curl', '--globoff', '-o', 'output.json', 'http://overpass-api.de/api/interpreter?data=[out:json];node(1);out;']))