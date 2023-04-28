#SingleInstance
SetKeyDelay 0, 50

WinGet, AvidemuxWindows, List, ahk_exe avidemux.exe
Loop % AvidemuxWindows {
	WinClose % "ahk_id" AvidemuxWindows%A_Index%
}
