# Pushes layer information to clients

def get_layer_info_string(print_job):
	if print_job:
		return print_job.to_string()
	return "-"

def push(plugin, print_job):
	result = get_layer_info_string(print_job)
	plugin._plugin_manager.send_plugin_message(plugin._plugin_name, dict(layerString = result))

