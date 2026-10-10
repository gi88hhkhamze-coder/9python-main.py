[app]
title = Bot Host
package.name = bothost
package.domain = org.bothost
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,discord.py,asyncio,charset-normalizer,idna,requests,urllib3,certifi

orientation = portrait
osx.kivy_version = 2.2.1

fullscreen = 0
android.permissions = INTERNET, FOREGROUND_SERVICE

[buildozer]
log_level = 2
warn_on_root = 1
