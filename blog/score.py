
# import numpy as np
# from datetime import datetime
# from googleapiclient.discovery import build
# from transformers import pipeline

# # API_KEY = 'YOUR_API_KEY'
# # CHANNEL_ID = 'YOUR_CHANNEL_ID'
# # CHANNEL_ID = 'UCk3JZr7eS3pg5AGEvBdEvFg' #village
# CHANNEL_ID = 'UCX6OQ3DkcsbYNE6H8uQQuVA' #mR BEEST
# # CHANNEL_ID = 'UCoGForHQAmk0_9rI9CABeYw'  #woody and klewmy


# # CHANNEL_ID = 'UC56gTxNs4f9xZ7Pa2i5xNzg' #sony
# # CHANNEL_ID = 'UC6N3zABqbVuPR1xDdp5sDng' #Poorvika

# def initialize_youtube_client(api_key):
#     """Initializes the YouTube API client."""
#     return build('youtube', 'v3', developerKey=api_key)


# def get_channel_details(youtube, channel_id):
#     """Fetches channel details including snippet and statistics."""
#     try:
#         response = youtube.channels().list(part='snippet,statistics', id=channel_id).execute()
#         if response['items']:
#             return response['items'][0]
#         else:
#             return None
#     except Exception as e:
#         print(f"Failed to fetch channel details: {e}")
#         return None


# def get_recent_video_ids(youtube, channel_id, max_results=10):
#     """Retrieves recent video IDs from the specified channel."""
#     video_ids = []
#     try:
#         response = youtube.search().list(
#             part='id',
#             channelId=channel_id,
#             maxResults=max_results,
#             order='date',
#             type='video'
#         ).execute()
#         video_ids = [item['id']['videoId'] for item in response['items']]
#     except Exception as e:
#         print(f"Failed to fetch video IDs: {e}")
#     return video_ids


# def fetch_video_comments(youtube, video_id, max_comments=100):
#     """Fetches comments from a video."""
#     comments = []
#     try:
#         response = youtube.commentThreads().list(
#             part='snippet',
#             videoId=video_id,
#             textFormat='plainText',
#             maxResults=max_comments
#         ).execute()
#         for item in response['items']:
#             comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
#             comments.append(comment_text)
#     except Exception as e:
#         print(f"Failed to fetch comments: {e}")
#     return comments


# def sentiment_analysis(comments):
#     """Performs sentiment analysis on the comments using a transformer model."""
#     classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
#     sentiments = [classifier(comment)[0] for comment in comments]
#     positive_comments = sum(1 for sentiment in sentiments if sentiment['label'] == 'POSITIVE')
#     sentiment_score = positive_comments / len(comments) if comments else 0
#     return sentiment_score


# def get_video_engagement_metrics(youtube, video_ids):
#     """Fetches engagement metrics for a list of video IDs."""
#     metrics = {'likes': 0, 'dislikes': 0, 'views': 0, 'comments': 0, 'video_count': len(video_ids)}
#     try:
#         response = youtube.videos().list(part='statistics', id=','.join(video_ids)).execute()
#         for item in response['items']:
#             stats = item['statistics']
#             metrics['likes'] += int(stats.get('likeCount', 0))
#             metrics['dislikes'] += int(stats.get('dislikeCount', 0))
#             metrics['views'] += int(stats.get('viewCount', 0))
#             metrics['comments'] += int(stats.get('commentCount', 0))
#     except Exception as e:
#         print(f"Failed to fetch video metrics: {e}")
#     return metrics



# def calculate_trust_score(channel_details, engagement_metrics, sentiment_score):
#     """Calculates a trust score based on channel details, engagement metrics, and sentiment."""
#     try:
#         subscribers = int(channel_details['statistics']['subscriberCount'])
#         published_at = datetime.strptime(channel_details['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')  # Updated format string
#         account_age_years = (datetime.now() - published_at).days / 365.25

#         subscriber_score = np.clip(subscribers / 100000, 0, 10)
#         age_score = np.clip(account_age_years / 5, 0, 10)
#         engagement_score = np.clip(
#             (engagement_metrics['likes'] / max(engagement_metrics['likes'] + engagement_metrics['dislikes'], 1)) * 10,
#             0, 10)
#         viewing_engagement_score = np.clip(
#             np.log10(engagement_metrics['views'] / max(engagement_metrics['comments'], 1) + 1) * 2, 0, 10)
#         sentiment_score_scaled = np.clip(sentiment_score * 10, 0, 10)  # Scale sentiment score

#         total_score = subscriber_score + age_score + engagement_score + viewing_engagement_score
#         max_score = 40  # Adjusted for additional sentiment score contribution
#         return np.clip(total_score / max_score * 100, 0, 100)
#     except Exception as e:
#         print(f"Error calculating trust score: {e}")
#         return 0
import numpy as np
from datetime import datetime
from googleapiclient.discovery import build
from transformers import pipeline

