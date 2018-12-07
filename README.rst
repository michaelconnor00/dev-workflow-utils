===============
Command Wrapper
===============

Install
-------

``$> pip install -i https://testpypi.python.org/pypi dev-workflow-utils``

Config File
-----------

The tool reads from a default `commands.json` file that contains JSON describing the different commands that are wrapped. Use `--help` to see all the available base commands.

Dev Rebuild and Upload
----------------------

After a new change is made, the package must be re-built and uploaded to `testpypi`. However make sure the version number is bumped first.


``$> sudo python setup.py sdist install``

``$> sudo python setup.py sdist develop  <- So it can be tested locally before hand, not required though.``


Once the package has been tested (manually or through unittests) then it can be uploaded.

``$> python setup.py sdist upload -r https://testpypi.python.org/pypi``

Usage
-----

All commands are to be configured in JSON format. The tools will look for a file in root called `commands.json`. There is a flag to specify a custom file location if required.

A basic example of a defined command:

.. code-block:: json

  "psql_host": ["psql -U postgres -h my_container"]

Using the command wrapper tool, the command is executed by ``cw psql_host``. Where the key name from the json object is the command name. Please note the commands defined in commands.json must be platform compatible. That means they should be compatible with your operatins system.

Here is an example of a command that wraps two seperate commands:

.. code-block:: json

  "clean": [
      "docker rm $(docker ps -a -q -f \"status=exited\")",
      "docker images | grep \"<none>\" | awk '{{ print \"docker rmi \" $3 }}' | bash"
    ]

Each command is executed stateless by default. Meaning, no variables will persist in memory between commands. This can be changed by adding making the first string in the array "--SHELL". This acts as a flag to indicate that the commands are to be run in a bash script, which will allow all the commands to run in the same memory space. It should be noted that this will not be cross-platform!!

Also, it is possible to provide arguments when running a command. When defining the commands, use "#" before a keyword to identify the argument. For example:

.. code-block:: json

  "shell": [
    "docker exec -it #container_name bash"
  ]

When executing ``cw shell my_container``, the argument will be substituted in before executing.


