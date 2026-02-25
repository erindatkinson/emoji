# Emoji

This repo is a collection of emojis from various slack teams. Emoji images can be found in the `emojis` directory. Browsing in GitHub is difficult, so the `docs` dir has a series of pages with emoji tables on them.

![An image of green yellow and red leaves and some small berries laying on the dirt](assets/autumn-g98ec0f698_1920.jpg)
Image by [wal_172619](https://pixabay.com/users/wal_172619-12138562/)

## Usage

Since the python script I made had aged out of how slack was doing things, I rewrote the upstream for [slack-emojinator](https://github.com/erindatkinson/slack-emojinator) in Golang, so you should be able to download the most recent release for your architecture from there and use it to archive/import emojis, post release notes, and generate docs.

### Examples

All examples assume you have sourced a `.env` file or set the env vars as follows

```shell
export SLACK_TEAM=subdomain
export SLACK_TOKEN=xoxc-1234
export SLACK_COOKIE='utm=blah;...'
```

```shell
# To Import
slack-emojinator import -d /path/to/dir/to/import
```

```shell
# To Export
slack-emojinator export -d /path/to/emojis/namespace
```

```shell
# To generate docs
slack-emojinator docs -d /path/to/emojis/namespace
```

## Building new emoji

Many people have been keen on building new emoji, and have made templates and scripts to help aid in making new emoji permutations, to see those, please see [assets/templates/](assets/templates/) and [assets/scripts/](assets/scripts/).

:)
