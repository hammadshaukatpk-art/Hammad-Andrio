# MH Andrio

Early-stage Windows Android emulator manager powered by Google's official Android Emulator. Dark interface, multiple Android Virtual Device profiles, start/stop/delete, APK installation, RAM and CPU settings.

## Windows installer

Go to [GitHub Actions](../../actions/workflows/build-windows.yml), open the newest successful build and download the `MH-Andrio-Windows-Installer` artifact. Extract the ZIP and run `MH-Andrio-Setup.exe`.

## Required separately

Install Android Studio SDK components: Android Emulator, Platform Tools, Command-line Tools (latest), and an Android x86_64 system image. Default SDK directory is `%LOCALAPPDATA%\Android\Sdk`. Enable Windows hardware virtualization. The installer does not include these components.

## Limitations

This is a development release, not a feature-complete BlueStacks alternative. It has not been validated on a physical Windows machine. The number of simultaneous devices is limited by hardware. Google Play is not guaranteed. Uninstalling MH Andrio does not remove Android SDK or device profiles.

## Development

`pip install -r requirements.txt` then `python run.py`.
