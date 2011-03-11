import sublime, sublime_plugin, rubyformatter
  
class PrettyRubyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		region = sublime.Region(0L, view.size())

		reformatter = rubyformatter.RubyFormatter(view.substr(region))
		beautified = reformatter.run()

		view.replace(edit, region, beautified) 

