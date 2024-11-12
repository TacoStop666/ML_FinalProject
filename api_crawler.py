import requests
import csv
import os
import random
import time

class IG_API_Parser:
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id
        self.folder_name = 'result/'
        self.create_csv()

    def create_csv(self):
        csv_file = os.path.join(self.folder_name, 'output2.csv')
        if not os.path.exists(csv_file):
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Post Index', 'followers', 'upload time', 'Like Count', 'Comment Count', 'is Photo', 'hashtag', 'Pic Description'])

    def save_to_csv(self, post_idx, followers, upload_time, like_count, comment_count, is_photo, hashtags, pic_description):
        csv_file = os.path.join(self.folder_name, 'output2.csv')
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([post_idx, followers, upload_time, like_count, comment_count, is_photo, hashtags, pic_description])

    def get_user_followers(self):
        url = f"https://graph.instagram.com/{self.user_id}?fields=followers_count&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("followers_count", 0)
        else:
            print("Error fetching followers data:", response.json())
            return 0

    def get_user_media(self):
        url = f"https://graph.instagram.com/{self.user_id}/media?fields=id,caption,media_type,like_count,comments_count,timestamp&access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            print("Error fetching media data:", response.json())
            return []

    def parse_data(self):
        followers = self.get_user_followers()
        posts = self.get_user_media()
        
        for idx, post in enumerate(posts):
            like_count = post.get('like_count', 0)
            comment_count = post.get('comments_count', 0)
            upload_time = post.get('timestamp', '')
            is_photo = (post.get('media_type', '') == 'IMAGE')
            hashtags = [tag for tag in post.get('caption', '').split() if tag.startswith('#')]
            pic_description = post.get('caption', '')

            self.save_to_csv(idx, followers, upload_time, like_count, comment_count, is_photo, hashtags, pic_description)

# access token + user ID

# crawler
if __name__ == '__main__':
    download_num = 500
    retry_count = 0
    max_retries = 500

    while retry_count < max_retries:
        try:
            parser = IG_API_Parser(access_token, user_id)
            # parser.start_parse(download_num)
            parser.parse_data()

            print('下載完成')
            break
        except Exception as e:
            retry_count += 1
            print(f'error: {e}')
            print('retry no. {retry_count}')
            
            # add delay
            delay_retry = random.uniform(1, 3)
            print(f'Sleeping for {delay_retry:.2f} seconds before retry')
            time.sleep(delay_retry)