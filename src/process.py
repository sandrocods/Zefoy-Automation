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
    API_VISION = 'https://api.sandroputraa.com/zefoy.php'

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
                'Auth': 'sandrocods',
                'Host': 'api.sandroputraa.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            },
            json={
                "img": base64.b64encode(open('captcha.png', 'rb').read()).decode('utf-8')
            }
        )
        if solve_captcha.status_code == 200 and solve_captcha.json()['Message'] == 'Success':
            return solve_captcha.json()['Data']
        else:
            exit("Error: " + solve_captcha.json()['message'])

    def get_session_captcha(self):
        request_session = self.session.get(
            url=self.API_ZEFOY,
            headers=self.STATIC_HEADERS,
        )

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

            soup = BeautifulSoup(decode, 'html.parser')

            if "An error occurred. Please try again." in decode:

                self.force_send_views(
                    url_video=url_video,
                    old_request=decode
                )

                if "Successfully views sent." in decode:
                    return {
                        'message': 'Successfully views sent.',
                        'data': soup.find('button').text.strip()
                    }
                else:
                    return {
                        'message': 'Another State',
                        'data': soup.find('button').text.strip()
                    }

            elif "Successfully views sent." in decode:
                return {
                    'message': 'Successfully views sent.',
                    'data': soup.find('button').text.strip()
                }

            # elif "Please try again later. Server too busy." in decode:
            #     return {
            #         'message': 'Please try again later. Server too busy.',
            #     }

            elif "Session Expired. Please Re Login!" in decode:
                return {
                    'message': 'Please try again later. Server too busy.',
                }

            try:
                return {
                    'message': re.search(r"ltm=[0-9]+", decode).group(0).replace("ltm=", "")
                }
            except:
                match = re.findall(r" = [0-9]+", decode)
                return {
                    'message': match[0].replace(" = ", "")
                }

        except Exception:
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

    def send_shares(self, url_video):
        try:
            self.STATIC_HEADERS['cookie'] = "PHPSESSID=" + self.phpsessid
            request_send_views = self.session.post(
                url=self.API_ZEFOY + 'c2VuZC9mb2xsb3dlcnNfdGlrdG9s',
                headers=self.STATIC_HEADERS,
                data={
                    self.key_views: url_video,
                }
            )
            # https://stackoverflow.com/questions/58120947/base64-and-xor-operation-needed
            decode = base64.b64decode(urllib.parse.unquote(request_send_views.text[::-1])).decode()

            soup = BeautifulSoup(decode, 'html.parser')

            if "An error occurred. Please try again." in decode:

                self.force_send_shares(
                    url_video=url_video,
                    old_request=decode
                )

                if "Shares successfully sent." in decode:
                    return {
                        'message': 'Shares successfully sent.',
                        'data': soup.find('button').text.strip()
                    }
                else:
                    return {
                        'message': 'Another State',
                        'data': soup.find('button').text.strip()
                    }

            elif "Shares successfully sent." in decode:
                return {
                    'message': 'Successfully views sent.',
                    'data': soup.find('button').text.strip()
                }

            # elif "Please try again later. Server too busy." in decode:
            #     return {
            #         'message': 'Please try again later. Server too busy.',
            #     }

            elif "Session Expired. Please Re Login!" in decode:
                return {
                    'message': 'Please try again later. Server too busy.',
                }

            try:
                return {
                    'message': re.search(r"ltm=[0-9]+", decode).group(0).replace("ltm=", "")
                }
            except:
                match = re.findall(r" = [0-9]+", decode)
                return {
                    'message': match[0].replace(" = ", "")
                }

        except Exception:
            pass

    def force_send_shares(self, url_video, old_request):

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
            url=self.API_ZEFOY + 'c2VuZC9mb2xsb3dlcnNfdGlrdG9s',
            headers=self.STATIC_HEADERS,
            data={
                parse.find('input', {'type': 'text'}).get('name'): valid_id,
            }
        )
        decode = base64.b64decode(urllib.parse.unquote(request_send_views.text[::-1])).decode()
        return decode

    def send_favorites(self, url_video):
        try:
            self.STATIC_HEADERS['cookie'] = "PHPSESSID=" + self.phpsessid
            request_send_views = self.session.post(
                url=self.API_ZEFOY + 'c2VuZF9mb2xsb3dlcnNfdGlrdG9L',
                headers=self.STATIC_HEADERS,
                data={
                    self.key_views: url_video,
                }
            )
            # https://stackoverflow.com/questions/58120947/base64-and-xor-operation-needed
            decode = base64.b64decode(urllib.parse.unquote(request_send_views.text[::-1])).decode()

            soup = BeautifulSoup(decode, 'html.parser')

            if "An error occurred. Please try again." in decode:

                self.force_send_favorites(
                    url_video=url_video,
                    old_request=decode
                )

                if "Favorites successfully sent." in decode:
                    return {
                        'message': 'Favorites successfully sent.',
                        'data': soup.find('button').text.strip()
                    }
                else:
                    return {
                        'message': 'Another State',
                        'data': soup.find('button').text.strip()
                    }

            elif "Favorites successfully sent." in decode:
                return {
                    'message': 'Favorites successfully sent.',
                    'data': soup.find('button').text.strip()
                }

            # elif "Please try again later. Server too busy." in decode:
            #     return {
            #         'message': 'Please try again later. Server too busy.',
            #     }

            elif "Session Expired. Please Re Login!" in decode:
                return {
                    'message': 'Please try again later. Server too busy.',
                }

            try:
                return {
                    'message': re.search(r"ltm=[0-9]+", decode).group(0).replace("ltm=", "")
                }
            except:
                match = re.findall(r" = [0-9]+", decode)
                return {
                    'message': match[0].replace(" = ", "")
                }

        except Exception:
            pass

    def force_send_favorites(self, url_video, old_request):

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
            url=self.API_ZEFOY + 'c2VuZF9mb2xsb3dlcnNfdGlrdG9L',
            headers=self.STATIC_HEADERS,
            data={
                parse.find('input', {'type': 'text'}).get('name'): valid_id,
            }
        )
        decode = base64.b64decode(urllib.parse.unquote(request_send_views.text[::-1])).decode()
        return decode
