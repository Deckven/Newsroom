"""HTML output formatter using Jinja2."""

from __future__ import annotations

from jinja2 import Template

from newsroom.formatters.base import BaseFormatter
from newsroom.models import Digest

HTML_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>News Digest: {{ digest.topic }}</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; color: #222; }
    h1 { border-bottom: 2px solid #333; padding-bottom: .5rem; }
    .meta { color: #666; font-size: .9rem; }
    .article { margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #ddd; }
    .summary { background: #f9f9f9; padding: .75rem; border-left: 3px solid #4a90d9; margin: .5rem 0; }
    .tags span { background: #e8e8e8; padding: 2px 8px; border-radius: 3px; font-size: .85rem; margin-right: 4px; }
    a { color: #4a90d9; }
  </style>
</head>
<body>
  <h1>News Digest: {{ digest.topic }}</h1>
  <p class="meta">Generated: {{ digest.generated_at.strftime('%Y-%m-%d %H:%M UTC') }} &middot; {{ digest.articles | length }} articles</p>

  {% for article in digest.articles %}
  <div class="article">
    <h2>{{ loop.index }}. {{ article.title }}</h2>
    <p class="meta">
      <strong>{{ article.source_name }}</strong>
      {% if article.published_at %} &middot; {{ article.published_at.strftime('%Y-%m-%d') }}{% endif %}
    </p>
    {% if article.summary %}
    <div class="summary">{{ article.summary }}</div>
    {% elif article.content %}
    <p>{{ article.content[:300] }}{% if article.content | length > 300 %}&hellip;{% endif %}</p>
    {% endif %}
    {% if article.url %}<p><a href="{{ article.url }}">Read more &rarr;</a></p>{% endif %}
    {% if article.tags %}
    <p class="tags">{% for tag in article.tags %}<span>{{ tag }}</span>{% endfor %}</p>
    {% endif %}
  </div>
  {% endfor %}
</body>
</html>
""")


class HTMLFormatter(BaseFormatter):
    """Render a digest as an HTML page."""

    def format(self, digest: Digest) -> str:
        return HTML_TEMPLATE.render(digest=digest)
