from flask import Flask, render_template, request, url_for,redirect,session
import pytumblr
import praw
import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

# Tumblr API Setup
tumblr_client = pytumblr.TumblrRestClient(
   'WylHVQBFehklZ8aVIZj8Kjt6zqez1vo68D8Auq8No8pCiwSySd',
 '2aEiyV81TcRL1a4czSxsSnDfQwDxf0iIL1u3buSBrIE70UERj7',
  'FmBY75NFhB9MsLeJ0Nh69HYJB1rCr4Ede4bF57hICGrPO8diFr',
 '9sYC2fX1Z5Nuua2nrhyi2ESqdELfMt25jo8AlhEi7kzqxxNIv6'
    )
# Reddit API credentials
REDDIT_CLIENT_ID = 'OeUbeQ4DRwnc4tmWGVwfwA'
REDDIT_CLIENT_SECRET = 'NrDDvakfgz2byxDVAK2-evoVjbKHaQ'
REDDIT_USER_AGENT = 'python:com.example.socialint:v1.0 (by u/Lonely_Safe_8701)'

# Initialize Reddit API
reddit_client = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username='Lonely_Safe_8701',
    password='0118669952bd'
)

import secrets

def generate_random_secret(length=32):

  alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
  secret = ''.join(secrets.choice(alphabet) for _ in range(length))
  return secret

username_reddit = 'boury'
password_reddit = '123'
username_tumblr = 'boury'
password_tumblr = '123'
last_id = 0
old_posts = []
offset_t = 0
old_posts_t = []
post_ids =[]
offset_filter = 0
offset_filter_all = 0

@app.route('/')
def index():
    return redirect('login')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_reddit_input = request.form['reddit_username']
        password_reddit_input = request.form['reddit_password']
        username_tumblr_input = request.form['tumblr_username']
        password_tumblr_input = request.form['tumblr_password']
        flag_reddit=False
        flag_tumblr=False

        if username_reddit_input == username_reddit and password_reddit_input == password_reddit:
            flag_reddit=True 
        else:
            return render_template('login.html', error='Invalid credentials for reddit')
        if username_tumblr_input == username_tumblr and password_tumblr_input == password_tumblr:
            flag_tumblr=True
        else:
            return render_template('login.html', error='Invalid credentials for tumblr')
        if flag_tumblr==True and flag_reddit==True:
            session['authenticated'] = True
            return redirect(url_for('merged_feed'))
        
    else:
        return render_template('login.html')


