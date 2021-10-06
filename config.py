from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TELEBOT",
    settings_files=['settings.toml', '.secrets.toml'],
    ignore_unknown_envvars=True,
    environments=True
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
