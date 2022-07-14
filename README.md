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

This repo was originally based on the download script from [gist:lmarkus/lmarkus](https://gist.github.com/lmarkus/8722f56baf8c47045621#file-download-sh) to download but has migrated to a python script located in the `scripts/` dir.

### Getting emoji json lists
The current way that has been working is to go to the webapp of the slack team, and pull the token from one of the requests and using the [api test page](https://api.slack.com/methods/emoji.list/test) to download the emoji list directly

### Make Commands

* get
  * run `JSON_PATH=/path/to/emoji.list.json NAMESPACE=<subdir in emojis/> make get`
  * This will filter out all the emoji/aliases that aren't in your downloads.db and download the rest to the directory `emojis/${NAMESPACE}/` and add the downloaded data to the downloads.db for future filtering.

* gen
  * run `NAMESPACE=<subdir in emojis/> make gen`
  * This will generate an index and browse pages of markdown for all emoji in the `emojis/$NAMESPACE/` dir.

:)
