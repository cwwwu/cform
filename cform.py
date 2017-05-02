import sublime
import sublime_plugin

import subprocess
import json
import pprint


class ValidatecftCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, ST3 World!")
		#self.view.insert(edit, 0, self.view.file_name())
		error = False
		status = 'Valid CloudFormation template!\n'
		try:
			output = subprocess.check_output("aws cloudformation validate-template --template-body file://" + self.view.file_name(), shell=True, stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as exc:
			status = 'Invalid CloudFormation template!\n'
			error = True
			output = exc.output

		window = self.view.window()
		output_view = window.create_output_panel('my_output')
		window.run_command('show_panel', {'panel': 'output.my_output'})
		output_view.run_command('insert', {'characters': status})
		if not error:
			cft_params = json.dumps(json.loads(output.decode('utf-8')), indent=2)
			output_view.run_command('append', {'characters': cft_params })
		else:
			output_view.run_command('append', {'characters': output.decode('utf-8') })