# API_KEY and CHANNEL_ID should be set appropriately
API_KEY = ''
CHANNEL_ID = 'YOUR_CHANNEL_ID'

def initialize_youtube_client(api_key):
    """Initializes the YouTube API client."""
    return build('youtube', 'v3', developerKey=api_key)

def get_channel_details(youtube, channel_id):
    """Fetches channel details including snippet and statistics."""
    try:
        response = youtube.channels().list(part='snippet,statistics', id=channel_id).execute()
        if response['items']:
            return response['items'][0]
        else:
            return None
    except Exception as e:
        print(f"Failed to fetch channel details: {e}")
        return None

def get_recent_video_ids(youtube, channel_id, max_results=10):
    """Retrieves recent video IDs from the specified channel."""
    video_ids = []
    try:
        response = youtube.search().list(
            part='id',
            channelId=channel_id,
            maxResults=max_results,
            order='date',
            type='video'
        ).execute()
        video_ids = [item['id']['videoId'] for item in response['items']]
    except Exception as e:
        print(f"Failed to fetch video IDs: {e}")
    return video_ids

def fetch_video_comments(youtube, video_id, max_comments=100):
    """Fetches comments from a video."""
    comments = []
    try:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=max_comments
        ).execute()
        for item in response['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment_text)
    except Exception as e:
        print(f"Failed to fetch comments: {e}")
    return comments

def sentiment_analysis(comments):
    """Performs sentiment analysis on the comments using a transformer model."""
    classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
    sentiments = [classifier(comment)[0] for comment in comments]
    positive_comments = sum(1 for sentiment in sentiments if sentiment['label'] == 'POSITIVE')
    sentiment_score = positive_comments / len(comments) if comments else 0
    return sentiment_score

def get_video_engagement_metrics(youtube, video_ids):
    """Fetches engagement metrics for a list of video IDs."""
    metrics = {'likes': 0, 'dislikes': 0, 'views': 0, 'comments': 0, 'video_count': len(video_ids)}
    try:
        response = youtube.videos().list(part='statistics', id=','.join(video_ids)).execute()
        for item in response['items']:
            stats = item['statistics']
            metrics['likes'] += int(stats.get('likeCount', 0))
            metrics['dislikes'] += int(stats.get('dislikeCount', 0))
            metrics['views'] += int(stats.get('viewCount', 0))
            metrics['comments'] += int(stats.get('commentCount', 0))
    except Exception as e:
        print(f"Failed to fetch video metrics: {e}")
    return metrics

def parse_timestamp(timestamp):
    """Parses the timestamp from different possible formats."""
    for fmt in ('%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ'):
        try:
            return datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
    raise ValueError(f"Timestamp {timestamp} does not match any expected format")

def calculate_trust_score(channel_details, engagement_metrics, sentiment_score):
    """Calculates a trust score based on channel details, engagement metrics, and sentiment."""
    try:
        subscribers = int(channel_details['statistics']['subscriberCount'])
        published_at = parse_timestamp(channel_details['snippet']['publishedAt'])
        account_age_years = (datetime.now() - published_at).days / 365.25

        subscriber_score = np.clip(subscribers / 100000, 0, 10)
        age_score = np.clip(account_age_years / 5, 0, 10)
        engagement_score = np.clip(
            (engagement_metrics['likes'] / max(engagement_metrics['likes'] + engagement_metrics['dislikes'], 1)) * 10,
            0, 10)
        viewing_engagement_score = np.clip(
            np.log10(engagement_metrics['views'] / max(engagement_metrics['comments'], 1) + 1) * 2, 0, 10)
        sentiment_score_scaled = np.clip(sentiment_score * 10, 0, 10)  # Scale sentiment score

        total_score = subscriber_score + age_score + engagement_score + viewing_engagement_score + sentiment_score_scaled
        max_score = 50  # Adjusted for additional sentiment score contribution
        return np.clip(total_score / max_score * 100, 0, 100)
    except Exception as e:
        print(f"Error calculating trust score: {e}")
        return 0

# # Example usage
# if __name__ == '__main__':
#     youtube = initialize_youtube_client(API_KEY)
#     channel_detail s = get_channel_details(youtube, CHANNEL_ID)
#     if channel_details:
#         video_ids = get_recent_video_ids(youtube, CHANNEL_ID)
#         engagement_metrics = get_video_engagement_metrics(youtube, video_ids)
#         all_comments = []
#         for video_id in video_ids:
#             comments = fetch_video_comments(youtube, video_id)
#             all_comments.extend(comments)
#         sentiment_score = sentiment_analysis(all_comments)
#         trust_score = calculate_trust_score(channel_details, engagement_metrics, sentiment_score)
#         print(f"Trust Score: {trust_score}")
#     else:
#         print("Channel details not found.")

