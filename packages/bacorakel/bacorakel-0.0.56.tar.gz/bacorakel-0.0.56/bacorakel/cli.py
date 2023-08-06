"""BACorakel Command-Line Interface."""


import click

from bacorakel.logging import error
from bacorakel.state import ArduinoSettings, ScalesSettings, State, state

try:
    DEFAULTS = State(state_file="bacorakel.toml")
    DEFAULTS.load()
except Exception:
    DEFAULTS = State()


@click.command(name="BACorakel")
@click.option("--debug/--no-debug", "-d", default=DEFAULTS.debug, show_default=True)
@click.option(
    "--emulate-arduino/--no-emulate-arduino",
    "-a/-na",
    default=DEFAULTS.arduino.device == "emulate",
    show_default=True,
)
@click.option(
    "--emulate-scales/--no-emulate-scales",
    "-s/-ns",
    default=DEFAULTS.scales.device == "emulate",
    show_default=True,
)
@click.option("--host", "-h", default=DEFAULTS.host, show_default=True)
@click.option("--port", "-p", default=DEFAULTS.port, show_default=True)
@click.option(
    "--state-file",
    "-f",
    default="bacorakel.toml",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, readable=True),
    show_default=True,
)
def bacorakel(
    debug: bool,
    emulate_arduino: bool,
    emulate_scales: bool,
    host: str,
    port: int,
    state_file: click.Path,
):
    """The BACorakel Command-Line Interface."""
    try:
        import cherrypy
        from cherrypy.process.plugins import Monitor

        from bacorakel.controller import Controller
        from bacorakel.dashboard import server

        state.state_file = str(state_file)
        state.load()
        state.debug = debug
        state.arduino.device = "emulate" if emulate_arduino else ArduinoSettings.device
        state.scales.device = "emulate" if emulate_scales else ScalesSettings.device
        state.host = host
        state.port = port
        state.save()

        controller = Controller()

        cherrypy.tree.graft(server, "/")
        cherrypy.server.unsubscribe()
        server = cherrypy._cpserver.Server()
        server.socket_host = host
        server.socket_port = port
        server.thread_pool = 30
        server.subscribe()

        monitor = Monitor(cherrypy.engine, controller.cycle, frequency=1)
        monitor.subscribe()

        cherrypy.engine.start()
        cherrypy.engine.block()
    except Exception as e:
        error(str(e))


if __name__ == "__main__":
    bacorakel()
