Sesame: config file encryption
==============================

Almost all applications have configuration of some kind. Often this config is 
sensitive in some way - database passwords, SMTP account details, API keys etc.

These days it's common to use public source control - which means you can no
longer store your application's sensitive config in with its code.

Sesame provides a simple way to encrypt (and decrypt) your application's config
so it can be safely stored in public source control.


Usage
-----


Flask Bindings
--------------

When using `Flask-Script <http://flask-script.readthedocs.org/en/latest/>`_ you
benefit from automatic integration.

.. code-block:: python

    # create your Flask app and Flask-Script manager as usual
    app = Flask("test")
    manager = Manager(app)

    # include the sesame manager
    from sesame.flask.script import manager as sesame_manager
    manager.add_command("sesame", sesame_manager)

Then you can use the encrypt/decrypt commands via your manage script:

.. code-block::

    > ./manage.py sesame
    Please provide a command:
    Encrypt/decrypt Flask application config
        decrypt  Decrypt a config file
        encrypt  Encrypt a config file


Django Bindings
---------------

Coming Soon
