from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

import subprocess


class WindowSwitcherExtension(Extension):
    def __init__(self):
        super(WindowSwitcherExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        result = subprocess.run(
            ['wmctrl -xlp | sed \'s/\\s\\s*/ /g\' | cut -d \' \' -f 1,3,4,6-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True,
        ).stdout

        windows = [
            {
                'id': l.split(maxsplit=3)[0],
                'pid': l.split(maxsplit=3)[1],
                'class': l.split(maxsplit=3)[2],
                'name': l.split(maxsplit=3)[3],
            }
            for l in result.splitlines()
        ]

        search_word = str(event.get_argument() or "").lower().strip()
        search_results = []
        for w in windows:
            if search_word == '' or search_word in w['name'].lower() or search_word in w['class'].lower():
                search_results.append(
                    ExtensionResultItem(
                        icon="images/icon.svg",
                        name=w["name"].replace("&", "&amp;"),
                        description="PID: {}, Class: {}".format(w['pid'], w['class']),
                        on_enter=RunScriptAction("wmctrl -ia {}".format(w['id'])),
                    )
                )

        return RenderResultListAction(search_results)


if __name__ == "__main__":
    WindowSwitcherExtension().run()
