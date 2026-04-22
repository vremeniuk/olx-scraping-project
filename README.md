# olx-scraping-project

## Overview
This project demonstrates web scraping using Selenium to collect real estate data from OLX.

The script extracts apartment listings from Kyiv, including both basic and detailed attributes.

---

## Data Collected
The following fields were extracted:

- Title
- Price
- Location
- City
- Link
- Area (m²)
- Floor
- Total Floors (if available)

---

## Approach

- Used Selenium to handle dynamic content loading on OLX
- Collected listing data from the catalog page
- Opened each listing in a new tab to extract additional attributes
- Parsed text content instead of relying on unstable HTML structure
- Cleaned numeric fields (price, area) for analysis
- Handled missing values where data was not available

---

## Technologies Used

- Python
- Selenium
- Pandas

---

## Output

The result is a structured dataset saved as: olx_data.csv


---

## Notes

- Some fields (e.g., total floors) may be missing depending on the listing
- The script currently scrapes a limited number of listings for demonstration purposes

---

## How to Run

1. Install dependencies: pip install -r requirements.txt

2. Run the script: python scraper.py


---

## Future Improvements

- Add pagination to collect more data
- Export data directly to Google Sheets
- Improve parsing accuracy for additional attributes

## Results

- Google Sheets: https://docs.google.com/spreadsheets/d/19-8VyEZadP7McRNK3XuH6Rb-43BrqjN7HFV47Z8Tmi8/edit?usp=sharing