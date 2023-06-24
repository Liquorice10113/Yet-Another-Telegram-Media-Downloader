# Yet-Another-Telegram-Media-Downloader
Yet Another Telegram Media Downloader (Work in Progress).

A Telegram media downloader written for my own usage.


### Features
* Skip existing files.
* Auto floodwait handling (a custom Pyrogram library is required, which is still a work in progress).
* Resume download from where it last stopped.

### Installation
Install requirements by
```
pip3 install -r requirements.txt
```

### Configuration
Just fill your api_hash and api_id in `config.py`.
```
api_hash = "your_api_hash_here"
api_id = "your_api_id_here"
```

### Run
As simple as:
```
python3 download.py -c "https://t.me/xxx1234"
```
Files will be saved in `{current_dir}/{chat_name}/`.
Full usage:
```
usage: download.py [-h] [-c CHAT] [-l 100]
Yet Another Telegram Media Downloader.
options:
  -h, --help            show this help message and exit
  -c CHAT, --chat CHAT  Specify a chat name like "https://t.me/xxx1234" or just "xxx1234".
  -l 100, --limit-size 100
                        Specify a file size limit(MB), default to 100, files larger than this value will be skipped.
```

### TODO
* Develop a custom Pyrogram library for improved floodwait handling.
* Perform additional testing.
