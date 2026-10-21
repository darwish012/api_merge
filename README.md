# Reddit and Tumblr Merged Feed

A Flask web application that brings Reddit and Tumblr posts into one chronological feed. It fetches a configured Reddit account's front page and Tumblr dashboard, or combines posts from a selected subreddit and Tumblr blog. The interface supports date filtering, sorting, additional batches of posts, images, and video playback.

## What is implemented

- A local demonstration login that sets a Flask session flag.
- Reddit front-page and subreddit retrieval through PRAW.
- Tumblr dashboard and blog retrieval through pytumblr.
- A common post representation with source, account/subreddit, content, timestamp, and media.
- Newest-first merging, date filtering, and oldest/newest sorting of loaded posts.
- A Load More action using Reddit post IDs and Tumblr offsets.
- Image slideshows, MP4 video, and HLS video through hls.js.
- Tumblr question/answer text and HTML text extraction with BeautifulSoup.

## Repository structure

| Path | Contents |
| --- | --- |
| [app2.py](app2.py) | Flask routes, API clients, post extraction, filtering, pagination state, and the development entry point. |
| [templates/login.html](templates/login.html) | Local login form. |
| [templates/merged_feed_with_media.html](templates/merged_feed_with_media.html) | Feed, filtering forms, media rendering, slideshow controls, and HLS playback. |
| [static/](static/) | Reddit and Tumblr logo images. |

## Requirements and configuration

Use Python with Flask, pytumblr, PRAW, and BeautifulSoup. A dependency file and pinned Python/package versions are not supplied. Network access and valid credentials for both services are required; the feed template also loads hls.js from a CDN.

Configure your own values in `app2.py` before running:

- The Tumblr client constructor takes the consumer key, consumer secret, OAuth token, and OAuth token secret.
- The Reddit client uses a client ID, client secret, user agent, username, and password.
- The separate `username_reddit`, `password_reddit`, `username_tumblr`, and `password_tumblr` variables control the local login form.

The local form compares its inputs to those configured demonstration values. It does **not** authenticate a new Reddit or Tumblr account or replace the API clients' credentials. Configuration is currently embedded in Python rather than loaded from environment variables; do not reuse or publish committed credentials.

## Run locally

From the repository root:

```bash
python -m pip install flask pytumblr praw beautifulsoup4
python app2.py
```

Open `http://127.0.0.1:5000/login/` and use the local demonstration credentials you configured. The script generates a session secret and starts Flask in debug mode with the reloader disabled.

## Use the feed

1. Sign in to open the merged feed.
2. Leave both platform fields empty for the configured Reddit front page and Tumblr dashboard.
3. Enter a Tumblr blog name to retrieve that blog, a subreddit name to retrieve that subreddit, or both to merge the two sources. Although the UI says Reddit Account, the backend treats that field as a subreddit.
4. Use the date picker and sort selector to filter and order posts already loaded into memory.
5. Use Load More to request another batch, or Refresh to reload the page.

| Route | Purpose |
| --- | --- |
| `/` | Redirect to login. |
| `/login/` | Display and submit the local login form. |
| `/merged_feed` | Fetch and display the selected feeds. |
| `/loadmore` | POST action to retrieve and merge more posts. |
| `/filter_by_date` | Filter the loaded list by date and apply sort order. |

## Implementation limits

Feed lists, filters, pagination IDs, and offsets are process-wide globals shared by visitors. Date filtering mutates the loaded list, and there is no persistent database or exported feed output. Some branches assume Reddit results are nonempty before indexing their final item. String-timestamp branches call `datetime.strptime` despite importing the `datetime` module, so they would need correction if a string timestamp reaches them.

The login form posts to `/login`, while the Flask route is declared as `/login/`; align the form action if POST redirection causes login problems in your environment. The application is a local demonstration with debug mode and embedded API credentials, not a configured multi-user deployment.

## Tech stack and references

Python, Flask/Jinja2, PRAW, pytumblr, BeautifulSoup, HTML, CSS, JavaScript, and hls.js.

References retained from the original README: [Flask](https://flask.palletsprojects.com/), [PRAW](https://praw.readthedocs.io/), [pytumblr](https://github.com/tumblr/pytumblr), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), [Reddit API](https://www.reddit.com/dev/api), and [Tumblr API](https://www.tumblr.com/docs/api/v2).

## Author

Abdelrahman Darwish ([GitHub @darwish012](https://github.com/darwish012)).
