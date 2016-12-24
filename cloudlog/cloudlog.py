import os
import time
import dropbox
import dropbox.files
from matplotlib import pyplot
from twx.botapi import TelegramBot, InputFile, InputFileInfo


class CloudLog(object):
    """
    Lets you duplicate console logs in a locally stored file, folder on Dropbox and
    receive updates in a Telegram chat.
    """

    def __init__(self, root_path, dropbox_token=None, telegram_token=None, telegram_chat_id=None):
        """
        Initialises a new logger instance.

        Parameters
        ----------
        root_path           :
                              Local log root path.
        dropbox_token       :
                              Dropbox access token.
        telegram_token      :
                              Telegram Bot API access token.
        telegram_chat_id    :
                              Telegram chat ID.
        """
        self.telegram_chat_id = int(telegram_chat_id)
        self.cloud_log_writer = dropbox.Dropbox(dropbox_token) if dropbox_token is not None else None
        self.notification_bot = TelegramBot(telegram_token) if telegram_token is not None else None

        self.log_file = time.strftime('%Y-%m-%d_%H-%M-%S') + '_log.txt'
        self.root = root_path
        os.makedirs(root_path, exist_ok=True)

    def __call__(self, string):
        """
        Logs the value to console and appends the same string to the log file.

        Parameters
        ----------
        string  : string
                  Value to be logged.
        """
        print(string)
        with open(os.path.join(self.root, self.log_file), 'a') as file:
            file.write(string + '\n')

    def add_plot(self, notify=False, caption=None):
        """
        Saves current `pyplot` plot as a .png, uploads it to Dropbox and optionally notifies via Telegram chat.

        Parameters
        ----------
        notify  :
                  Flag indicating if we need to send a Telegram notification.
        caption :
                  Optional plot caption.
        """
        plot_file = time.strftime('%Y-%m-%d_%H-%M-%S') + '.png'
        plot_path = os.path.join(self.root, plot_file)
        pyplot.savefig(plot_path)

        self.cloud_upload_plot(plot_file)
        if notify:
            self.bot_send_plot(plot_file, caption)

    def sync(self, notify=False, message=None):
        """
        Synchronises local log with Dropbox.

        Parameters
        ----------
        notify  :
                  Flag indicating if we need to send a Telegram notification.
        message :
                  Optional notification message.
        """
        self.cloud_sync_log()
        if notify:
            self.bot_send_message(message)
            self.bot_send_log()

    # Dropbox routines

    def cloud_sync_log(self):
        """
        Syncs local log with the one in Dropbox App's folder (e.g. overwrtites it).
        """
        if self.cloud_log_writer is None: return

        with open(os.path.join(self.root, self.log_file), 'rb') as file:
            try:
                self.cloud_log_writer.files_upload(
                    file.read(),
                    '/' + self.log_file,
                    mode=dropbox.files.WriteMode('overwrite', None)
                )
            except Exception as e:
                self('Failed to sync log: ' + str(e))
                pass

    def cloud_upload_plot(self, filename):
        """
        Uploads plot to Dropbox app's folder.

        Parameters
        ----------
        filename    :
                      Plot filename or relative path.
        """
        if self.cloud_log_writer is None: return

        plot_path = os.path.join(self.root, filename)
        with open(plot_path, 'rb') as file:
            try:
                self.cloud_log_writer.files_upload(
                    file.read(),
                    '/' + filename,
                    mode=dropbox.files.WriteMode('overwrite', None)
                )
            except Exception as e:
                self('Failed to upload plot: ' + str(e))
                pass

    # Telegram routines

    def bot_send_message(self, message, mode="Markdown"):
        """
        Sends a text message to default Telegram chat.

        Parameters
        ----------
        message :
                  Message to send.
        mode    :
                  Message parsing mode. Defaults to `Markdown`.
        """
        if self.notification_bot is None: return

        try:
            self.notification_bot.send_message(
                self.telegram_chat_id,
                message,
                parse_mode=mode
            ).wait()
        except Exception as e:
            self('Failed to send notification: ' + str(e))
            pass

    def bot_send_plot(self, filename, caption=None):
        """
        Sends plot saved as `filename` to default Telegram chat with optional caption.

        Parameters
        ----------
        filename  :
                    Plot filename or path relative to current directory.
        caption   :
                    Optional plot caption.
        """
        if self.notification_bot is None: return

        plot_path = os.path.join(self.root, filename)
        with open(plot_path, 'rb') as file:
            try:
                self.notification_bot.send_photo(
                    self.telegram_chat_id,
                    InputFile('photo', InputFileInfo(filename, file, 'image/png')),
                    caption=caption,
                    disable_notification=True
                ).wait()
            except Exception as e:
                self('Failed to send plot: ' + str(e))
                pass

    def bot_send_log(self):
        """
        Sends current log file to default Telegram chat. Does not notify the user about this message, send a separate
        message if you want the notification to hit user's device.
        """
        if self.notification_bot is None: return

        with open(os.path.join(self.root, self.log_file), 'rb') as file:
            try:
                self.notification_bot.send_document(
                    self.telegram_chat_id,
                    InputFile('document', InputFileInfo(self.log_file, file, 'text/plain')),
                    disable_notification=True
                ).wait()
            except Exception as e:
                self('Failed to send log: ' + str(e))
                pass
