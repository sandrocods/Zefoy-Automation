import datetime
import random
import time
import inquirer
from colorama import init, Fore
from src import process
from prettytable import PrettyTable


def main():
    init(autoreset=True)
    inject = process.ZefoyViews()
    inject.get_session_captcha()

    print(Fore.GREEN + """
      _____ _ _  __   ___
     |_   _(_) |_\ \ / (_)_____ __ _____
       | | | | / /\ V /| / -_) V  V (_-<
       |_| |_|_\_\ \_/ |_\___|\_/\_//__/
       make with ❤️️ by @sandroputraa
    """)
    print(Fore.LIGHTYELLOW_EX + "Example: https://www.tiktok.com/@awokwokwokwkokwow/video/6865609642974743810")
    url_video = input("Enter URL Video: ")
    if url_video == "":
        url_video = "https://www.tiktok.com/@awokwokwokwkokwow/video/6865609642974743810"
    time.sleep(1)

    if inject.post_solve_captcha(captcha_result=inject.captcha_solver()):

        print("\n[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + "Success Solve Captcha" + "\n")

        table = PrettyTable(field_names=["Services", "Status"], title="Status Services", header_style="upper",
                            border=True)
        status_services = inject.get_status_services()
        if not status_services: print("Failed to get status services, try again later"); exit()

        valid_services = []
        for service in status_services:
            if service['name'] == 'Followers' or service['name'] == 'Comments Hearts':
                continue
            elif 'ago updated' in service['status']:
                valid_services.append(service['name'])

            table.add_row([service['name'], Fore.GREEN + service['status'] + Fore.RESET if 'ago updated' in service[
                'status'] else Fore.RED + service['status'] + Fore.RESET])

        table.title = Fore.YELLOW + " Total Online Services: " + str(len(valid_services)) + Fore.RESET
        print(table)

        questions = [
            inquirer.List('type', message="What services do you need?", choices=valid_services, carousel=True, ), ]
        answers = inquirer.prompt(questions)

        while True:

            try:

                if answers['type'] == 'Views':

                    while True:
                        inject_views = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_views:

                            if inject_views['message'] == "Please try again later":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_views[
                                    'message'])
                                exit()

                            elif inject_views['message'] == 'Another State':
                                print("[ " + str(
                                    datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + "Current Views: " +
                                      inject_views['data'], end="\r")


                            elif inject_views['message'] == "Successfully views sent.":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + inject_views[
                                    'message'] + " to " + Fore.LIGHTYELLOW_EX + "" + url_video + ", " + Fore.LIGHTGREEN_EX + "Current Views: " +
                                      inject_views['data'], end="\n\n")
                                print()

                            elif inject_views['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_views[
                                    'message'])
                                exit()

                            elif inject_views['message'] == "Video not found.":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_views[
                                    'message'])
                                exit()

                            else:
                                for i in range(int(inject_views['message']), 0, -1):
                                    print("[ " + str(
                                        datetime.datetime.now()) + " ] " + Fore.LIGHTYELLOW_EX + "Please wait " + str(
                                        i) + " seconds to send views again.", end="\r")
                                    time.sleep(1)

                            time.sleep(random.randint(1, 5))

                        else:
                            pass

                elif answers['type'] == 'Shares':

                    while True:
                        inject_shares = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_shares:

                            if inject_shares['message'] == "Please try again later":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_shares[
                                    'message'])
                                exit()

                            elif inject_shares['message'] == 'Another State':
                                print("[ " + str(
                                    datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + "Current Shares : " +
                                      inject_shares['data'], end="\n\n")
                                print()


                            elif inject_shares['message'] == "Shares successfully sent.":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + inject_shares[
                                    'message'] + " to " + Fore.LIGHTYELLOW_EX + "" + Fore.LIGHTGREEN_EX + "Current Shares: " +
                                      inject_shares['data'], end="\r")


                            elif inject_shares['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_shares[
                                    'message'])
                                exit()

                            elif inject_shares['message'] == "Video not found.":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_shares[
                                    'message'])
                                exit()

                            else:
                                for i in range(int(inject_shares['message']), 0, -1):
                                    print("[ " + str(
                                        datetime.datetime.now()) + " ] " + Fore.LIGHTYELLOW_EX + "Please wait " + str(
                                        i) + " seconds to send Shares again.", end="\r")
                                    time.sleep(1)

                            time.sleep(random.randint(1, 5))

                        else:
                            pass

                elif answers['type'] == 'Favorites':

                    while True:
                        inject_favorites = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_favorites:

                            if inject_favorites['message'] == "Please try again later":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_favorites[
                                    'message'])
                                exit()

                            elif inject_favorites['message'] == 'Another State':
                                print("[ " + str(
                                    datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + "Current Favorites : " +
                                      inject_favorites['data'], end="\r")


                            elif inject_favorites['message'] == "Favorites successfully sent.":
                                print(
                                    "[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + inject_favorites[
                                        'message'] + " to " + Fore.LIGHTYELLOW_EX + "" + url_video + Fore.LIGHTGREEN_EX + "Current Favorites : " +
                                    inject_favorites['data'], end="\n\n")
                                print()

                            elif inject_favorites['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_favorites[
                                    'message'])
                                exit()

                            elif inject_favorites['message'] == "Video not found.":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_favorites[
                                    'message'])
                                exit()


                            else:
                                for i in range(int(inject_favorites['message']), 0, -1):
                                    print("[ " + str(
                                        datetime.datetime.now()) + " ] " + Fore.LIGHTYELLOW_EX + "Please wait " + str(
                                        i) + " seconds to send Favorites again.", end="\r")
                                    time.sleep(1)

                            time.sleep(random.randint(1, 5))

                        else:
                            pass

                elif answers['type'] == 'Hearts':

                    while True:
                        inject_hearts = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_hearts:

                            if inject_hearts['message'] == "Please try again later":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_hearts[
                                    'message'])
                                exit()

                            elif inject_hearts['message'] == 'Another State':
                                print("[ " + str(
                                    datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + "Current Hearts : " +
                                      inject_hearts['data'], end="\r")


                            elif inject_hearts['message'] == "Hearts successfully sent.":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTGREEN_EX + inject_hearts[
                                    'message'] + " to " + Fore.LIGHTYELLOW_EX + "" + url_video + Fore.LIGHTGREEN_EX + " Current Hearts: " +
                                      inject_hearts['data'], end="\n\n")
                                print()

                            elif inject_hearts['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_hearts[
                                    'message'])
                                exit()

                            elif inject_hearts['message'] == "Video not found.":
                                print("[ " + str(datetime.datetime.now()) + " ] " + Fore.LIGHTRED_EX + inject_hearts[
                                    'message'])
                                exit()

                            else:
                                for i in range(int(inject_hearts['message']), 0, -1):
                                    print("[ " + str(
                                        datetime.datetime.now()) + " ] " + Fore.LIGHTYELLOW_EX + "Please wait " + str(
                                        i) + " seconds to send Hearts again.", end="\r")
                                    time.sleep(1)

                            time.sleep(random.randint(1, 5))

                        else:
                            pass

            except Exception as e:
                pass

    else:
        print(Fore.RED + "Failed to solve captcha.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "Exit")
        exit()
