import logging
import pkgutil
import traceback

import click

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        pass

from maxbot.bot import MaxBot
from maxbot.errors import BotError


@click.command()
@click.option(
    "-f",
    "--file",
    "bot_file",
    type=click.Path(exists=True, dir_okay=False),
    help=(
        "Path for bot file. Use this option to create bot from single file."
        " NOTE: This option is mutually exclusive with '-d' and '-b'."
    ),
)
@click.option(
    "-d",
    "--directory",
    "bot_dir",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help=(
        "Path for bot directory. Use this option to create bot from directory of resources."
        " NOTE: This option is mutually exclusive with '-f' and '-b'."
    ),
)
@click.option(
    "-i",
    "--import",
    "import_spec",
    type=str,
    metavar="IMPORT",
    help=(
        "The Maxbot instance to load, in the form 'module:name'. Module can be a dotted import."
        " Name is not required if it is 'bot'."
        " "
    ),
)
def run(bot_file, bot_dir, import_spec):
    """
    Run bot locally.

    There are three options to run the bot.

    You can create bot from scratch and load resources from single file by using '-f' option.

        maxbot run -f mybot.yaml

    Use '-d' option to create bot from scratch and load resouces from dirctory.

        maxbot run -d mybot/

    Finally, you can manualy create and configure the bot and provide
    import spec to load it by using -i option.

        maxbot run -i mybot

    NOTE: Options '-f', '-d', '-i' are mutually exclusive.
    """
    try:
        if _check_mutually_exclusive(bot_file, bot_dir, import_spec):
            raise click.UsageError("Options '-f', '-d' and '-i' are mutually exclusive.")
        elif bot_file:
            bot = MaxBot.from_file(bot_file)
        elif bot_dir:
            bot = MaxBot.from_directory(bot_dir)
        elif import_spec:
            bot = _import_bot(import_spec)
        else:
            raise click.UsageError("Missing one of options '-f', '-d', '-i'.")
        # This is the only way we have for now to run bot app
        bot.telegram.run_ptb_polling()
    except BotError as exc:
        raise click.ClickException(str(exc))


@click.group()
def main():
    """A general utility script for MaxBot applications.

    Provides commands to run bots, test them with stories etc.
    """
    load_dotenv()
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # logging.getLogger('apscheduler').setLevel(logging.WARNING)
    # logging.getLogger('telegram').setLevel(logging.WARNING)


main.add_command(run)


def _check_mutually_exclusive(*args):
    return len(list(filter(None, args))) > 1


def _import_bot(import_spec):
    if ":" not in import_spec:
        import_spec += ":bot"
    try:
        bot = pkgutil.resolve_name(import_spec)
    except Exception:
        raise click.ClickException(
            f"While loading {import_spec!r}, an exception was raised:\n\n{traceback.format_exc()}"
        )

    if not isinstance(bot, MaxBot):
        raise click.ClickException(
            f"A valid MaxBot instance was not obtained from {import_spec!r}."
        )
    return bot