@app.route("/merged_feed")
def merged_feed():
    if 'authenticated' in session and session['authenticated']:
        {}
    else:
        return redirect(url_for('login'))
    global reddit_filter
    global tumblr_filter
    reddit_filter = request.args.get('reddit_filter', '').strip()
    tumblr_filter = request.args.get('tumblr_filter', '').strip()
    
    
    global post_ids
    global last_id
    global old_posts
    
    # Case 1: Filter by Tumblr only
    if tumblr_filter and not reddit_filter:
        global offset_filter
        try:
            tumblr_dashboard = tumblr_client.posts(tumblr_filter, limit=20,  offset = offset_filter)  # Get 20 posts from the Tumblr blog
            if not tumblr_dashboard['posts']:
                return render_template("merged_feed_with_media.html", error="No posts found for this Tumblr blog")
        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching posts from Tumblr: {e}")
        
        tumblr_posts = extract_tumblr_post_data(tumblr_dashboard )
        for post in tumblr_posts:
            if isinstance(post['timestamp'], str):
                post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

        tumblr_posts.sort(key=lambda x: x['timestamp'], reverse=True)
        old_posts = tumblr_posts
        return render_template("merged_feed_with_media.html", posts=tumblr_posts)
    
    # Case 2: Filter by Reddit only
    elif reddit_filter and not tumblr_filter:
        try:
            subreddit = reddit_client.subreddit(reddit_filter)
            reddit_feed = subreddit.new(limit=20)  # Get 20 posts from the specific subreddit
            if not reddit_feed:
                return render_template("merged_feed_with_media.html", error="No posts found for this subreddit")
        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching posts from Reddit: {e}")
        reddit_posts = extract_reddit_post_data(reddit_feed)
        for post in reddit_posts:
            post_ids.append(post['id2'])  # Collect post IDs for pagination

        for post in reddit_posts:
            if isinstance(post['timestamp'], str):  # If the timestamp is a string
                post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

        reddit_posts.sort(key=lambda x: x['timestamp'], reverse=True)
        last_id = reddit_posts[-1]['id2']
        old_posts = reddit_posts
        return render_template("merged_feed_with_media.html", posts=reddit_posts)
    
        
    # Case 3: Filter by both Tumblr and Reddit
    elif tumblr_filter and reddit_filter:
        global offset_filter_all
        # Fetch 20 posts from Tumblr
        try:
            tumblr_dashboard = tumblr_client.posts(tumblr_filter, limit=20, offset = offset_filter_all)
            if not tumblr_dashboard['posts']:
                return render_template("merged_feed_with_media.html", error="No posts found for this Tumblr blog")
        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching posts from Tumblr: {e}")
        
        tumblr_posts = extract_tumblr_post_data(tumblr_dashboard )
         # Fetch 20 posts from Reddit
        try:
            subreddit = reddit_client.subreddit(reddit_filter)
            reddit_feed = subreddit.new(limit=20)
            if not reddit_feed:
                return render_template("merged_feed_with_media.html", error="No posts found for this subreddit")
        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching posts from Reddit: {e}")
        
        reddit_posts = extract_reddit_post_data(reddit_feed)
     
        for post in reddit_posts:
            post_ids.append(post['id2'])   

        all_posts = tumblr_posts + reddit_posts
       
        for post in all_posts:
            if isinstance(post['timestamp'], str):  
                post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

        all_posts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        last_id = reddit_posts[-1]['id2']
        old_posts = all_posts
        
        return render_template("merged_feed_with_media.html", posts=all_posts)
        
     # Case 4: No filter (normal case)
    else:
         # Fetch 20 posts from Tumblr
        global offset_t
        try:
            tumblr_dashboard = tumblr_client.dashboard(limit=20, offset = offset_t)  # Get 20 posts from the Tumblr dashboard
            if not tumblr_dashboard['posts']:
                return render_template("merged_feed_with_media.html", error="No posts found on Tumblr")
        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching posts from Tumblr: {e}")
        
        tumblr_posts = extract_tumblr_post_data(tumblr_dashboard )
        
        try:
            reddit_feed = reddit_client.front.new(limit=20)  
            
            if not reddit_feed:
                return render_template("merged_feed_with_media.html", error="No posts found on Reddit")
        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching posts from Reddit: {e}")
        reddit_posts = extract_reddit_post_data(reddit_feed)
        
        for post in reddit_posts:
            post_ids.append(post['id2']) 
        all_posts = tumblr_posts + reddit_posts
        
        for post in all_posts:
            if isinstance(post['timestamp'], str):  # If the timestamp is a string
                post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

        all_posts.sort(key=lambda x: x['timestamp'], reverse=True)
        last_id = reddit_posts[-1]['id2']
        old_posts = all_posts
        return render_template("merged_feed_with_media.html", posts=all_posts)

    

def extract_tumblr_post_data(tumblr):
    tumblr_posts = []
    i = 0

    for post in tumblr['posts']:
        i += 1
        post_data = {
            'source': 'Tumblr',
            'blog_name': post['blog_name'],
            'type': post['type'],
            'content': '',
            'media': '',
            'timestamp': datetime.datetime.fromtimestamp(post['timestamp']),
            'id': i,
            'video_type': "mp4"
        }

        content = post.get('body', post.get('caption', ''))
        soup = BeautifulSoup(content, 'html.parser')

       
        xl = soup
        post_data['aloo'] = xl
        post_data['content'] = soup.get_text()
        media_urls = []

        if post['type'] == 'answer':
                    question_html = post.get('question', '')
                    answer_html = post.get('answer', '')
                   
                    question = BeautifulSoup(question_html, 'html.parser').get_text()
                    answer = BeautifulSoup(answer_html, 'html.parser').get_text()

                    post_data['content']=f"Q: {question}\nA: {answer}"
        elif post['type'] == 'photo':
            tags = post.get('tags', [])
            try:
                post_data['content']= tags[0]
            
            except Exception as e:
                post_data['content']== ""
            try:
                for photo in post.get('photos', []):
                    
                   
                    if 'original_size' in photo and 'url' in photo['original_size']:
                        media_urls.append(photo['original_size']['url'])
                        post_data['type'] = 'photo'  
            except Exception as e:
                        print(f"Error extracting photo URL: {e}")

        # Find media (images, videos, etc.)
        for media_tag in soup.find_all(['img', 'video']):
            if media_tag.name == 'img' and media_tag.get('src'):
                media_urls.append(media_tag['src'])
                post_data['type'] = 'photo'  # Set the type to photo if image is found
            elif media_tag.name == 'video' and media_tag.get('src'):
                xl = media_tag['src']
                post_data['aloo'] = xl
                media_urls.append(media_tag['src'])
                post_data['type'] = 'video'  # Set the type to video if video is found
            elif media_tag.name == 'video': 
                source_tag = media_tag.find('source')
                if source_tag and source_tag.get('src'):
                    xl = source_tag['src']
                    post_data['aloo'] = xl  # Save video source URL
                    media_urls.append(xl)
                    post_data['type'] = 'video'    

        post_data['media'] = media_urls if media_urls else None

        tumblr_posts.append(post_data)

    return tumblr_posts
 

     
