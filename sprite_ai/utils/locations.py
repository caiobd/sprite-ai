import platformdirs

from sprite_ai.constants import APP_NAME


user_data_location = platformdirs.user_data_path(
    appname=APP_NAME,
    appauthor=None,
    version=None,
    roaming=False,
    ensure_exists=True,
)
user_voices_location = user_data_location / 'voices'