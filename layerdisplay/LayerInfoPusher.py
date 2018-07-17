# Pushes layer information to clients

def push(plugin, print_job):
	result = "-"
	if print_job and print_job.layer_change_info:
		if print_job.printing:
			result = "%d / %d" % (print_job.current_layer, print_job.get_layer_count())
		else:
			result = "- / %d" % print_job.get_layer_count()
	plugin._plugin_manager.send_plugin_message(plugin._plugin_name, dict(layerString = result))