def extract_reddit_post_data(reddit_feed):
    reddit_posts = []
    i = 0

    for post in reddit_feed:
        i += 1
        post_data = {
            'source': 'Reddit',
            'blog_name': post.subreddit.display_name,
            'type': '' if post.is_self else 'media',
            'content': post.title + "\n\n" + post.selftext,
            'media': None,  # Default to None unless media is found
            'timestamp': datetime.datetime.fromtimestamp(post.created_utc),
            'id': i,
            'id2': post.id,
            'video_type': "mp4"
        }
        

        # Check if the post has media (e.g., image or video)
        if hasattr(post, 'is_video') and post.is_video:
            # If the post is a video, include the video URL
            post_data['media'] = [post.media['reddit_video']['fallback_url']]
            post_data['type'] = 'video'
            hls_url = post.media['reddit_video'].get('hls_url', '')
            if hls_url:
                post_data['media'] = [hls_url]
                post_data['video_type'] = "hls"  # Append HLS URL to the media list
                
        elif hasattr(post, 'preview') and 'images' in post.preview:
            # Get the first image URL from the preview
            post_data['media'] = [image['source']['url'] for image in post.preview['images']]
            post_data['type'] = 'photo'
            
        elif hasattr(post, 'media_metadata'):
            # Iterate over all images in media_metadata
            images = []
            for media_key, media_info in post.media_metadata.items():
                if 's' in media_info and 'u' in media_info['s']:
                    image_url = media_info['s']['u']  # Get the image URL from the 's' key
                    images.append(image_url)  # Add image to the list
                elif 'p' in media_info and len(media_info['p']) > 0:
                    # If 's' is not available, fallback to 'p' and get the first image link
                    image_url = media_info['p'][0]['u']
                    images.append(image_url)    
            if images:
                post_data['media'] = images  # Add all image URLs to media
                post_data['type'] = 'photo'  # Mark the post type as photo     

        reddit_posts.append(post_data)
    return reddit_posts

