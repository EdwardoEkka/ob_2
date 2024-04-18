import os
import json
import googleapiclient.discovery
import googleapiclient.errors

def authenticate_youtube_api(api_key):
    # Build the YouTube resource object to interact with the YouTube API.
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    return youtube

def video_details(youtube, vdo_id):
    video_details_list = []

    for i in range(0, len(vdo_id), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(vdo_id[i:i + 50])
        )
        response = request.execute()

        for video in response['items']:
            video_details = {
                'videoId': video['id'],
                'title': video['snippet']['title'],
                'publishedAt': video['snippet']['publishedAt'],
                'likes': video['statistics']['likeCount'],
                'views': video['statistics']['viewCount']
            }
            video_details_list.append(video_details)
    
    return video_details_list

if __name__ == "__main__":
    # Replace ['video_id_1', 'video_id_2', ...] with your list of video IDs
    video_ids = ['RqbLwFmieCA',
 'PUkFfkqq1Pg',
 'fW64NL8LpbQ',
 'Agm-c4jLzY4',
 'n6GE96No4ww',
 'dnkaA-WCDuE',
 '3dDQL2t6rl8',
 '4uS5drcfHc8',
 'Jl8WgA53PgA',
 'C4-_5zZVkpc',
 'JLws37tCqEs',
 'xqDxaWVQSSc',
 'StAjO0YHgeo',
 'sD2IBxwPc9c',
 'hLaelIId80M',
 'FckH6z5zhyA',
 'EGnYaXaovJI',
 'r49Uf0thyiE',
 '_rJXn0qRlBo',
 'uTPRsthfgX4',
 'N30r174CsWM',
 'dKteixFJqrk',
 'oakQuOe1wLA',
 '1-xQpZ9mssk',
 '3sIc5BtdP7M',
 'yL1cxrDLm2A',
 '3mVK0oYg4RQ',
 'T-n9OMVbJMM',
 '9a9tgSeQU5c',
 'GLUYnFWwS0o']


    # Provide your API key here
    api_key = "AIzaSyBPshcz6o-C-JD5uf3uQTBxrGcGKHGMR6o"

    # Authenticate with YouTube API using API key
    youtube_client = authenticate_youtube_api(api_key)

    # Retrieve details for the provided video IDs
    video_details_list = video_details(youtube_client, video_ids)

    # Save video details to a JSON file
    with open('video_details.json', 'w') as json_file:
        json.dump(video_details_list, json_file, indent=4)

    print("Video details saved to 'video_details.json'")
