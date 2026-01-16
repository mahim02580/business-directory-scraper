import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.bdbusinessdirectory.com"
endpoint = "/single-location/all-businesses-in-dhaka/"

page_num = 1
business_info_list = []
start_time = time.time()
while True:
    page = requests.get(f"{base_url}{endpoint}", params={"page": page_num, "directory_type": "general"})

    soup = BeautifulSoup(page.content, "html.parser")

    cards_links_elements = soup.select(selector="h2.directorist-listing-title a")
    if not cards_links_elements:
        break
    cards_links = [cards_links_element.get("href") for cards_links_element in cards_links_elements]

    for link in cards_links:
        business_details_page = requests.get(link)
        business_details_soup = BeautifulSoup(business_details_page.content, "html.parser")

        business_title = business_details_soup.find("h1", class_="directorist-listing-details__listing-title").text

        business_address = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-address div.directorist-single-info__value")
        address = business_address.text.strip() if business_address else "N/A"

        business_phone = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-phone div.directorist-single-info__value")
        phone = business_phone.text.replace("-", "").strip().replace(" ", "") if business_phone else "N/A"
        if phone != "N/A":
            if ":" in phone:
                phone = phone.split(",")[0].split(":")[1].strip()
            if "+88" not in phone:
                phone = "+88" + phone


        business_email = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-email div.directorist-single-info__value")
        email = business_email.text.strip() if business_email else "N/A"

        business_website = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-web div.directorist-single-info__value")
        website = business_website.text.strip() if business_website else "N/A"

        business_zip = business_details_soup.select_one(
            "div.directorist-single-info.directorist-single-info-zip div.directorist-single-info__value")
        zip = business_zip.text.strip() if business_zip else "N/A"

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
            "Business Name": business_title,
            "Phone": phone,
            "Website": website,
            "Email": email,
            "Address": address,
            "Zip Code": zip,
            "Facebook": facebook_link,
            "Instagram": instagram_link,
            "Youtube": youtube_link,
            "LinkedIn": linkedin_link
        }
        business_info_list.append(business_info)

    page_num += 1
    if page_num == 10:
        break

business_df = pd.DataFrame(business_info_list)
business_df.to_excel("sample_data.xlsx", index=False)


end_time = time.time()

diff_time = divmod((end_time - start_time), 60)
print(f"Time taken: {diff_time[0]}m {diff_time[1]}s")