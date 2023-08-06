from pathlib import Path
from configuration_maker import Config, ConfigKey

keys = [
    ConfigKey(
        name='user',
        group='pacer',
        description='Username for PACER account',
    ),

    ConfigKey(
        name='pass',
        group='pacer',
        description='Password for PACER account',
    ),

    ConfigKey(
        name='courtlistener_token',
        group='recap',
        description='API Token for CourtListener',
    ),
]

config = Config(
    path=Path.home() / '.cache' / 'courts_api' / 'config.json',
    config_keys=keys,
    cli_command='courts-api configure',
)