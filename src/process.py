import re
import base64
import requests
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# for debug
# from requests_toolbelt.utils import dump

class ZefoyViews:
    API_ZEFOY = 'https://zefoy.com/'
    API_VISION = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAUbA4T8UWO-pw750uQqz0X2deq9lHLuLk'

    STATIC_HEADERS = {
        "origin": "https://zefoy.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        'Host': 'zefoy.com',

    }

    def __init__(self):
        self.key_views = None
        self.session = requests.Session()
        self.captcha = None
        self.phpsessid = None

    def captcha_solver(self):
        solve_captcha = requests.post(
            url=self.API_VISION,
            headers={
                'Content-Type': 'application/json',
                'Host': 'vision.googleapis.com',
                'x-android-package': 'image.to.text.ocr',
                'x-android-cert': 'ad32d34755bb3b369a2ea8dfe9e0c385d73f80f0',
            },
            json={
                "requests": [
                    {
                        "image": {
                            "content": base64.b64encode(open('captcha.png', 'rb').read()).decode('utf-8')
                        },
                        "features": [
                            {
                                "type": "TEXT_DETECTION",
                                "maxResults": 1
                            }
                        ]
                    }
                ]
            }
        )
        return solve_captcha.json()['responses'][0]['textAnnotations'][0]['description'].lower()

    def get_session_captcha(self):
        request_session = self.session.get(
            url=self.API_ZEFOY,
            headers=self.STATIC_HEADERS,
        )

        if not "Extremely Superfast" in request_session.text:
            return False

        soup = BeautifulSoup(request_session.text, 'html.parser')

        # Download Captcha Image

        request_captcha_image = self.session.get(
            url=self.API_ZEFOY + soup.find('img', {'alt': 'CAPTCHA code'}).get('src'),
            headers=self.STATIC_HEADERS,
        )

        with open('captcha.png', 'wb') as f:
            f.write(request_captcha_image.content)

        self.phpsessid = request_session.cookies.get_dict()['PHPSESSID']

    def post_solve_captcha(self, captcha_result):

        try:
            self.STATIC_HEADERS['cookie'] = "PHPSESSID=" + self.phpsessid
            self.STATIC_HEADERS['content-type'] = "application/x-www-form-urlencoded; charset=UTF-8"

            post_captcha = self.session.post(
                url=self.API_ZEFOY,
                headers=self.STATIC_HEADERS,
                data={
                    'captcha_secure': captcha_result,
                    'r75619cf53f5a5d7aa6af82edfec3bf0': '',
                }
            )
            soup = BeautifulSoup(post_captcha.text, 'html.parser')
            self.key_views = soup.find('input', {'placeholder': 'Enter Video URL'}).get('name')
            return True
        except Exception as e:
            return "Error: " + str(e)

    def send_views(self, url_video):
        try:
            self.STATIC_HEADERS['cookie'] = "PHPSESSID=" + self.phpsessid
            request_send_views = self.session.post(
                url=self.API_ZEFOY + 'c2VuZC9mb2xsb3dlcnNfdGlrdG9V',
                headers=self.STATIC_HEADERS,
                data={
                    self.key_views: url_video,
                }
            )
            # https://stackoverflow.com/questions/58120947/base64-and-xor-operation-needed
            decode = base64.b64decode(urllib.parse.unquote(request_send_views.text[::-1])).decode()

            if "An error occurred. Please try again." in decode:

                decode = self.force_send_views(
                    url_video=url_video,
                    old_request=decode
                )
                if "Successfully views sent." in decode:
                    return "Successfully views sent."

            elif "Successfully views sent." in decode:
                return "Successfully views sent."

            elif "Please try again later. Server too busy." in decode:
                return "Please try again later. Server too busy."

            elif "Session Expired. Please Re Login!" in decode:
                return "Session Expired. Please Re Login!"

            # elif "Too many requests. Please slow down." in decode:
            #     return "Too many requests. Please slow down."

            try:
                return re.search(r"ltm=[0-9]+", decode).group(0).replace("ltm=", "")
            except:
                match = re.findall(r" = [0-9]+", decode)
                return match[0].replace(" = ", "")

        except Exception as e:
            pass

    def force_send_views(self, url_video, old_request):

        if 'tiktok' in url_video:
            if len(urlparse(url_video).path.split('/')[-1]) == 19:
                valid_id = urlparse(url_video).path.split('/')[-1]
            else:
                return False
        else:
            return False

        parse = BeautifulSoup(old_request, 'html.parser')

        self.STATIC_HEADERS['cookie'] = "PHPSESSID=" + self.phpsessid
        request_send_views = requests.post(
            url=self.API_ZEFOY + 'c2VuZC9mb2xsb3dlcnNfdGlrdG9V',
            headers=self.STATIC_HEADERS,
            data={
                parse.find('input', {'type': 'text'}).get('name'): valid_id,
            }
        )
        decode = base64.b64decode(urllib.parse.unquote(request_send_views.text[::-1])).decode()
        return decode
