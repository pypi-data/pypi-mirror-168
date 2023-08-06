import subprocess as sp
import threading
from typing import Optional, Union

from flask import Flask
from werkzeug.serving import make_server


class _ServerThread(threading.Thread):
    """Class that represents a thread managing a flask app. Allows for the starting and stopping of the webserver
    in the background.

    """

    def __init__(self, app: Flask, host: str, port: int):
        """Constructor for the _ServerThread class.

        Args:
            app (Flask): the flask app to manage.
            host (str): the host to run at.
            port (int): the port to use.
        """
        threading.Thread.__init__(self)
        self.server = make_server(host, port, app)
        self.context = app.app_context()
        self.context.push()

    def run(self) -> None:
        """Start the provider webserver.

        """
        print("Starting provider server")
        self.server.serve_forever()

    def join(self, timeout: Union[float, None] = None) -> None:
        """Shut down the provider webserver.

        """
        print("Stopping provider server")
        self.server.shutdown()
        super().join(timeout)


class _FactoryThread(threading.Thread):
    """Class that represents a thread managing the Luminesce python provider factory process. Allows for the starting
    and stopping of the factory process in the background.

    """

    def __init__(self, host: str, port: int, user_id: Optional[str] = None, domain: Optional[str] = 'fbn-prd', _fbn_run=False):
        """Constructor for the _FactoryThread class.

        Args:
            host (str): the host that the provider webserver is running at.
            port (int): the port that the provider webserver is listening at.
            user_id (Optional[str]): optional user ID to run for.
            domain (Optional[str]): environment to run in (defaults to fbn-prd).
        """

        threading.Thread.__init__(self)

        self.cmd = f'luminesce-python-providers --quiet --authClientDomain={domain} '

        if user_id is not None and user_id != 'global':
            self.cmd += f'--localRoutingUserId "{user_id}" '

        elif user_id is not None and user_id == 'global':
            self.cmd += f'--routeAs:Global '

        self.cmd += f'--config "PythonProvider:BaseUrl=>http://{host}:{port}/api/v1/" '
        if _fbn_run:
            self.cmd += '"NameServiceClient:RabbitConfigFile=>honeycomb-rabbit-config-plain.json" '
            self.cmd += '"NameServiceClient:RabbitUserPassword->/usr/app/secrets/service-main" '
        self.factory_process = None

    def run(self) -> None:
        """Start the factory process.

        """
        print("Starting local provider factory")
        print(self.cmd)
        self.factory_process = sp.Popen(
            args=self.cmd.split()
        )

    def join(self, timeout: Union[float, None] = None) -> None:
        """Terminate the factory process.

        """
        if self.factory_process is not None:
            print("Stopping local provider factory")
            self.factory_process.terminate()
            super().join(timeout)
        else:
            # No factory is running: no-op
            super().join(timeout)
