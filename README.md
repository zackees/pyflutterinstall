# pyflutterinstall

Install flutter and all the dependencies for Mac, Windows and Linux.

# Win Tests

[![Win_Tests](https://github.com/zackees/pyflutterinstall/actions/workflows/push_win.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_win.yml)

[![Win_FullInstall](https://github.com/zackees/pyflutterinstall/actions/workflows/push_win_fullinstall.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_win_fullinstall.yml)

Installs all dependencies for pyflutter on Windows.

# MacOS

[![MacOS_Tests](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos.yml)

[![MacOS_Fullinstall](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos_fullinstall.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos_fullinstall.yml)

# Ubuntu

[![Ubuntu_Tests](https://github.com/zackees/pyflutterinstall/actions/workflows/push_ubuntu.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_ubuntu.yml)

[![Ubuntu_Fullinstall](https://github.com/zackees/pyflutterinstall/actions/workflows/push_ubuntu_fullinstall.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_ubuntu_fullinstall.yml)

Usage
```bash
> pip install pyflutterinstall
> pyflutterinstall
```

# Releases
  * 1.0.9: adb is now installed on the path.
  * 1.0.8: Gradle upgrade to 7.5, JDK is downgraded to 9.
  * 1.0.7: Windows now uses user environment variables to avoid elevated privileges.
  * 1.0.6: Fix macos install.
  * 1.0.5: Gradle is now installed as well.
  * 1.0.3: Uses pexpect to run commands.
  * 1.0.2: MacOS: now installs cocoapods dependency.
  * 1.0.1: Update setenvironment to 1.0.9 to get expanded paths.
  * 1.0.0: Windows, Mac and Linux now supported and all tests pass.
  * 0.0.2: Automated tests for windows.
  * 0.0.1: Initial release - windows supported.
