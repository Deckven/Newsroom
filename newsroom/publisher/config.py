"""
Publisher configuration — loads credentials from environment variables.

All secrets are read from env vars (or a .env file loaded externally).
No credentials are stored in code or config files.

Required env vars per platform:

WordPress:
  WORDPRESS_URL          — site URL (e.g. https://myblog.com)
  WORDPRESS_USER         — username
  WORDPRESS_APP_PASSWORD — application password

Telegram:
  TELEGRAM_BOT_TOKEN     — bot token from @BotFather
  TELEGRAM_CHAT_ID       — target chat/channel ID

Discord:
  DISCORD_WEBHOOK_URL    — webhook URL for the channel

Twitter/X:
  TWITTER_API_KEY        — API key (consumer key)
  TWITTER_API_SECRET     — API secret (consumer secret)
  TWITTER_ACCESS_TOKEN   — access token
  TWITTER_ACCESS_SECRET  — access token secret

LinkedIn:
  LINKEDIN_ACCESS_TOKEN  — OAuth 2.0 access token
  LINKEDIN_PERSON_ID     — person URN (or organization URN)

Reddit:
  REDDIT_CLIENT_ID       — app client ID
  REDDIT_CLIENT_SECRET   — app client secret
  REDDIT_USERNAME        — Reddit username
  REDDIT_PASSWORD        — Reddit password
  REDDIT_SUBREDDIT       — target subreddit (without r/)

Facebook:
  FACEBOOK_PAGE_TOKEN    — page access token
  FACEBOOK_PAGE_ID       — page ID

Instagram:
  INSTAGRAM_ACCESS_TOKEN — access token (same as Facebook Page token)
  INSTAGRAM_USER_ID      — Instagram Professional account user ID
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class WordPressConfig:
    url: str
    user: str
    app_password: str

    @classmethod
    def from_env(cls) -> WordPressConfig | None:
        url = os.getenv("WORDPRESS_URL")
        user = os.getenv("WORDPRESS_USER")
        pw = os.getenv("WORDPRESS_APP_PASSWORD")
        if not all([url, user, pw]):
            return None
        return cls(url=url, user=user, app_password=pw)  # type: ignore[arg-type]


@dataclass(frozen=True)
class TelegramConfig:
    bot_token: str
    chat_id: str

    @classmethod
    def from_env(cls) -> TelegramConfig | None:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat = os.getenv("TELEGRAM_CHAT_ID")
        if not all([token, chat]):
            return None
        return cls(bot_token=token, chat_id=chat)  # type: ignore[arg-type]


@dataclass(frozen=True)
class DiscordConfig:
    webhook_url: str

    @classmethod
    def from_env(cls) -> DiscordConfig | None:
        url = os.getenv("DISCORD_WEBHOOK_URL")
        if not url:
            return None
        return cls(webhook_url=url)


@dataclass(frozen=True)
class TwitterConfig:
    api_key: str
    api_secret: str
    access_token: str
    access_secret: str

    @classmethod
    def from_env(cls) -> TwitterConfig | None:
        vals = [
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET"),
        ]
        if not all(vals):
            return None
        return cls(*vals)  # type: ignore[arg-type]


@dataclass(frozen=True)
class LinkedInConfig:
    access_token: str
    person_id: str

    @classmethod
    def from_env(cls) -> LinkedInConfig | None:
        token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        pid = os.getenv("LINKEDIN_PERSON_ID")
        if not all([token, pid]):
            return None
        return cls(access_token=token, person_id=pid)  # type: ignore[arg-type]


@dataclass(frozen=True)
class RedditConfig:
    client_id: str
    client_secret: str
    username: str
    password: str
    subreddit: str

    @classmethod
    def from_env(cls) -> RedditConfig | None:
        vals = [
            os.getenv("REDDIT_CLIENT_ID"),
            os.getenv("REDDIT_CLIENT_SECRET"),
            os.getenv("REDDIT_USERNAME"),
            os.getenv("REDDIT_PASSWORD"),
            os.getenv("REDDIT_SUBREDDIT"),
        ]
        if not all(vals):
            return None
        return cls(*vals)  # type: ignore[arg-type]


@dataclass(frozen=True)
class FacebookConfig:
    page_token: str
    page_id: str

    @classmethod
    def from_env(cls) -> FacebookConfig | None:
        token = os.getenv("FACEBOOK_PAGE_TOKEN")
        pid = os.getenv("FACEBOOK_PAGE_ID")
        if not all([token, pid]):
            return None
        return cls(page_token=token, page_id=pid)  # type: ignore[arg-type]


@dataclass(frozen=True)
class InstagramConfig:
    access_token: str
    user_id: str

    @classmethod
    def from_env(cls) -> InstagramConfig | None:
        token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        uid = os.getenv("INSTAGRAM_USER_ID")
        if not all([token, uid]):
            return None
        return cls(access_token=token, user_id=uid)  # type: ignore[arg-type]
