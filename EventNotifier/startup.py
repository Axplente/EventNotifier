import sys
import os


def update_windows_startup(enabled_flag):
    try:
        import winreg
    except ImportError:
        return

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "EventNotifier"

    exe_path = os.path.abspath(sys.argv[0])
    cmd = f'"{exe_path}" --notify'

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0,
            winreg.KEY_ALL_ACCESS
        )
    except OSError:
        return

    with key:
        if enabled_flag:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass