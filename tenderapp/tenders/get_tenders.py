import requests

url = "https://public.api.openprocurement.org/api/0/tenders?descending=1"
response = requests.get(url)
data = response.json()

tenders = data["data"]

for tender in tenders:
    tender_id = tender["id"]
    date_modified = tender["dateModified"]

    print("Tender ID:", tender_id)
    print("Date Modified:", date_modified)

    tender_url = f"https://public.api.openprocurement.org/api/0/tenders/{tender_id}"
    tender_response = requests.get(tender_url)
    tender_data = tender_response.json()

    if "description" in tender_data:
        description = tender_data["description"]
        print("Description:", description)

    print("-" * 30)
