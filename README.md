# Emoji

This repo is a collection of emojis from various slack teams. Emoji images can be found in the `emojis` directory. Browsing in GitHub is difficult, so the `docs` dir has a series of pages with emoji tables on them.

![An image of green yellow and red leaves and some small berries laying on the dirt](assets/autumn-g98ec0f698_1920.jpg)
Image by [wal_172619](https://pixabay.com/users/wal_172619-12138562/)

## Installation

### Prerequisites

* Python3 installed
* pipenv installed

### Install

`pipenv install`

## Usage

This repo was originally based on the download script from [gist:lmarkus/lmarkus](https://gist.github.com/lmarkus/8722f56baf8c47045621#file-download-sh) to download emoji but has migrated to a python script I wrote located in the `scripts/` dir.

### Getting emoji json lists
The current way that has been working is to go to the webapp of the slack team in your browser, opening a network inspector for the page and pulling your `token` from one of the requests there, and using the [api test page](https://api.slack.com/methods/emoji.list/test) to download the emoji.list json directly.

### Getting the slackbot response json lists.
I've never been able to get curl to handle this well, so what has worked is navigating to the slackbot response list for the slack team in a browser, opening the network inspector for the page and getting the raw response json directly from the browser's call to the `slackbot.responses.list` endpoint.

### Make Commands

* get
  * run `JSON_PATH=/path/to/emoji.list.json NAMESPACE=<subdir in emojis/> make get`
  * This will filter out all the emoji/aliases that are already in your downloads.db and download the rest to the directory `emojis/${NAMESPACE}/` and add the downloaded data to the downloads.db for future filtering.
* gen
  * run `NAMESPACE=<subdir in emojis/> make gen`
  * This will generate an index and browse pages of markdown for all emoji in the `emojis/$NAMESPACE/` dir.
* slackbot
  * run `JSON_PATH=/path/to/slackbot.responses.list.json MATCH=<substring for matching> make slackbot`
  * This will generate a list of triggers for slackbot responses that include your match substring.

:)
