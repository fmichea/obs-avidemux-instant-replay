#SingleInstance
SetKeyDelay 0, 50

; Send the key to make it dump a replay.
ControlFocus,, ahk_exe obs64.exe
ControlSend,, ^+{F7}, ahk_exe obs64.exe

; Wait for avidemux to start with the replay file, scroll to the end of the file.
WinWait, ahk_exe avidemux.exe,, 60
if ErrorLevel
{
	MsgBox, Could not find avidemux window.
	return
}

Sleep 1000

ControlFocus,, ahk_exe avidemux.exe
ControlSend,, {End}{Down 3}{Space}, ahk_exe avidemux.exe
