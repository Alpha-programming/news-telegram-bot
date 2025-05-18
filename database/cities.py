countries = {
    "Afghanistan": "AF", "Albania": "AL", "Algeria": "DZ","Argentina": "AR",
    "Armenia": "AM", "Australia": "AU", "Austria": "AT", "Azerbaijan": "AZ", "Bahrain": "BH",
    "Bangladesh": "BD", "Belarus": "BY", "Belgium": "BE", "Bhutan": "BT",
    "Brazil": "BR", "Brunei": "BN", "Bulgaria": "BG", "Cambodia": "KH", "Canada": "CA",
    "Chile": "CL", "China": "CN", "Colombia": "CO", "Croatia": "HR",
    "Czech Republic": "CZ", "Denmark": "DK", "Dominican Republic": "DO", "Ecuador": "EC", "Egypt": "EG",
    "Estonia": "EE", "Finland": "FI", "France": "FR", "Georgia": "GE", "Germany": "DE",
    "Greece": "GR", "Guatemala": "GT", "Hungary": "HU", "Iceland": "IS", "India": "IN",
    "Indonesia": "ID", "Iran": "IR", "Iraq": "IQ", "Ireland": "IE",
    "Italy": "IT", "Japan": "JP", "Jordan": "JO", "Kazakhstan": "KZ", "Kenya": "KE",
    "Kuwait": "KW", "Kyrgyzstan": "KG", "Lebanon": "LB",
    "Lithuania": "LT", "Malaysia": "MY", "Maldives": "MV", "Malta": "MT",
    "Mexico": "MX",  "Monaco": "MC", "Mongolia": "MN", "Montenegro": "ME",
    "Morocco": "MA", "Myanmar": "MM", "Nepal": "NP", "Netherlands": "NL", "New Zealand": "NZ", "North Macedonia": "MK", "Norway": "NO", "Oman": "OM", "Pakistan": "PK",
    "Palestine": "PS", "Panama": "PA", "Peru": "PE", "Philippines": "PH", "Poland": "PL",
    "Portugal": "PT", "Qatar": "QA", "Romania": "RO", "Russia": "RU", "Saudi Arabia": "SA",
    "Serbia": "RS", "Singapore": "SG", "Slovakia": "SK", "Slovenia": "SI", "South Korea": "KR",
    "Spain": "ES", "Sri Lanka": "LK", "Sweden": "SE", "Switzerland": "CH", "Syria": "SY",
    "Tajikistan": "TJ", "Thailand": "TH", "Tunisia": "TN", "Turkey": "TR", "Turkmenistan": "TM",
    "Ukraine": "UA", "United Arab Emirates": "AE", "United Kingdom": "GB", "United States": "US", "Uzbekistan": "UZ", "Vietnam": "VN", "Yemen": "YE"
}



import requests
def get_cities_for_country(country_code):
    username = "alpha_programming"
    url = f"http://api.geonames.org/searchJSON?country={country_code}&featureClass=P&maxRows=10&username={username}"

    response = requests.get(url)
    data = response.json()

    if "geonames" in data:
        cities = [city["name"] for city in data["geonames"]]

        return cities


    return []