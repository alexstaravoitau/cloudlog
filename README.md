# cloudlog
A simple logger that duplicates console logs to a file, Dropbox and Telegram.

## How to use

* Install package: 
  
  ```
  pip install cloudlog
  ```
* Import `CloudLog` class:

  ```
  from cloudlog import CloudLog
  ```

You can log text by simply calling a `CloudLog` instance:
```python
import os

log = CloudLog(os.path.join(os.getcwd(), 'logs'))

log('Some important stuff happening.')
log('And again!')
log('Luckily, it\'s all safe now.')
```

You may as well add `pyplot` plots as images in the same folder:
```
from matplotlib import pyplot

log = CloudLog(os.path.join(os.getcwd(), 'logs'))

x = range(42)
pyplot.plot(x, x)

pyplot.xlabel('Amount of logs')
pyplot.ylabel('Coolness of your app')
pyplot.grid(True)

# Call it before calling `pyplot.show()`.
log.add_plot()

pyplot.show()
```

## Dropbox
In order to sync your logs and plots to Dropbox: 
* [Create a Dropbox app](https://www.dropbox.com/developers/apps/create) with `App folder` access type.
* Get your Dropbox access token and provide it in initialiser.
* Call `sync()` in order to dispatch log file to your Dropbox app folder.

```python
log = CloudLog(os.path.join(os.getcwd(), 'logs'), dropbox_token='YOUR_DROPBOX_TOKEN_HERE')

log('Some important stuff happening again.')
log('Luckily, it\'s all safe now. In the cloud!')
log.sync()
```

Plots are being synced to Dropbox folder by default.

## Telegram
You may as well get notifications in a Telegram chat, with logs and plots being sent to you.
* [Create a Telegram bot](https://core.telegram.org/bots#creating-a-new-bot).
* Get your Telegram Bot API access token
* [Find out your Telegram chat or user ID](http://stackoverflow.com/a/32777943/300131).
* Provide both values in the initialiser.

```
log = CloudLog(os.path.join(os.getcwd(), 'logs'), dropbox_token='YOUR_DROPBOX_TOKEN', telegram_token='YOUR_TELEGRAM_TOKEN', telegram_chat_id='CHAT_ID')

log('Some important stuff once more.')
log('Luckily, it\'s all safe now. In the cloud! AND you\'re notified — how cool is that?')

log.sync(notify=True, message='I\'m pregnant.')
```

Specify the same flag for plots and add an optional caption message:
```
...
log.add_plot(notify=True, caption='Pie chart of chances you\'re the father.')
```
