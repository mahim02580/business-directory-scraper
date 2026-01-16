import time
import random
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

base_url = "https://www.bdbusinessdirectory.com"
endpoint = "/single-location/all-businesses-in-dhaka/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

page_num = 1
business_info_list = []
start_time = datetime.now()
print("Starting...")
while True:
    print(f"Scraping page number - {page_num}")
    page = requests.get(f"{base_url}{endpoint}", params={"page": page_num, "directory_type": "general"},
                        headers=headers)
    time.sleep(random.uniform(2, 5))  # A random delay to incorporate human-like behaviour

    soup = BeautifulSoup(page.text, "html.parser")

    cards_links_elements = soup.select(selector="h2.directorist-listing-title a")

    if not cards_links_elements:
        break  # Ends loop if there is no more business information cards on the page
    cards_links = [cards_links_element.get("href") for cards_links_element in cards_links_elements]

    for card_link in cards_links:
        business_details_page = requests.get(card_link, headers=headers)
        time.sleep(random.uniform(2, 5))  # A random delay to incorporate human-like behaviour

        business_details_soup = BeautifulSoup(business_details_page.text, "html.parser")

        title_tag = business_details_soup.find("h1", class_="directorist-listing-details__listing-title")
        title = title_tag.text.strip() if title_tag else "N/A"

        address_tag = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-address div.directorist-single-info__value")
        address = address_tag.text.strip() if address_tag else "N/A"

        phone_tag = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-phone div.directorist-single-info__value")
        # Data Cleaning
        phone = phone_tag.text.replace("-", "").strip().replace(" ", "") if phone_tag else "N/A"
        if phone != "N/A":
            if ":" in phone:
                phone = phone.split(",")[0].split(":")[1].strip()
            if "+88" not in phone:
                phone = "+88" + phone

        email_tag = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-email div.directorist-single-info__value")
        email = email_tag.text.strip() if email_tag else "N/A"

        website_tag = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-web div.directorist-single-info__value")
        website = website_tag.text.strip() if website_tag else "N/A"

        zipcode_tag = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-zip div.directorist-single-info__value")
        zipcode = zipcode_tag.text.strip() if zipcode_tag else "N/A"

        business_social_links = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-socials div.directorist-social-links")

        try:
            facebook_link = business_social_links.find(class_="facebook").get("href")
        except AttributeError:
            facebook_link = "N/A"
        try:
            instagram_link = business_social_links.find(class_="instagram").get("href")
        except AttributeError:
            instagram_link = "N/A"
        try:
            youtube_link = business_social_links.find(class_="youtube").get("href")
        except AttributeError:
            youtube_link = "N/A"
        try:
            linkedin_link = business_social_links.find(class_="linkedin").get("href")
        except AttributeError:
            linkedin_link = "N/A"

        business_info = {
            "Business Name": title,
            "Phone": phone,
            "Website": website,
            "Email": email,
            "Address": address,
            "Zip Code": zipcode,
            "Facebook": facebook_link,
            "Instagram": instagram_link,
            "Youtube": youtube_link,
            "LinkedIn": linkedin_link
        }
        business_info_list.append(business_info)

    page_num += 1

print("Scraping Ended!")

print("Exporting to excel...")
data_df = pd.DataFrame(business_info_list)
data_df.to_excel("data.xlsx", index=False)
print("Done! Check \"data.xlsx\"")

# Runtime Calculation
end_time = datetime.now()
diff = end_time - start_time
total_seconds = int(diff.total_seconds())
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
print(f"Time taken: {hours}h {minutes}m {seconds}s")
