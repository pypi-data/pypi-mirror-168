# Created by Jan Rummens at 8/01/2021
import logging, logging.config

logging.config.fileConfig(fname='vision_logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from nemonet.runner.runner import Runner
import typer
import traceback

app = typer.Typer()

@app.command()
def scenario(name: str, useconfig: bool = False):
    try:
        if useconfig:
            runner = Runner.from_json_file(runner_config="runner_config.json")
        else:
            runner = Runner()
        runner.execute_scenario(name)
    except ValueError:
        typer.echo(f"invalid commandline")
        logger.debug("Fatal Error ValueError", exc_info=True)
    except FileNotFoundError as e:
        typer.echo(e)
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        logger.debug("Fatal Error Exception", exc_info=True)
    finally:
        pass
