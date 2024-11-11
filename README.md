# Tou.TV Downloader
### Allows you to search and download content from Tou.TV.


## Usage: `toutv.py` [help] connect, search, list, info, download [download options]

## Ways to Represent Seasons and Episodes:
- `download stat s01e01`
- `download "stat/S01E01"` (NOT WORKING)
- `download "temps de chien"` (Downloads entire series)
- `download "temps de chien" s01e01-s01e04` (Downloads all episodes from S1E1 to S1E4)
- `download "temps de chien" s01` (Downloads entire season)
- `download "temps de chien" s1-s3` (Downloads all episodes from season 1 to 3)
- `download "temps de chien" s1-s3e2` (Downloads all episodes from season 1 to season 3 episode 2)
- `download "stat e01"` (Downloads all episode 1 in a series) (NOT WORKING)

## Positional Arguments:
- **help**
  Show this help message and exit

- **connect**  
  Connect using your Tou.tv credentials (You need to enter your credentials in the `settings.json` file)
  
- **search**  
  Search for a show using its name (e.g., `search temps de chien`). This will give back a list of shows that match the pattern (e.g., `search "temps de chien"`)

- **list**  
  Lists all the episodes available for a show using its name or its "url name" (e.g., `list chien` OR `list temps-de-chien`)

- **info**  
  Gives all the information about a show using its name or its "url name" (e.g., `info temps de chien`)

- **download**  
  Download a show using its name or its "url name" (See the representation of the download commands)

## Download Options:
- `-r`  **Resolution** (e.g., `-r 1080` or `-r 720`)
- `-q`  **Quiet mode** (Don't display output in the terminal about what the program is doing.)
- `-ad` **Audiodescription** (Also downloads the audiodescription audio tracks)
- `-l`  **Latest Episode** (Downloads the latest episode that was available)
- `-s`  **Subtitles** (Doesn't seem to be working right now, unsure why)