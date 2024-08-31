# StoryScraper

This project is an automated tool for downloading Instagram Stories from specified users without using Instagram's API or requiring login credentials. It utilizes a [third-party website](https://igram.world/story-saver) igram.com to fetch and download stories in full resolution.

## Features

- Download Instagram Stories from a list of usernames
- Schedule automatic downloads at specified intervals
- Web-based interface for easy management
- Organizes downloaded content by date and username
- Error handling and logging

## Project Structure

- `frontend.py`: Flask web application for the user interface
- `backend.py`: Core functionality for story downloading
- `usernames.txt`: List of Instagram usernames to monitor
- `index.html`: HTML template for the web interface

## Requirements

- Python 3.x
- Flask
- Playwright

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/patermars/StoryScraper.git
   cd StoryScraper
   ```

2. Install the required Python packages:
   ```
   pip install flask playwright
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

## Usage

1. Run the Flask application:
   ```
   python frontend.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload a list of usernames or add them manually through the web interface

4. Set the download interval (in hours)

5. Click "Start Download" to begin the automated process

## How It Works

This tool uses Playwright to automate browser interactions with a third-party website (igram.world) that allows downloading Instagram Stories without authentication. The process includes:

1. Navigating to the story downloader website
2. Entering usernames and initiating downloads
3. Saving downloaded content to date-organized folders

## Limitations

- Relies on a third-party website, which may change or become unavailable
- Does not use official Instagram API, which may affect reliability
- May not work if the target Instagram account is private

## Legal Disclaimer

This tool is for educational purposes only. Users are responsible for ensuring they have the right to download and use the content they access with this tool. Always respect copyright and Instagram's terms of service.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/patermars/StoryScraper/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
