import os, re, json
from datetime import datetime

print("##### Index's Anime RSS Feed Downloader Generator for qBittorrent v1.1 #####")

# I would in general recommend to first install qBittorrent and set up separate RSS feeds for the subgroups that you want to use.
# By default, this program should detect and find all subgroups that are longer than 2 characters, as long as the name of your RSS feeds in qBittorrent include the subgroup name.
# The following variables can be changed to fit your needs.
# There are a more detailed explanations on the GitHub: https://github.com/anotherindex/Anime-RSS-Feed-Downloader-Generator-for-qBittorrent


##### MAIN DOWNLOAD SETTINGS #####

# DOWNLOAD FOLDER
# This is the folder where your anime will be downloaded to. If you leave it blank it will use the default download folder you set in qBittorrent.
download_folder = r""

# CURRENT FOLDER AS DOWNLOAD FOLDER
# If this option is set to True, then the script will use its own location as the destination download folder. Great for when you move it from folder to folder or have a bunch of separate folders.
# This option also has higher priority than the above-mentioned "download_folder" variable, so if it's set to True the "download_folder" path will be ignored.
current_folder_as_download_folder = False

# SEPARATE DOWNLOAD FOLDERS
# If you want to download each show into its own individual folder (with the name of the show as the folder name) you can set this to True, otherwise set it to False.
save_every_anime_in_a_separate_folder = False


##### ADVANCED DOWNLOAD SETTINGS #####

# CUSTOM BLACKLISTED PHRASES
# Enter all phrases you want the downloaded filenames NOT to contain in here, it works exactly like the "Must Not Contain:" field in qBittorrent so look up its formatting rules in case you want to make use of this.
# Before you type something like "480p" in here I would in general HIGHLY recommend filtering those things out within the RSS feed URL itself, not the RSS downloader configuration.
custom_must_not_contain_values = ""

# USE SHORTENED ANIME TITLES IN RSS SEARCH
# Some anime titles are really long, and it might be more reliable to shorten really long titles while searching through the RSS feed.
# This does not change the name of any files or folders and should only be set to "False" if the RSS downloader keeps downloading wrong shows with similar titles.
use_shortened_anime_titles_in_RSS_match = True

# MANUAL FILE PATH TO FEEDS JSON
# If you use for example a portable version of qBittorrent or have an unusual folder structure and this program can't find the 'feeds.json' file on your PC please enter the full file path down below. An example would be:
# manual_file_path_to_feeds_json = r"D:\Users\YourUsername\Documents\qBittorrent\config\rss\feeds.json"
# It is usually located in the 'C:\Users\YourUsername\AppData\Roaming\qBittorrent\rss' folder and this program should be able to detect it, but there might be exceptions.
manual_file_path_to_feeds_json = r""

# SUBGROUP SEARCH DICTIONARY
# This dictionary makes finding subgroups more reliable by associating the subgroup with a search term. (It also exists for visual reasons.)
# You should not need to add extra subgroups to this as the script should generally find subgroups not included in this dictionary just fine, as long as you named your RSS feed correctly in qBittorrent.
# This can however help with subgroups that have weird naming schemes or trouble getting detected.
# NOTE: If you want to use subgroups shorter than 3 letters you WILL have to add them to this dictionary, maybe even consider using brackets as the search term and in your RSS feed name like: "[gg]": "[gg]",
subgroup_search_dictionary = {
    "[SubsPlease]": "subsplease",
    "[Erai-raws]": "erai",
    "[EMBER]": "ember",
    "[ASW]": "asw",
    "[ToonsHub]": "toonshub",
    "[Shiniori-Raws]": "shiniori",
    "[Judas]": "judas",
    "[DKB]": "dkb",
    "[Anime Time]": "anime time",
}

# MY RSS FEEDS
# I would recommend using the 'feeds.json' method and leaving this variable untouched, but if the 'feeds.json' method doesn't work you can alternatively enter the RSS feeds you use down below.
# They need to be the same links as in your qBittorrent, so if you use for example "https://nyaa.si/?page=rss&q=subsplease+1080&c=0_0&f=0" as your RSS feed for SubsPlease
# then you need to enter the same exact link down below, like "[SubsPlease]": "https://nyaa.si/?page=rss&q=subsplease+1080&c=0_0&f=0",
my_RSS_feeds = {
    "[SubsPlease]": "",
    "[Erai-raws]": "",
    "[EMBER]": "",
}

