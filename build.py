import os
import shutil
import pytz
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from stonksfeed.web.siliconinvestor import (si_ai_robotics_forum,
                                            si_amd_intel_nvda_forum)
from stonksfeed.measures import measures
from stonksfeed.config import rss_feeds
from stonksfeed.rss.rss_reader import RSSReader


def datetime_format(value, format="%Y-%m-%d %H:%M"):
    return value.strftime(format)


def build_site(build_path, template_path, static_path):
    # Setup Jinja2 env
    jinja_env = Environment(loader=FileSystemLoader([template_path]), autoescape=True)
    jinja_env.filters["datetime_format"] = datetime_format

    chicago_tz = pytz.timezone("America/Chicago")
    now = datetime.now(chicago_tz)

    articles = []

    for feed in rss_feeds:
        reader = RSSReader(
            publisher=feed["publisher"],
            feed_title=feed["feed_title"],
            rss_url=feed["rss_url"]
        )
        articles += reader.get_articles()

    # SiliconInvestor Forum Posts
    si_ai_robotoics_articles = si_ai_robotics_forum.get_articles()
    si_amd_intel_nvda_articles = si_amd_intel_nvda_forum.get_articles()

    articles += si_ai_robotoics_articles
    articles += si_amd_intel_nvda_articles

    # Write the main site index.html file
    with open(os.path.join(build_path, "index.html"), "w") as outfile:
        template = jinja_env.get_template("index.html")
        rendered_template = template.render(articles=articles, build_time=now)
        outfile.write(rendered_template)

    # Write the measures page
    with open(os.path.join(build_path, "measures.html"), "w") as outfile:
        template = jinja_env.get_template("measures.html")
        rendered_template = template.render(measures=measures)
        outfile.write(rendered_template)

    # Copy static folder
    shutil.rmtree(os.path.join(build_path, "static"), ignore_errors=True)
    shutil.copytree(static_path, os.path.join(build_path, "static"))


if __name__ == "__main__":
    site_path = os.getcwd()
    template_path = os.path.join(site_path, "templates")
    build_path = os.path.join(site_path, "_build")
    static_path = os.path.join(site_path, "static")

    build_site(build_path, template_path, static_path)
