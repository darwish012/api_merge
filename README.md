# 🌐 Social Media Integrator

A powerful web application that seamlessly integrates **Reddit** and **Tumblr** feeds into a unified, interactive dashboard. View, filter, and explore content from multiple social media platforms in one place with an elegant, user-friendly interface.

## ✨ Features

### 📱 Multi-Platform Integration
- **Reddit Integration** - Access your Reddit front page, browse subreddits, and explore curated content
- **Tumblr Integration** - Browse Tumblr dashboards and explore specific blogs
- **Unified Feed** - Combine posts from both platforms into a single, chronologically sorted feed
- **Seamless Authentication** - Secure login system for both Reddit and Tumblr accounts

### 🎯 Powerful Filtering & Search
- **Single Platform Filtering** - View posts from Reddit only or Tumblr only
- **Combined Platform Search** - Filter by both Reddit subreddits and Tumblr blogs simultaneously
- **Date-Based Filtering** - Sort posts by specific dates (YYYY-MM-DD format)
- **Chronological Sorting** - View posts from most recent to oldest (or vice versa)

### 🎨 Rich Media Support
- **Image Display** - Automatic image extraction and rendering
- **Video Playback** - Support for both MP4 and HLS video formats
- **Multi-Media Posts** - Handle posts with multiple images or videos
- **Media Metadata** - Extract and display media from various post formats

### 📖 Pagination & Loading
- **Infinite Scroll** - "Load More" functionality to fetch additional posts
- **Smart Pagination** - Automatic deduplication to prevent duplicate posts
- **Performance Optimized** - Efficient API calls with proper offset management

### 🎭 Content Type Support
- **Text Posts** - Full text content with HTML parsing
- **Photo Posts** - Image galleries with proper sizing
- **Video Posts** - Embedded video players with multiple format support
- **Q&A Posts** - Question and answer content from Tumblr
- **Media Collections** - Posts with multiple images or videos

## 🏗️ Architecture

### Technology Stack

```
Backend:
├── Flask (Python Web Framework)
├── PRAW (Python Reddit API Wrapper)
├── pytumblr (Tumblr API Client)
├── BeautifulSoup (HTML/XML Parsing)
└── Python datetime (Timestamp Management)

Frontend:
├── HTML5 (Template Structure)
├── CSS3 (Styling)
├── JavaScript (Dynamic Interactions)
└── Jinja2 (Template Engine)

APIs:
├── Reddit API v1
└── Tumblr v2 API
```

### Project Structure

```
api_merge/
├── app2.py                              # Main Flask application
├── templates/
│   ├── login.html                       # Authentication page
│   └── merged_feed_with_media.html      # Main feed display
├── static/                              # CSS, JS, and images
├── README.md                            # This file
└── requirements.txt                     # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Reddit API credentials
- Tumblr API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/darwish012/api_merge.git
   cd api_merge
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask pytumblr praw beautifulsoup4
   ```

4. **Configure API Credentials**
   
   Open `app2.py` and update the following with your credentials:
   
   ```python
   # Tumblr API Setup
   tumblr_client = pytumblr.TumblrRestClient(
       'YOUR_CONSUMER_KEY',
       'YOUR_CONSUMER_SECRET',
       'YOUR_OAUTH_TOKEN',
       'YOUR_OAUTH_TOKEN_SECRET'
   )
   
   # Reddit API credentials
   REDDIT_CLIENT_ID = 'YOUR_CLIENT_ID'
   REDDIT_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
   REDDIT_USER_AGENT = 'your_app_name'
   ```

