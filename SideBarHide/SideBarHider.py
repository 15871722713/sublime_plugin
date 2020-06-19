import sublime
import sublime_plugin

PLUGIN_NAME = 'HideSidebarWhenNotFocussed'


class Vars:
    auto_hide = True


class HideSidebarWhenNotFocussedListener(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        if hover_zone == sublime.HOVER_GUTTER:
            view.window().set_sidebar_visible(True)
        else:
            view.window().set_sidebar_visible(False)
