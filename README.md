# Index's Anime RSS Feed Downloader Generator for qBittorrent

This python script creates anime download rules for the RSS Feed Downloader in qBittorrent from files you have downloaded.    
If you for example have a folder with anime episodes from the currently airing season and you want qBittorrent to automatically download all upcoming episodes from those shows using RSS feeds, this script will generate a .json file that can be imported into qBittorrent's RSS Downloader.    

*Note that just like with [my previous project](https://github.com/anotherindex/anime-screenshot-sorter), this is more of a personal project that I made public because it might also be useful for some people.*

&nbsp;

## Table of Contents
- [Demo Video](#demo-video)
- [How-To](#how-to)
  - [Setup, Installation and Use](#setup-installation-and-use)
- [Settings](#settings)
  - [Download Folder](#download-folder)
  - [Current Folder as Download Folder](#current-folder-as-download-folder)
  - [Separate Download Folders](#separate-download-folders)
- [Advanced Settings](#advanced-settings)
  - [Custom Blacklisted Phrases](#custom-blacklisted-phrases)
  - [Use Shortened Anime Titles in RSS Search](#use-shortened-anime-titles-in-rss-search)
  - [Manual File Path to feeds.json](#manual-file-path-to-feedsjson)
  - [Subgroup Search Dictionary](#subgroup-search-dictionary)
  - [My RSS Feeds](#my-rss-feeds)
- [F.A.Q.](#faq)
  - [qBittorrent Notifications/Errors](#i-successfully-added-the-download-rules-to-the-rss-downloader-but-now-qbittorrent-shows-a-ton-of-notificationserrors-about-either-merging-trackers-or-duplicated-torrents-how-do-i-make-them-stop)
  - [Script Opens in Text Editor](#if-i-doubleclick-on-the-script-it-just-opens-it-in-a-text-editor-instead-of-executing-it-what-do-i-do)

&nbsp;

## Demo Video
<video src="https://github.com/user-attachments/assets/0e911edf-5bff-40d0-8586-7db0b79760ca"></video>

&nbsp;

## How-To

### Setup, Installation and Use
1. Download and install the latest version of qBittorrent. (Older versions should generally work as well.)
2. Install Python version 3.6 or later.
3. Put all the anime episodes you want to add to the RSS Downloader rules into a folder.
4. Add RSS feeds for each subgroup to your qBittorrent and make sure you have the RSS downloader enabled and correctly configured in the settings. *(You will have to figure out how to get RSS feeds from whatever tracker you download torrents from by yourself, but it's usually fairly simple.)*
5. Optional: Edit the preferences of this script by opening it in a text editor.
6. Run this .py script. It should generate a .json file that is called something like `Anime RSS Feed for <number> shows - created on <current date and time>.json`.
7. In qBittorrent go to the RSS Downloader rules and click on "Import..." at the bottom left and select the previously generated .json file.

&nbsp;

## Settings

### Download Folder
This is the folder where your anime will be downloaded to. If you leave it blank, it will use the default download folder you set in qBittorrent.    
Example setting: `download_folder = r"C:\Users\Index\Documents\Anime Downloads"`    
Default setting: `download_folder = r""`

### Current Folder as Download Folder
If this option is set to `True`, the script will use its own location as the destination download folder. Great for when you move it from folder to folder or have a bunch of separate folders.    
This option also has higher priority than the above-mentioned "download_folder" variable, so if it's set to `True`, the "download_folder" path will be ignored.    
Default setting: `current_folder_as_download_folder = False`

### Separate Download Folders
If you want to download each show into its own individual folder (with the name of the show as the folder name), you can set this to `True`; otherwise, set it to `False`.    
Default setting: `save_every_anime_in_a_separate_folder = False`

&nbsp;

## Advanced Settings

### Custom Blacklisted Phrases
Enter all phrases you want the downloaded filenames NOT to contain here. It works exactly like the "Must Not Contain:" field in qBittorrent, so look up its formatting rules in case you want to make use of this.    
Before you type something like "480p" in here, I would in general ***highly*** recommend filtering those things out within the RSS feed URL itself, not the RSS downloader configuration.    
Default setting: `custom_must_not_contain_values = ""`

### Use Shortened Anime Titles in RSS Search
Some anime titles are unnecessarily long, and it might be more reliable to shorten really long titles while searching through the RSS feed.    
This does not change the name of any files or folders and should only be set to `False` if the RSS downloader keeps downloading wrong shows with similar titles.    
Default setting: `use_shortened_anime_titles_in_RSS_match = True`

### Manual File Path to feeds.json
If you use, for example, a portable version of qBittorrent or have an unusual folder structure and this script can't find the `feeds.json` file on your PC, please enter the full file path below.     
It is usually located in the `C:\Users\YourUsername\AppData\Roaming\qBittorrent\rss` folder, and this program *should* be able to detect it, but there might be exceptions.    
Example setting: `manual_file_path_to_feeds_json = r"D:\Users\YourUsername\Documents\qBittorrent\config\rss\feeds.json"`    
Default setting: `manual_file_path_to_feeds_json = r""`

### Subgroup Search Dictionary
This dictionary makes finding subgroups more reliable by associating the subgroup with a search term. It also exists for visual reasons.    
You should not need to add extra subgroups to this as the script should generally find subgroups not included in this dictionary just fine, as long as you named your RSS feed correctly in qBittorrent.    
This can, however, help with subgroups that have weird naming schemes or trouble getting detected.    
NOTE: If you want to use subgroups shorter than three letters, you WILL have to add them to this dictionary. Consider using brackets as the search term and in your RSS feed name, like: `"[gg]": "[gg]",`.

### My RSS Feeds
I would recommend using the `feeds.json` method and leaving this variable untouched, but if the `feeds.json` method doesn't work, you can alternatively enter the RSS feeds you use below.    
They need to be the same links as in your qBittorrent, so if you use, for example, `"https://animetorrenttracker.com/?page=rss&q=RANDOM-SUBGROUP+1080&c=0_0&f=0"` as your RSS feed for RANDOM-SUBGROUP,    
then you need to enter the same exact link below, like `"[RANDOM-SUBGROUP]": "https://animetorrenttracker.com/?page=rss&q=RANDOM-SUBGROUP+1080&c=0_0&f=0"`.

&nbsp;

## F.A.Q.

### I successfully added the download rules to the RSS Downloader, but now qBittorrent shows a ton of notifications/errors about either merging trackers or duplicated torrents. How do I make them stop?
Wait for all the notifications to finish showing up once, then go to the RSS tab in qBittorrent with all your RSS feeds. Select the anime-related feeds (using shift or control to select multiple) and hit the "Mark items read" button at the top. This should stop the messages.

### If I doubleclick on the script it just opens it in a text editor instead of executing it, what do I do?
Create a new text file, write `py "Index's Anime RSS Feed Downloader Generator for qBittorrent v1.1.py"` in it (with the correct filename in case you use a different version), save it as `RSS Downloader Generator.bat`, and double-click that `.bat` file.
