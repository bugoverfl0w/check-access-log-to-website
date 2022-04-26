> Check referral domains to your website

# Install
> bash -x install.sh

# How to use
> update .env file
```sh
TELEGRAM_BOT_TOKEN: telegram bot token
TELEGRAM_CHAT_ID: telegram chat id. How to get your group/channel chat id?
You should add @getidsbot, then it will print your chat id
```

```sh
> ./access_log_check_ref.py
```

# **Crontab**
> You can set crontab (linux) to check referral links, example every 30 minutes
```sh */30 * * * * /path/to/access_log_check_ref.py```
