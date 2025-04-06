# Event Calendar Synchronizer

See public events from IEEE Colombia in: [**IEEE Colombia Events**](https://calendar.google.com/calendar/u/0/embed?src=c_43af0395e171c4997b9f25b43fa77a8e172f0405ed2fd325ded2462439218024@group.calendar.google.com&ctz=America/Bogota)

This project synchronizes events from the IEEE vTools API to a Google Calendar. It fetches events for a specific country (Colombia by default) and adds or updates them in a Google Calendar.

## Features

- Fetches events from the IEEE vTools API.
- Filters events by country.
- Synchronizes events with a Google Calendar:
  - Adds new events.
  - Updates existing events if they have changed.
  - Skips events that are already up-to-date.

## Requirements

- Python 3.7 or higher
- Google Calendar API credentials
- Internet connection

## Setup

### Docker quickstart

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set up Configuration**:
   * Copy `.env.example` to `.env` 
   * Update `.env` file with your data

3. **Build and run the Docker container**:
   ```bash
   docker build -t event-calendar-synchronizer .
   docker run -it --env-file=.env --rm event-calendar-synchronizer
   ```

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies**: Install the required Python packages using pip:
    ```bash
    pip -m venv .venv
    source ./.venv/bin/activate
    pip install -r requirements.txt
    ```
   
3. **Set up Configuration**:
   * Copy `.env.example` to `.env` 
   * Update `.env` file with your data

4. **Set up Google Calendar API credentials**: 
   * See [Python quickstart](https://developers.google.com/calendar/api/quickstart/python) to set up the Google Calendar API credentials.
   * Move the client secret JSON file to the project folder and rename it to `credentials.json`.

5. **Run the script**: The first time you run the script, it will prompt you to authenticate with your Google account. This will generate a `token.json` file for future use.
    ```bash
    python main.py
    ```
# How It Works
1. **Fetching Events**:
  * The script uses the IEEE vTools API to fetch a list of events.
  * Events are filtered by the country code (Example: Colombia code is CO).

2. **Event Synchronization**:
  * The script initializes the CalendarAPI class, which handles communication with the Google Calendar API.
  * For each event fetched from the vTools API:
    * If the event does not exist in the calendar, it is added.
    * If the event exists but has been updated, it is modified in the calendar.
    * If the event is already up-to-date, no changes are made.

3. **Statistics**:
  * At the end of the synchronization process, the script prints a summary of the number of events added, updated, and unchanged.

# Configuration
* **Google Calendar ID**: The Google Calendar ID can be changed in the `calendar_api.py` file. The default calendar is the primary calendar of the authenticated user. 
Replace this with the ID of the calendar you want to use. You can find the ID in the Google Calendar settings.
* **Country Code**: The country Code can be changed in the `.env` file. Use ISO 3166-1 alpha-2 standard


# File Structure
```plaintext
credentials.json       # Google API credentials
token.json             # Generated after authentication
lib/
    __init__.py        # Empty file for module initialization
    calendar_api.py    # Handles Google Calendar API interactions
    vtools_fetcher.py  # Fetches and processes events from the IEEE vTools API
main.py                # Entry point for the script
README.md              # Project documentation
```
