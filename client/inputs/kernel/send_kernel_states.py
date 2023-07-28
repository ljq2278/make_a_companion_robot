import subprocess

command_get_power1 = 'vcgencmd measure_volts'
command_get_power2 = 'vcgencmd get_throttled'
command_get_temperature = 'vcgencmd measure_temp'
result = subprocess.run(command_get_power2, shell=True, capture_output=True, text=True)

print(result.stdout)