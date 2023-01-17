# Telegram - Outgoing calls
Python script to make a VoIP telegram call with audio playback.

## Installation
On Linux and macOS to install this library you must have `make`, `cmake`, C++11 compatible compiler, Python headers, Opus and OpenSSL libraries and headers installed:

Debian-based distributions
```shell
apt install make cmake gcc g++ pkg-config python3-dev python3-pip gcc g++ openssl libssl-dev libopus0 libopus-dev
```

Archlinux-based distributions
```shell
pacman -S make cmake gcc python3 openssl opus
```

macOS
```shell
brew install make cmake gcc g++ python3 openssl opus
```

Windows

Unfortunately pytgvoip has a bug which causes failure while installing pytgvoip. A good workaround is using [WSL (Windows Subsystem for Linux)](https://docs.microsoft.com/en-us/windows/wsl/install). Ubuntu would be the preferable WSL Distro.

### Installing the required python packages
```shell
# pytgvoip only works on versions < 2
pip3 install Pyrogram==1.4.0
pip3 install pytgvoip
pip3 install pytgvoip-pyrogram
```

Create a file named `config.py` in the root directory with the following contents
`config.py`
```python
# Visit https://my.telegram.org./auth to generate your credentials
API_HASH = 'API Hash'
API_ID = 0 # API ID
CLIENT_NAME = 'Rose'
```
