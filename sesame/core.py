import os

from keyczar.keys import AesKey


def encrypt_config(config, keyfile=None):
    """
    Encrypt a config file.

    :param config: The path to the config file to be encrypted.
    :type config: str
    :param keyfile: A previously generated encryption keyfile.
    :type keyfile: str
    :raises: :class:`ConfigError`
    :return: The path to the encrypted file, or None.
    :rtype: string or None

    Example use::

        try:
            config = encrypt_config(config, keyfile)
            if config is not None:
                print "Application config encrypted at {0}".format(config)
    
        except ConfigError as e:
            sys.stderr.write("{0}".format(e))
            sys.exit(1)

    """
    if config is None:
        raise ConfigError("You must supply the path to your config file.")
    elif not os.path.exists(config):
        raise ConfigError("Application config doesn't exist at {0}".format(
            config
        ))

    if keyfile is None or os.path.exists(keyfile) is False:
        key = None

        if os.path.exists("key.pem"):
            try:
                with open("key.pem", "r") as f:
                    data = f.read()
                key = AesKey.Read(data)

                res = raw_input(("Encryption key appears to exist in key.pem. "
                                 "Use this? [Y/n] "))
                if len(res) > 0 and not res.lower().startswith('y'):
                    key = None
            except (ValueError, KeyError):
                pass

        if key is None:
            res = raw_input("Encryption key not provided. Create? [Y/n] ")
            if len(res) > 0 and not res.lower().startswith('y'):
                return None

            key = AesKey.Generate()
            with open("key.pem", "w") as f:
                f.write(str(key))
    else:
        with open(keyfile, "r") as f:
            data = f.read()

        key = AesKey.Read(data)

    with open(config, "r") as f:
        data = f.read()
    with open("{0}.encrypted".format(config), "w") as f:
        f.write(key.Encrypt(data))

    return config


def decrypt_config(config, keyfile):
    """
    Decrypt a config file.

    Args:
        * config (str): The path to the config file to be encrypted.
        * keyfile (str): The keyfile to use for decryption.
    Returns:
        string or None. The path to the decrypted file, or None.
    Raises:
       ConfigError

    """
    if config is None:
        raise ConfigError(("You must supply the path to your encrypted config "
                           "file."))
    else:
        if config.endswith(".encrypted"):
            config = config[0:-10]

        if not os.path.exists("{0}.encrypted".format(config)):
            raise ConfigError("Encrypted config doesn't exist at {0}.encrypted"
                              .format(config))

    if keyfile is None:
        raise ConfigError("Encryption keys are required for decryption!")
    elif not os.path.exists(keyfile):
        raise ConfigError("Encryption key doesn't exist at {0}".format(
            keyfile
        ))

    if os.path.exists(config):
        res = raw_input("Application config already exists. Overwrite? [y/N] ")
        if not res.lower().startswith('y'):
            return None

    with open(keyfile, "r") as f:
        data = f.read()

    key = AesKey.Read(data)

    with open("{0}.encrypted".format(config), "r") as f:
        data = f.read()
    with open(config, "w") as f:
        f.write(key.Decrypt(data))

    return config


class ConfigError(Exception):
    pass
