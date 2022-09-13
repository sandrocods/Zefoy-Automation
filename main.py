import datetime
import time, random
from src import process
from colorama import init, Fore


def main():
    init(autoreset=True)
    inject = process.ZefoyViews()
    print(
        Fore.GREEN + """
      _____ _ _  __   ___
     |_   _(_) |_\ \ / (_)_____ __ _____
       | | | | / /\ V /| / -_) V  V (_-<
       |_| |_|_\_\ \_/ |_\___|\_/\_//__/
       make with ❤️️ by @sandroputraa
    """
    )
    print(Fore.LIGHTYELLOW_EX + "Example: https://www.tiktok.com/@awokwokwokwkokwow/video/6940134095989050626")
    url_video = input("Enter URL Video: ")

    inject.get_session_captcha()
    time.sleep(1)

    if inject.post_solve_captcha(captcha_result=inject.captcha_solver()):

        print("\n[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + "Success Solve Captcha" + "\n")

        while True:

            inject_views = inject.send_views(
                url_video=url_video
            )

            if "Please try again later" in inject_views:
                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_views)
                exit()

            elif "Successfully views sent." in inject_views:
                print("[ " + str(
                    datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + inject_views + " to " + Fore.LIGHTYELLOW_EX + "" + url_video,
                      end="\n\n")

            else:
                for i in range(int(inject_views), 0, -1):
                    print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTYELLOW_EX + "Please wait " + str(
                        i) + " seconds to send views again.", end="\r")
                    time.sleep(1)

            time.sleep(random.randint(1, 5))

    else:
        print(Fore.RED + "Failed to solve captcha.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "Exit")
        exit()