############################################

# global variables
current_folder = str(os.path.dirname(__file__))
file_list = os.listdir(current_folder)
appdata_file = fr"""{os.getenv('APPDATA')}\qBittorrent\rss\feeds.json"""
qBittorrent_ini_file = fr"""{os.getenv('APPDATA')}\qBittorrent\qBittorrent.ini"""
added_shows = []
final_output = {}
potential_RSS_feeds = {}

default_path = ""
if os.path.isfile(qBittorrent_ini_file):
    try:
        with open(qBittorrent_ini_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("Session\\DefaultSavePath="):
                    default_path = line.split('=', 1)[1].strip()
                    default_path = default_path.replace("\\\\", "\\")
    except Exception as e:
        default_path = "<Default qBittorrent path>"
else:
    default_path = "<Default qBittorrent path>"


def my_RSS_feeds_check():
    rss_names = []
    for current_RSS_feed in my_RSS_feeds:
        if my_RSS_feeds[current_RSS_feed] != "":
            rss_names.append(current_RSS_feed)
    if rss_names:
        return rss_names
    else:
        return False


def check_for_feeds_json():
    global potential_RSS_feeds
    if manual_file_path_to_feeds_json != "":
        if os.path.exists(manual_file_path_to_feeds_json):
            feeds_location = manual_file_path_to_feeds_json
        else:
            print("WARNING: You entered a custom path for the 'Manual file path to feeds.json file' variable, but there doesn't seem to be a file at that file location.")
            print("Trying to locate the file in the usual location...")
            if os.path.exists(appdata_file):
                feeds_location = appdata_file
                print("Found a 'feeds.json' file in the default file location.")

            else:
                input("Did not manage to find a 'feeds.json' file in the default file location.\nPlease close the program and add a proper filepath.")
                quit()

    elif os.path.exists(appdata_file):
        feeds_location = appdata_file
    else:
        return False
    with open(feeds_location, "r") as file:
        data = json.load(file)
        for current_entry in subgroup_search_dictionary:
            for key, value in data.items():
                potential_RSS_feeds[key] = value.get("url")
                if subgroup_search_dictionary[current_entry] in key.lower():
                    my_RSS_feeds[current_entry] = value.get("url")

        temp_values = set(my_RSS_feeds.values())
        potential_RSS_feeds = {key: value for key, value in potential_RSS_feeds.items() if value not in temp_values}

    return True


def get_title_and_subgroup(full_filename):
    subgroup_regex_search = re.search("^\[[^+]*?]", full_filename)
    anime_title_regex_search_strong = re.search("] (.*?) - \d", full_filename)
    anime_title_regex_search_weak = re.search("] (.*?) - ", full_filename)

    try:
        subgroup_name_return = subgroup_regex_search.group()
        if anime_title_regex_search_strong:
            anime_title_return = anime_title_regex_search_strong.group()[2:-4]
        else:
            anime_title_return = anime_title_regex_search_weak.group()[2:-3]

        for current_entry in subgroup_search_dictionary:
            if subgroup_search_dictionary[current_entry] in subgroup_name_return.lower():
                subgroup_name_return = current_entry

        return subgroup_name_return, anime_title_return
    except AttributeError:
        return 0, 0


def add_data_to_json(subgroup_name, anime_title, RSS_feed_URL=""):
    RSS_title = anime_title
    if RSS_feed_URL == "":
        affected_feeds = my_RSS_feeds[subgroup_name]
    else:
        affected_feeds = RSS_feed_URL

    if use_shortened_anime_titles_in_RSS_match:
        if len(anime_title) > 30:
            words = anime_title.split()
            while len(" ".join(words)) > 30:
                words.pop()
            must_contain = (" ".join(words))

        else:
            must_contain = anime_title

    else:
        must_contain = anime_title

    if download_folder == "":
        save_path = ""
    else:
        save_path = download_folder

    if current_folder_as_download_folder:
        save_path = current_folder

    if save_every_anime_in_a_separate_folder:
        if default_path == "<Default qBittorrent path>":
            save_path = ""
        elif save_path == "":
            save_path = default_path + f"\\{anime_title}"
        else:
            save_path += f"\\{anime_title}"

    final_output[RSS_title] = {
        "addPaused": None,
        "affectedFeeds": [affected_feeds],
        "assignedCategory": "",
        "enabled": True,
        "episodeFilter": "",
        "ignoreDays": 0,
        "lastMatch": "",
        "mustContain": must_contain,
        "mustNotContain": custom_must_not_contain_values,
        "previouslyMatchedEpisodes": [],
        "priority": 0,
        "savePath": save_path,
        "smartFilter": False,
        "torrentContentLayout": "",
        "torrentParams": {
            "category": "",
            "download_limit": -1,
            "download_path": "",
            "inactive_seeding_time_limit": -2,
            "operating_mode": "AutoManaged",
            "ratio_limit": -2,
            "save_path": save_path.replace("\\","/"),
            "seeding_time_limit": -2,
            "share_limit_action": "Default",
            "skip_checking": False,
            "ssl_certificate": "",
            "ssl_dh_params": "",
            "ssl_private_key": "",
            "tags": [],
            "upload_limit": -1,
            "use_auto_tmm": bool(not bool(save_path))
        },
        "useRegex": False
    }


if __name__ == "__main__":
    print("\nSettings:")
    if download_folder == "":
        print(f"Manually set download folder: No")
    else:
        print(f"Manually set download folder: '{download_folder}'")
    print(f"Current folder set as download folder: {current_folder_as_download_folder}")
    print(f"Save every anime in a separate folder: {save_every_anime_in_a_separate_folder}")

    if default_path == "<Default qBittorrent path>" and save_every_anime_in_a_separate_folder:
        print(f"""Your setup triggered an exception because this script could not detect a default path and you have the option for separate anime folders selected."""
              f"""\nBecause of limitations you will eiter have to set the "download_folder" manually by opening and editing this file or alternatively accept that this script will work with only the default path and no separate anime title folders.
              \nBecause of that the download folder will be: {default_path}""")
    else:
        if current_folder_as_download_folder:
            print(f"Because of that the download folder will be: {current_folder}\<Anime Title>" if save_every_anime_in_a_separate_folder else f"Because of that the download folder will be: {current_folder}")
        else:
            print(f"Because of that the download folder will be: {default_path}\<Anime Title>" if save_every_anime_in_a_separate_folder else f"Because of that the download folder will be: {default_path}")

    print(f"Use shortened anime titles for RSS matching: {use_shortened_anime_titles_in_RSS_match}")
    if manual_file_path_to_feeds_json == "":
        print(f"Manual feed.json file location set: No")
    else:
        print(f"Manual 'feed.json' file location set: Yes: {manual_file_path_to_feeds_json}")

    if custom_must_not_contain_values == "":
        print(f"No 'Must Not Contain' phrases were set.")
    else:
        print(f"The following 'Must Not Contain' phrases are used: {custom_must_not_contain_values}")

    print("\n ---  STEP 1 - Searching for RSS feeds to use  --- ")
    if my_RSS_feeds_check():
        print(f"Found RSS feeds for {', '.join(my_RSS_feeds_check())} in this python file. Will continue to use these.")

    else:
        feeds_json_results = check_for_feeds_json()

        if my_RSS_feeds_check():
            print(f"Found RSS feeds for {', '.join(my_RSS_feeds_check())}{f' and {len(potential_RSS_feeds)} potential other RSS feed(s)' if potential_RSS_feeds else ''} in qBittorrent's 'feeds.json' file and will work with those.")

        elif feeds_json_results:
            input("Couldn't find any RSS feeds in this file (you can open the file and add yours), and while this program did manage to find qBittorrent's 'feeds.json' file there weren't any subgroups in there."
                  "\nPlease open your qBittorrent Client, go to the RSS section (View -> RSS Reader, then click on the RSS tab) and add 'subscriptions' and preferably name them like the supported subgroups, so 'SubsPlease', 'Erai-raws', 'Ember'. "
                  "\nThen close and run this file again.")
            quit()
        else:
            input("Found neither RSS feeds in this file (you can open the file and add yours), nor did this program manage to find qBittorrent's feeds.json file where your RSS feeds are stored. \nPlease make sure qBittorrent is properly installed!\nIf it still doesn't work open this file in a text editor and preferably enter the directory to the 'feeds.json' file or alternatively enter your RSS feeds.")
            quit()

    print("\n ---  STEP 2 - Searching for anime in this folder  --- ")
    sg_table_width = int(max(len(key) for key in my_RSS_feeds)) + 2
    title_table_width = 70
    table_fill_character = " "
    print(f"""╔═══╦═{sg_table_width * "═"}╦{title_table_width * "═"}╗\n║ = ║ Sub Group{(sg_table_width - 10) * " "} ║ Anime Title {(title_table_width - 13) * " "}║\n╠═══╬═{sg_table_width * "═"}╬{title_table_width * "═"}╣""")

    usable_RSS_feeds = my_RSS_feeds_check()
    for current_file in file_list:
        if bool(re.search(".mkv|.mp4", current_file)):
            subgroup_name, anime_title = get_title_and_subgroup(current_file)
            if subgroup_name == 0 or anime_title == 0:
                print(f"""║ ! ║ Missing? {(sg_table_width - 9) * " "}║ File: {(current_file[0:title_table_width - 10] + '...') if len(current_file) > (title_table_width - 7) else (current_file.ljust((title_table_width - 7), table_fill_character))}║""")
            else:
                if anime_title in added_shows:
                    pass
                elif subgroup_name not in usable_RSS_feeds:
                    if potential_RSS_feeds:
                        if len(subgroup_name[1:-1]) > 2:
                            subgroup_name_match = next(
                                (key for key in potential_RSS_feeds.keys() if subgroup_name[1:-1].lower() in key.lower()),
                                None
                            )
                            if subgroup_name_match:
                                print(f"""║ + ║ {subgroup_name}* {(sg_table_width - len(subgroup_name) - 2) * " "}║ {(anime_title[0:title_table_width - 3] + '...') if len(anime_title) > title_table_width else (anime_title.ljust((title_table_width - 1), table_fill_character))}║""")
                                add_data_to_json(subgroup_name, anime_title, potential_RSS_feeds[subgroup_name_match])
                                added_shows.append(anime_title)
                            else:
                                print(f"""║ ! ║ {subgroup_name}?{(sg_table_width - len(subgroup_name) - 1) * " "}║ Subgroup not found in any RSS feed for: {(anime_title[0:title_table_width - 44] + '...') if len(anime_title) > (title_table_width - 40) else (anime_title.ljust((title_table_width - 41), table_fill_character))}║""")
                        else:
                            print(f"""║ ! ║ {subgroup_name}?{(sg_table_width - len(subgroup_name) - 1) * " "}║ Subgroup name too short, please add to RSS dictionary: {(anime_title[0:title_table_width - 59] + '...') if len(anime_title) > (title_table_width - 59) else (anime_title.ljust((title_table_width - 59), table_fill_character))}║""")
                    else:
                        print(f"""║ ! ║ {subgroup_name}?{(sg_table_width - len(subgroup_name) - 1) * " "}║ Subgroup not found in any RSS feed for: {(anime_title[0:title_table_width - 44] + '...') if len(anime_title) > (title_table_width - 40) else (anime_title.ljust((title_table_width - 41), table_fill_character))}║""")
                else:
                    print(f"""║ + ║ {subgroup_name} {(sg_table_width - len(subgroup_name) - 1) * " "}║ {(anime_title[0:title_table_width - 4] + '...') if len(anime_title) > (title_table_width) else (anime_title.ljust((title_table_width - 1), table_fill_character))}║""")
                    add_data_to_json(subgroup_name, anime_title)
                    added_shows.append(anime_title)
        else:
            pass

    print(f"""╠═══╬═{sg_table_width * "═"}╩{title_table_width * "═"}╣""")
    print(f"""║ = ║ Found {len(added_shows)} anime with associated subgroup(s).{(title_table_width - 27 - (len(str(len(added_shows))))) * " "} ║""")
    print(f"""╚═══╩═{(sg_table_width + title_table_width + 1) * "═"}╝\n""")
    print(" ---  STEP 3 - Creating a .json file  --- ")
    current_time = datetime.now().strftime("%Y_%m_%d at %H_%M_%S")
    output_file = f"Anime RSS Feed for {len(added_shows)} shows - created on {current_time}.json"
    with open(output_file, "w") as file:
        json.dump(final_output, file, indent=4)
    input(f"A .json file with the title '{output_file}' has been successfully created. \nYou can now import that file into qBittorrent's RSS Downloader.\n\n(You may now close this window or press Enter...)")