@app.route("/loadmore", methods=["POST"])
def load_more():
    global last_id
    global old_posts
    global offset_t
    global post_ids
    global offset_filter
    global offset_filter_all
    if 'authenticated' in session and session['authenticated']:
        {}
    else:
        return redirect(url_for('login'))
    if reddit_filter and not tumblr_filter:
        try:
            subreddit = reddit_client.subreddit(reddit_filter)
            next_batch = subreddit.new(limit=20, params={'after': f't3_{last_id}'})
            if not next_batch:
                return render_template("merged_feed_with_media.html", error="No more posts available")
            
            next_reddit_posts = extract_reddit_post_data(next_batch)
            for post in next_reddit_posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            next_reddit_posts.sort(key=lambda x: x['timestamp'], reverse=True)
           
            for post in next_reddit_posts:  
                if post['id2'] not in post_ids:
                    post_ids.append(post['id2'])
                else:
                    next_reddit_posts.remove(post)
            posts = next_reddit_posts + old_posts
            for post in posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            posts.sort(key=lambda x: x['timestamp'], reverse=True)
            last_id = next_reddit_posts[-1]['id2']
            old_posts = posts

        
            return render_template("merged_feed_with_media.html", posts=posts)

        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching more posts from Reddit: {e}")
        
    elif tumblr_filter and not reddit_filter:
         try:
            offset_filter += 21
            tumblr_batch = tumblr_client.posts(tumblr_filter, limit=20,  offset = offset_filter)
            if not tumblr_batch:
                return render_template("merged_feed_with_media.html", error="No more posts available")
            next_tumblr_posts = extract_tumblr_post_data(tumblr_batch)
            for post in  next_tumblr_posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            next_tumblr_posts.sort(key=lambda x: x['timestamp'], reverse=True)
            posts = next_tumblr_posts+ old_posts
            for post in posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            posts.sort(key=lambda x: x['timestamp'], reverse=True)
            old_posts = posts
            return render_template("merged_feed_with_media.html", posts=posts)
         except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching more posts from Reddit: {e}")
         
    elif reddit_filter and tumblr_filter:
        try:
            subreddit = reddit_client.subreddit(reddit_filter)
            
            next_batch = subreddit.new(limit=20, params={'after': f't3_{last_id}'})
            offset_filter_all += 21
            tumblr_batch = tumblr_client.posts(tumblr_filter, limit=20, offset = offset_filter_all)
            if not next_batch:
                return render_template("merged_feed_with_media.html", error="No more posts available")
            if not tumblr_batch:
                return render_template("merged_feed_with_media.html", error="No more posts available")
            next_reddit_posts = extract_reddit_post_data(next_batch)
            next_tumblr_posts = extract_tumblr_post_data(tumblr_batch)
            for post in next_reddit_posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            next_reddit_posts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            for post in  next_tumblr_posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            next_tumblr_posts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            for post in next_reddit_posts:  
                if post['id2'] not in post_ids:
                    post_ids.append(post['id2'])
                else:
                    next_reddit_posts.remove(post)
            posts = next_reddit_posts + next_tumblr_posts+ old_posts
            
            
            for post in posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            posts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            last_id = next_reddit_posts[-1]['id2']
            old_posts = posts
        
            return render_template("merged_feed_with_media.html", posts=posts)

        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching more posts from Reddit: {e}")

    else:
        try:
            
            next_batch = reddit_client.front.new(limit=20, params={'after': f't3_{last_id}'})
            offset_t += 21
            tumblr_batch = tumblr_client.dashboard(limit=20, offset = offset_t)
            if not next_batch:
                return render_template("merged_feed_with_media.html", error="No more posts available")
            if not tumblr_batch:
                return render_template("merged_feed_with_media.html", error="No more posts available")
           
            next_reddit_posts = extract_reddit_post_data(next_batch)
            next_tumblr_posts = extract_tumblr_post_data(tumblr_batch)
            for post in next_reddit_posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            next_reddit_posts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            for post in  next_tumblr_posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            next_tumblr_posts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            for post in next_reddit_posts:  
                if post['id2'] not in post_ids:
                    post_ids.append(post['id2'])
                else:
                    next_reddit_posts.remove(post)
                
            posts = next_reddit_posts + next_tumblr_posts+ old_posts
            
            
            for post in posts:
                if isinstance(post['timestamp'], str):  
                    post['timestamp'] = datetime.strptime(post['timestamp'], '%Y-%m-%d %H:%M:%S')

            posts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            last_id = next_reddit_posts[-1]['id2']
            old_posts = posts
        
            return render_template("merged_feed_with_media.html", posts=posts)

        except Exception as e:
            return render_template("merged_feed_with_media.html", error=f"Error fetching more posts from Reddit: {e}")


    
@app.route("/filter_by_date", methods=["GET"])
def filter_by_date():
    global old_posts
    date_filter = request.args.get('date', '')
    sort_order = request.args.get('sort_order', 'most_recent')
    if date_filter:
            try:
                target_date = datetime.datetime.strptime(date_filter, '%Y-%m-%d').date()
                old_posts = [post for post in old_posts if post['timestamp'].date() == target_date]
            except ValueError:
                return render_template("merged_feed_with_media.html", error="Invalid date format. Use 'YYYY-MM-DD'.")
    
    old_posts.sort(key=lambda x: x['timestamp'], reverse=(sort_order == 'most_recent'))

    return render_template("merged_feed_with_media.html", posts=old_posts, sort_order=sort_order)

if __name__ == '__main__':
    app.secret_key=generate_random_secret()
    app.run(debug=True, use_reloader=False)
