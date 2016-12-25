# cloudlog
A simple logger that duplicates console logs to a local file, Dropbox and Telegram. More details [in this post](http://navoshta.com/cloud-log/).

## How to use

* Install package: 
  
	```bash
	pip install cloudlog
	```

* Import `CloudLog` class:

	```python
	from cloudlog import CloudLog
	```

* Log text by simply calling a `CloudLog` instance:

	```python
	log = CloudLog(root_path='~/logs'))
()	log('Some important stuff happening.')
	log('And again!')
	log('Luckily, it\'s all safe now in a local file.')
	```

* Add `pyplot` plots as images in the same folder:

	```python
	from matplotlib import pyplot

	# Draw a plot
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
log = CloudLog(root_path='~/logs', dropbox_token='YOUR_DROPBOX_TOKEN_HERE')

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

```python
log = CloudLog(root_path='~/logs', telegram_token='YOUR_TELEGRAM_TOKEN', telegram_chat_id='CHAT_ID')

log('Some important stuff once more.')
log('Luckily, it\'s all safe now in a local file. AND you\'re notified — how cool is that?')

log.sync(notify=True, message='I\'m pregnant.')
```

Specify the same `notify` flag for plots for them to be sent to a Telegram chat as well:

```python
...
log.add_plot(notify=True)
```

Since one may be tempted to dispatch a bunch of updates at the same time, the user will not be notified about messages containing files, such as plots and logs — only about the `message` passed to `sync()` method.