5. **Run the application**
   ```bash
   python app2.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## 🔐 Authentication

### Default Login Credentials

The application comes with default test credentials:
- **Reddit Username:** boury
- **Reddit Password:** 123
- **Tumblr Username:** boury
- **Tumblr Password:** 123

⚠️ **Security Note:** These are demonstration credentials. In production, implement proper OAuth authentication and secure credential management.

## 📖 Usage Guide

### Logging In
1. Navigate to the login page
2. Enter your Reddit username and password
3. Enter your Tumblr username and password
4. Click "Login" to proceed to the merged feed

### Viewing the Unified Feed
- Upon successful login, you'll see a combined feed of posts from your Reddit front page and Tumblr dashboard
- Posts are sorted chronologically (newest first)
- Media (images/videos) are displayed inline with posts

### Filtering by Platform

**Reddit Only:**
- Enter a subreddit name in the "Reddit Filter" field
- Leave "Tumblr Filter" empty
- Click apply to view only Reddit posts from that subreddit

**Tumblr Only:**
- Enter a blog name in the "Tumblr Filter" field
- Leave "Reddit Filter" empty
- Click apply to view only Tumblr posts from that blog

**Both Platforms:**
- Enter both a subreddit name and blog name
- Click apply to view merged posts from both sources

**No Filter (Default):**
- Leave both filter fields empty
- View your full Reddit front page and Tumblr dashboard

### Date Filtering
- Use the date picker to filter posts from a specific date
- Posts will be filtered to show only those from the selected date
- Chronological sorting options available

### Loading More Posts
- Click the "Load More" button to fetch additional posts
- The application automatically prevents duplicate posts
- Seamlessly integrates new posts with existing ones

## 🔄 API Integration Details

### Reddit API
- **Function:** Fetches posts from subreddits or the user's front page
- **Data Extracted:** Title, content, timestamps, media URLs, subreddit info
- **Media Handling:** Supports MP4 videos, HLS streams, and preview images

### Tumblr API
- **Function:** Fetches posts from blogs or the user's dashboard
- **Data Extracted:** Blog name, post type, captions, photos, videos
- **Special Handling:** Q&A posts, photo galleries, video content

## 🛠️ Key Functions

### `extract_tumblr_post_data(tumblr)`
Processes Tumblr API responses to extract relevant post information including:
- Blog name and post type
- HTML content parsing
- Media URL extraction
- Timestamp conversion

### `extract_reddit_post_data(reddit_feed)`
Processes Reddit API responses to extract:
- Subreddit name and post title
- Self-text content
- Video URLs (MP4 and HLS formats)
- Image URLs from previews and media metadata
- Timestamp conversion

### `load_more()`
Handles pagination by:
- Fetching the next batch of posts
- Preventing duplicate posts
- Merging with existing posts
- Maintaining chronological order

### `filter_by_date()`
Filters posts by a specific date and applies sorting preferences

## 🎨 Frontend Features

### Responsive Design
- Mobile-friendly interface
- Adaptive layout for different screen sizes
- Touch-friendly controls

### Media Rendering
- Inline image display with proper sizing
- Video player with multiple format support
- Fallback image handling for media errors

### User Interface
- Intuitive navigation
- Clear filtering options
- Error handling with user-friendly messages
- Real-time post loading

## 🚨 Error Handling

The application includes comprehensive error handling for:
- API authentication failures
- Network connectivity issues
- Invalid filter parameters
- Missing or malformed media data
- Empty result sets

## 🔒 Security Considerations

⚠️ **Important:** The current implementation stores credentials in code for demonstration purposes.

**For production deployment:**
- Use environment variables for sensitive credentials
- Implement OAuth 2.0 authentication flow
- Add HTTPS encryption
- Implement CSRF protection
- Use secure session management
- Add rate limiting
- Implement input validation and sanitization

## 🐛 Known Limitations

- Credentials are hardcoded (use environment variables in production)
- No persistent database for user sessions
- Limited error recovery mechanisms
- No pagination history tracking
- Basic input validation

## 📝 Code Quality

**Areas for Improvement:**
- Add comprehensive error handling and logging
- Implement input validation
- Refactor global variables into class-based architecture
- Add unit tests
- Implement caching for API responses
- Add database integration for session persistence
- Improve code organization with blueprints

## 🔮 Future Enhancements

- [ ] Support for additional platforms (Twitter, Instagram, etc.)
- [ ] User preferences and saved filters
- [ ] Advanced search and analytics
- [ ] Post sharing and bookmarking
- [ ] Comment fetching and display
- [ ] User authentication with OAuth
- [ ] Database integration for post history
- [ ] Dark mode support
- [ ] Real-time feed updates
- [ ] Mobile app version

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests with improvements
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Darwish** - Social Media Integrator Project  
GitHub: [@darwish012](https://github.com/darwish012)

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [PRAW](https://praw.readthedocs.io/) - Reddit API wrapper
- [pytumblr](https://github.com/tumblr/pytumblr) - Tumblr API client
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Reddit API](https://www.reddit.com/dev/api) - Social media data
- [Tumblr API](https://www.tumblr.com/docs/api/v2) - Social media data

---

**Last Updated:** February 2025  
**Status:** Active Development

