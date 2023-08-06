import os
import pwd

try:
    import getpass

    HAS_PASS = hasattr(getpass, "getuser") and hasattr(pwd, "getpwnam")
except ImportError:
    HAS_PASS = False


async def load_console_user(hub):
    if HAS_PASS:
        hub.grains.GRAINS.console_username = getpass.getuser()
        hub.grains.GRAINS.console_user = pwd.getpwnam(
            hub.grains.GRAINS.console_username
        ).pw_uid
    else:
        console = "/dev/console"
        if os.path.exists(console):
            # returns the 'st_uid' stat from the /dev/console file.
            uid = os.stat(console)[4]
            hub.grains.GRAINS.console_user = uid
        else:
            hub.grains.GRAINS.console_user = 0
        hub.grains.GRAINS.console_username = pwd.getpwuid(
            hub.grains.GRAINS.console_user
        ).pw_name
