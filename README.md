# n1-rss
Python script which pushes N1 RSS to your Discord Server
You can create 3 .txt files:
sent_link.txt
monitor_log.txt
error_log.txt

This way, the script will monitor which links were sent, and will prevent sending same links multiple times.
Also there will be few pip requirements:
feedparser
requests
colorama


In order to get these messages on Discord you will need to do the following:
Create a Discord server (if you don’t have one)

Open Discord → click the + on the left sidebar.

Select Create My Own → choose For me and my friends or For a club/community.

Give it a name and create it.

Create a channel for alerts

Click + next to Text Channels → choose Text Channel.

Name it something like n1-news-alerts.

Hit Create Channel.

Create a Webhook

Go to your new channel → click the gear icon (Edit Channel).

Go to Integrations → Webhooks → New Webhook.

Give it a name, e.g., N1 Monitor Bot.

Select the channel you want messages to appear in.

Click Copy Webhook URL → this is the URL you paste in your script:

WEBHOOK_NEWS = "INPUT_YOUR_WEBHOOK_HERE"


Replace INPUT_YOUR_WEBHOOK_HERE with the URL you copied.

I used Windows Task Scheduler to make sure this script will run every time my PC reboots/powers on. You don't have to do it.
