import subprocess
import os

import obspython as S


_INSTANT_REPLAY_SCENE = 'N64 - Instant Replay'
_REPLAY_POSITION = 'D:\\OBS Recordings\\SM64'

_AHK_BINARY = 'C:\\Program Files\\AutoHotkey\\AutoHotkey.exe'
_INSTANT_REPLAY_START_SCRIPT = 'D:\\AutoHotKey\\InstantReplay_Start.ahk'
_INSTANT_REPLAY_STOP_SCRIPT = 'D:\\AutoHotKey\\InstantReplay_Stop.ahk'

_AVIDEMUX_BINARY = 'C:\\Program Files\\Avidemux 2.8 VC++ 64bits\\avidemux.exe'


class Data:
    def __init__(self):
        self.previous_scene = None
        self.current_scene = None

    def set_current_scene(self, current_scene):
        self.previous_scene = self.current_scene
        self.current_scene = current_scene
        return self.previous_scene


d = Data()


def _monitor_replays():
    initial_files = set(os.listdir(_REPLAY_POSITION))

    def _check_files_callback():
        current_files = set(os.listdir(_REPLAY_POSITION))
        new_files = list(current_files - initial_files)
        if not new_files:
            return

        S.timer_remove(_check_files_callback)

        new_file_path = os.path.join(_REPLAY_POSITION, new_files[0])
        subprocess.Popen([_AVIDEMUX_BINARY, new_file_path])

    S.timer_add(_check_files_callback, 100)


def _handle_instant_replay_selected():
    scene_source = S.obs_frontend_get_current_scene()
    current_scene_name = S.obs_source_get_name(scene_source)
    S.obs_source_release(scene_source)

    previous_scene_name = d.set_current_scene(current_scene_name)

    if current_scene_name == _INSTANT_REPLAY_SCENE:
        _monitor_replays()
        subprocess.Popen([_AHK_BINARY, _INSTANT_REPLAY_START_SCRIPT])

    if previous_scene_name == _INSTANT_REPLAY_SCENE:
        subprocess.Popen([_AHK_BINARY, _INSTANT_REPLAY_STOP_SCRIPT])


def on_event(event):
    if event == S.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        _handle_instant_replay_selected()


def script_description():
    return "Automatically opens the correct replay buffer for N64 in avidemux when instant replay scene is selected."


def script_load(settings):
    S.obs_frontend_add_event_callback(on_event)


def script_save(settings):
    pass
