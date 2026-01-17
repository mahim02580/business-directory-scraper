# BD Business Directory Scraper


A **polite, rate-limited Python web scraper** that collects publicly available business information from **bdbusinessdirectory.com** for a particular city (Dhaka listings) and exports the data to an Excel file.

This project is designed with **ethical scraping practices** in mind:
- Respects public access only
- Uses realistic headers
- Applies randomized delays
- Includes basic anti-bot awareness
- Avoids aggressive crawling

---

## ✨ Features

- Scrapes business listings from Dhaka, Bangladesh
- Handles pagination
- Extracts fields:
  - Business name
  - Phone number (cleaned & normalized)
  - Email
  - Website
  - Address
  - ZIP code
  - Social media links (Facebook, Instagram, YouTube, LinkedIn)
- Human-like randomized request delays (rate limiting)
- Realistic browser headers
- Graceful handling of missing data
- Runtime tracking
- Exports results to **Excel (.xlsx)**

---

## 🛠️ Tech Stack

- Python 3
- requests
- BeautifulSoup (bs4)
- pandas

---

## 📂 Output

The scraper generates:

```
data.xlsx
```

Each row represents one business listing. Check `sample_data.xlsx`

---

## ▶️ How It Works

1. Fetches paginated business listing pages
2. Extracts individual business detail URLs
3. Visits each business page
4. Parses structured business information
5. Stores data in memory
6. Exports all results to an Excel file
7. Prints total runtime

---

## ⏱️ Rate Limiting & Anti-Bot Considerations

This scraper is intentionally **slow and respectful**:

- Random delay of **2–5 seconds** between requests
- No concurrency or threading
- Public pages only
- Stops automatically when no listings are found

⚠️ If the website introduces CAPTCHA or bot-protection pages, the scraper should be stopped and reviewed.

---

## 🚀 Usage

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the script

```bash
python main.py
```

### 3️⃣ Check output

```text
data.xlsx
```

---

## 🧪 Configuration

You can adjust:

- **Delay range** (`random.uniform(2, 5)`)
- **Target location** by changing the endpoint

```python
endpoint = "/single-location/all-businesses-in-dhaka/"
```

---

## 📏 Runtime Tracking

The script measures total execution time:

```
Time taken: Xh Ym Zs
```

This is useful for performance monitoring and scaling decisions.