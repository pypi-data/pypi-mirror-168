import logging

from marshmallow import Schema, fields
from telegram import Bot, Update


class TelegramChannel:
    """
    Channel for Telegram Bots. See https://core.telegram.org/bots.

    The implementation is based on python-telegram-bot library.
    See https://python-telegram-bot.org.

    You need to install additional dependencies to use this channel.
    Try `pip install -U maxbot[telegram]`.

    There are two channel arguments (chargs) in this channel.

    An :class:`~telegram.Update` object represents an incoming update.
    See https://core.telegram.org/bots/api#update for more information about updates.

    An :class:`~telegram.Bot` object represents the telegram bot you are working with.
    See https://core.telegram.org/bots/api#available-methods for more information about telegram bot methods.
    """

    class ConfigSchema(Schema):
        """
        Configuration schema for telegram bot.
        """

        # Authentication token to access telegram bot api.
        # @see https://core.telegram.org/bots#6-botfather
        api_token = fields.Str(required=True)

    def create_dialog(self, update: Update, bot: Bot):
        """
        Creates a dialog object from the incomming update.

        See https://core.telegram.org/bots/api#update.
        See https://docs.python-telegram-bot.org/en/latest/telegram.update.html.

        :param Update update: an incoming update.
        :param Bot bot: the telegram bot.
        :return dict: a dialog with the schema :class:`~maxbot.schemas.DialogSchema`
        """
        return {"channel_name": "telegram", "user_id": update.effective_user.id}

    def receive_text(self, update: Update, bot: Bot):
        """
        Receives a text message from the channel.

        See https://core.telegram.org/bots/api#message.

        :param Update update: an incoming update.
        :param Bot bot: the telegram bot.
        :return dict: a message with the payload :class:`~maxbot.schemas.MessageSchema.text`
        """
        if update.message and update.message.text:
            return {"text": update.message.text}

    def send_text(self, command: dict, dialog: dict, bot: Bot):
        """
        Sends a text command to the channel.

        See https://core.telegram.org/bots/api#sendmessage.

        :param dict command: a command with the payload :attr:`~maxbot.schemas.CommandSchema.text`.
        :param dict dialog: a dialog we respond in, with the schema :class:`~maxbot.schemas.DialogSchema`
        :param Bot bot: the telegram bot.
        """
        bot.send_message(dialog["user_id"], command["text"])

    def receive_image(self, update: Update, bot: Bot):
        """
        Receives an image message from the channel.

        See https://core.telegram.org/bots/api#message.
        See https://core.telegram.org/bots/api#photosize.
        See https://core.telegram.org/bots/api#getfile.
        See https://core.telegram.org/bots/api#file.

        :param Update update: an incoming update.
        :param Bot bot: the telegram bot.
        :return dict: a message with the payload :class:`~maxbot.schemas.MessageSchema.image`
        """
        if update.message and update.message.photo:
            # get the biggest image version
            photo = max(update.message.photo, key=lambda p: p.file_size)
            obj = bot.getFile(photo.file_id)
            message = {"image": {"url": obj.file_path, "size": obj.file_size}}
            if update.message.caption:
                message["image"]["caption"] = update.message.caption
            return message

    def send_image(self, command: dict, dialog: dict, bot: Bot):
        """
        Sends an image command to the channel.

        See https://core.telegram.org/bots/api#sendphoto.

        :param dict command: a command with the payload :attr:`~maxbot.schemas.CommandSchema.image`.
        :param dict dialog: a dialog we respond in, with the schema :class:`~maxbot.schemas.DialogSchema`
        :param Bot bot: the telegram bot.
        """
        image = command["image"]
        bot.send_photo(dialog["user_id"], image["url"], image.get("caption"))

    def run_ptb_polling(self):
        """Runs simple application based on `python-telegram-bot` polling mechanism."""

        from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        def callback(update: Update, context: CallbackContext):
            self.simple_adapter(update=update, bot=context.bot)

        updater = Updater(self.config["api_token"])
        updater.dispatcher.add_handler(MessageHandler(Filters.all, callback))
        updater.start_polling()
        updater.idle()
