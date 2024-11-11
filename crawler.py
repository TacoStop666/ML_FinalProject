from DrissionPage import ChromiumPage, errors
import requests
import time
import os
import csv
import re

def extract_like_count(like_text):
    # 使用正則表達式提取數字和單位（如「萬」）
    match = re.search(r'([\d.]+)(萬)?', like_text)
    
    if match:
        # 提取數字部分
        number = float(match.group(1))
        
        # 如果有「萬」單位，則乘以 10000
        if match.group(2) == "萬":
            number *= 10000
        
        # 回傳數值作為整數
        return int(number)
    else:
        # 如果沒有找到數字，返回 None
        return None
    
def extract_possible_description(pic_description):
    # 使用正則表達式匹配 "可能是" 之後的內容
    match = re.search(r'可能是(.+)', pic_description)
    if match:
        return match.group(1).strip()
    else:
        return None

def extract_hashtags(post_text):
    # 使用正則表達式來匹配 hashtag，允許中文、英文、數字，並且以非字母數字或空白結束
    hashtags = re.findall(r'#\w+|#[\u4e00-\u9fff]+', post_text)
    return hashtags


class IG_Parser:
    def __init__(self):
        self.folder_name = 'result/'
        #self.account = account
        self.post_idx = 0
        #self.create_folder(account)
        self.create_csv()
    

    def create_csv(self):
        # Create a CSV file and add headers if it does not already exist
        csv_file = os.path.join(self.folder_name, 'output.csv')
        if not os.path.exists(csv_file):
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Post Index', 'followers', 'upload time', 'Like Count', 'Comment Count', 'is Photo', 'is Video', 'hashtag', 'Pic Description'])

    def save_to_csv(self, like_count, pic_description, comment_count, followers, upload_time, is_photo, is_video, hashtag):
        csv_file = os.path.join(self.folder_name, 'output.csv')
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([self.post_idx, followers, upload_time, like_count, comment_count, is_photo, is_video, hashtag, pic_description])
    
    def get_follower_count(self, profile_page):
        follower_count = ""
        try:
            follower_ele = profile_page.eles('.x5n08af x1s688f')
            follower_count = extract_like_count(follower_ele[1].text)
        except errors.ElementNotFoundError:
            print("找不到粉絲數 element")
        return follower_count

    def navigate_to_user_profile(self, pop_window_ele, page):
        try:
            # Locate the element with the username link
            username_link = pop_window_ele.ele('.x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz  _acan _acao _acat _acaw _aj1- _ap30 _a6hd')  # Update with the correct selector
            new_tab = page.new_tab(username_link.attr('href'))
            new_tab.get(username_link.attr('href'))
            time.sleep(2)  # Adjust delay as necessary for page load
            
            follower_count = self.get_follower_count(new_tab)
            print("Follower count:", follower_count)
            new_tab.close()
            
            return follower_count
        except errors.ElementNotFoundError:
            print("找不到 username link element")
        except errors.ElementLostError:
            print("頁面加載失敗")


    def start_parse(self, download_num):
        url = 'https://www.instagram.com/explore/'
        page = ChromiumPage()
        page.get(url)

        # click first photo
        first_post = page.ele('._aagw')
        first_post.click()

        pop_window_ele = page.ele('.x1cy8zhl x9f619 x78zum5 xl56j7k x2lwn1j xeuugli x47corl')
        for i in range(download_num):
            print('=== 第', i + 1, '個 Post ===')
            retry_count = 0
            img_url = ''
            post_text = ''
            like_count = ''
            datetime = ''
            is_video = ''
            is_photo = ''
            hashtag = ''
            while retry_count < 2:
                try:
                    post_text_ele = pop_window_ele.ele('._ap3a _aaco _aacu _aacx _aad7 _aade')
                    post_text = post_text_ele.text
                    print('post_text:', post_text)
                    hashtag = extract_hashtags (post_text)
                    print('hashtag:', hashtag)

                    #img_url = self.get_img_url(pop_window_ele)
                    #print('img_url:', img_url)

                    like_count = self.get_like_count(pop_window_ele)
                    print('like_count:', like_count)

                    pic_description, is_photo, is_video = self.get_pic_description(pop_window_ele)
                    print('pic_discription:', pic_description)
                    print('is_photo:', is_photo)
                    print('is_video:', is_video)

                    comment_count = self.get_comment_count(pop_window_ele)
                    print('comment_count:', comment_count)

                    datetime = self.get_datetime(pop_window_ele)
                    print('datetime:', datetime)

                    follower_count = self.navigate_to_user_profile(pop_window_ele, page)
                    print('Follower count for this user:', follower_count)

                    self.save_to_csv(like_count, pic_description, comment_count, follower_count, datetime, is_photo, is_video, hashtag)
                    break
                except errors.ElementNotFoundError:
                    print('該 post 為影片')
                    self.post_idx += 1
                    break
                except errors.ElementLostError:
                    retry_count += 1
                    print('retry:', retry_count)
                    time.sleep(3)

            if (img_url != ''):
                parser.download_img(img_url)
                parser.download_text(post_text)

            self.post_idx += 1

            next_btm = pop_window_ele.ele('. _aaqg _aaqh')
            next_btm.click()

    #def download_img(self, img_url):
        # 使用requests發送HTTP GET請求獲取圖片數據
    #    response = requests.get(img_url)
    #    if response.status_code == 200:
            # 構造保存圖片的文件名
    #        file_name = self.folder_name + '/' + self.account + '_' + str(self.post_idx) + '.jpg'
    #        with open(file_name, 'wb') as f:
    #            f.write(response.content)  # 將圖片數據寫入文件
    #        print(f"Image saved as {file_name}")
    #    else:
    #        print(f"Failed to download image from {img_url}")

    #def download_text(self, text):
    #    file_name = self.folder_name + '/' + self.account + '_' + str(self.post_idx) + '.txt'
    #    with open(file_name, 'w') as f:
    #        f.write(text)
    #    print(f"Text saved as {file_name}")

    #def create_folder(self,folder_name):
    #    if not os.path.exists(self.folder_name):
    #        os.makedirs(self.folder_name)

    #def get_img_url(self,pop_window_ele):
    #    img_url = ''
    #    try:
    #        img = pop_window_ele.ele('.x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3', timeout=2)
    #        img_url = img.attr('src')
    #    except errors.ElementNotFoundError:
    #        print('找不到圖片 element')
    #    return img_url
    
    def get_like_count(self, pop_window_ele):
        like_count = ''
        try:
            # Find the like count element. The selector may need to be updated depending on Instagram's layout.
            like_ele = pop_window_ele.ele('.x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj', timeout=2)
            like_count = extract_like_count(like_ele.text)
        except errors.ElementNotFoundError:
            print('找不到讚數 element')
        return like_count
    def get_pic_description(self, pop_window_ele):
        pic_description = ''
        is_photo = 1
        is_video = 0
        try:
            # Find the like count element. The selector may need to be updated depending on Instagram's layout.
            pic = pop_window_ele.ele('.x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3', timeout=2)
            pic_description = pic.attr('alt')
            pic_description = extract_possible_description(pic_description)
        except errors.ElementNotFoundError:
            print('找不到 pic description')
            is_video = 1
            is_photo = 0
        return pic_description, is_photo, is_video
    
    def get_comment_count(self, pop_window_ele):
        comment_count = 0
        reply_count = 0
        max_clicks = 25  # Set maximum number of clicks
        click_count = 0  # Initialize click counter
        try:
            more_comment = pop_window_ele.ele('.x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xdj266r xat24cr x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh xl56j7k', timeout=2)
            # Click the button until there are no more comments to load or until the limit is reached
            while more_comment is not None and click_count < max_clicks:
                more_comment.click()
                click_count += 1
                more_comment = pop_window_ele.ele('.x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xdj266r xat24cr x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh xl56j7k', timeout=2)

            # Count the main comment elements
            comment_elements = pop_window_ele.eles('.x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1yztbdb x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1', timeout=2)
            comment_count = len(comment_elements)

            # Count the reply elements
            reply_elements = pop_window_ele.eles('._a9yi')
        
            # Extract the text inside the span and parse the number
            for reply_ele in reply_elements:
                print(reply_ele)
                text = reply_ele.text
                print(text)
                if "查看回覆" in text:
                    # Extract the number within parentheses and add it to the count
                    print("success")
                    reply_count += int(text.split('（')[1].split('）')[0])
        except errors.ElementNotFoundError:
            print('找不到 comment')
        except (IndexError, ValueError):
            print('解析查看回覆數字失敗')
        return comment_count+reply_count
    def get_datetime(self, pop_window_ele):
        datetime = ''
        try:
            # Find the like count element. The selector may need to be updated depending on Instagram's layout.
            #datetime_ele = pop_window_ele.ele('.x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1fhwpqd xo1l8bm x1roi4f4 x1s3etm8 x676frb x10wh9bi x1wdrske x8viiok x18hxmgj', timeout=2)
            datetime_ele2 = pop_window_ele.ele('.x1p4m5qa')
            datetime = datetime_ele2.attr('datetime')
        except errors.ElementNotFoundError:
            print('找不到 datetime')
        return datetime
    
if __name__ == '__main__':
    download_num = 10

    parser = IG_Parser()
    parser.start_parse(download_num)

    print('下載完成')
