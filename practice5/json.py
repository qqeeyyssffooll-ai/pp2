import re
import json


with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

clean_text = text.replace("\n", " ")

prices = re.findall(r"\d[\d\s]*,\d{2}", clean_text)
# Convert price to numbers
price_values = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

# 4. Find product names

products = re.findall(r"\d+\.\s*([^\d]+?)(?=\d+\.|$)", text)
products = [p.strip() for p in products]  

#  Calculate the total 
total = sum(price_values)

# 6. Find date and time in the format dd.mm.yyyy hh:mm:ss
datetime_match = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)


payment_match = re.search(r"(Банковская карта|Наличные)", text)

# 8. Create a dictionary of products with their corresponding prices
data = {
    "products": [
        {"name": name, "price": price_values[i] if i < len(price_values) else None} 
        for i, name in enumerate(products)
    ],
    "total_calculated": total,
    "date_time": datetime_match.group() if datetime_match else None,
    "payment_method": payment_match.group() if payment_match else None
}

# 9. Print the dictionary as formatted JSON
print(json.dumps(data, indent=4, ensure_ascii=False))
