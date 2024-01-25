# Music Link Converter

Music Link Converter is a Python project that allows you to convert music links between different platforms. Currently, it supports Spotify, Tidal, and YouTube.

## Installation

### Clone the repository
```
git clone https://github.com/bnjn/music-link-converter.git
```

### Navigate into the project directory
```
cd musiclinkconvert
```

### Install dependencies:


To install the project dependencies using pip, run the following command:
```
pip install -r requirements.txt
```
If using poety, run the following command:
```
poetry install
```

### Setup Environment Variables
Get API credentials for the platforms here:
- [Spotify](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- [Tidal](https://developer.tidal.com/documentation/api/api-quick-start) (Some results are rate limited due to licence holders)
- [YouTube](https://developers.google.com/youtube/registering_an_application) (May hit default quota)

Create a `.env` file in the root of the project directory using the template in `example.env`

Example:
```
SPOTIFY_CLIENT_ID='<spotify-id>'
SPOTIFY_SECRET='<spotify-secret>'
TIDAL_CLIENT_ID='<tidal-id>'
TIDAL_SECRET='<tidal-secret>'
YT_API_KEY='<youtube-api-key>'
```

## Usage (CLI)

### Search
This allows you to search for a song on a specific platform. You will be prompted to enter the platform (Spotify, Tidal, or YouTube) and the song/artist name.

Run the script with the --search or -s flag:
```
python musiclinkconvert.py --search
```
or
```
python musiclinkconvert.py -s
```
Example output:
```
python musiclinkconvert.py --search                                             
Which platform would you like to search on? Spotify (1), Tidal (2) or YouTube (3): 3
Enter song and/or artist name: badger badger badger
Found Badgers : animated music video : MrWeebl by Weebl's Stuff
Here is your youtube link: https://www.youtube.com/watch?v=EIyixC9NsLI
```

### Convert
This allows you to convert a music link from one platform to another. When the script is called with a music URL as the first arguement, it will prompt for the target platform to convert to. If the URL is invalid or a track is not found, the script will ask if you want to search for a track.

To use this function, run the script with a music URL as an argument:
```
python musiclinkconvert.py <music_url>
```
Where <music_url> is the URL of the song on the source platform.

Example output:
```
python musiclinkconvert.py https://tidal.com/browse/track/166824501
That is a tidal link for Pilling in My Head by Nina Kraviz
Convert to spotify (1) or youtube (2) link: 1
Here is your spotify link: https://open.spotify.com/track/3oPQtuNizGYAmzuxBvjQUa
```

## Modules
There are a variety of modules that can be used to create custom scripts. The documentation for these is still TODO.