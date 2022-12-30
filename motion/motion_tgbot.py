#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
user_id=123456789

import logging
import os
import subprocess
import sys
import shlex
import datetime
import html

from telegram import Update, ForceReply
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from subprocess import Popen, PIPE

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    global textoutput
    textoutput = ''
    while True:
        global output
        output = process.stdout.readline()
        output = output.decode('utf8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip())
        textoutput = textoutput + '\n' + output.strip()
    rc = process.poll()
    return rc

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if (user_id != update.message.from_user.id): #sender checks
        return
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def startmotion(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /startmotion is issued."""
    if (user_id != update.message.from_user.id): #sender checks
        return
    run_command('systemctl start motion;sleep 3;ps ax |grep motion')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )

def stopmotion(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /stopmotion is issued."""
    if (user_id != update.message.from_user.id): #sender checks
        return
    run_command('systemctl stop motion;ps ax |grep motion')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )


def startnginx(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /startnginx is issued."""
    if (user_id != update.message.from_user.id): #sender checks
        return
    run_command('systemctl start nginx;sleep 3;ps ax |grep nginx')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )

def stopnginx(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /stopnginx is issued."""
    if (user_id != update.message.from_user.id): #sender checks
        return
    run_command('systemctl stop nginx;ps ax |grep nginx')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )

def status(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /status is issued."""
    if (user_id != update.message.from_user.id): #sender checks
        return

    run_command('free;uptime;uname -a')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )
    run_command('df -h')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )
    run_command('ps axwwfu')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )
    run_command('top -n1 -b -o "%CPU"')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )
    run_command('netstat -anp |egrep -iv \"unix\"')
    update.message.reply_html(
        text='<pre>' + html.escape(textoutput)[:4095] + '</pre>',    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if (user_id != update.message.from_user.id): #sender checks
        return
    update.message.reply_text('/start\n/status\n/startmotion\n/stopmotion\n/startnginx\n/stopnginx')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("98342345:wlrkgjnlrgjnelrtgjnerltg")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("startmotion", startmotion))
    dispatcher.add_handler(CommandHandler("stopmotion", stopmotion))
    dispatcher.add_handler(CommandHandler("startnginx", startnginx))
    dispatcher.add_handler(CommandHandler("stopnginx", stopnginx))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
