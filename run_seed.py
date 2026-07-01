import os
import django
import random
from datetime import datetime, timedelta

# Django एनवायरनमेंट सेटअप
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'darazs.settings')
django.setup()

from django.db import transaction
# सीधे आपके 'products' ऐप से मॉडल्स इम्पोर्ट कर रहे हैं
from products.models import Product, Category, Stock

def start_seeding():
    raw_products = [
        {"title": "Sony WH-1000XM4 Wireless Headphones", "cat": "Electronics", "sub": "Audio", "price": 19999, "brand": "Sony"},
        {"title": "Logitech G502 Hero Gaming Mouse", "cat": "Electronics", "sub": "Accessories", "price": 4500, "brand": "Logitech"},
        {"title": "Samsung Odyssey G7 32-inch Monitor", "cat": "Electronics", "sub": "Displays", "price": 42000, "brand": "Samsung"},
        {"title": "Anker PowerCore 20000mAh Power Bank", "cat": "Electronics", "sub": "Accessories", "price": 2999, "brand": "Anker"},
        {"title": "Apple AirPods Pro (2nd Generation)", "cat": "Electronics", "sub": "Audio", "price": 24900, "brand": "Apple"},
        {"title": "JBL Flip 6 Portable Bluetooth Speaker", "cat": "Electronics", "sub": "Audio", "price": 9999, "brand": "JBL"},
        {"title": "Crucial X8 1TB Portable External SSD", "cat": "Electronics", "sub": "Storage", "price": 8500, "brand": "Crucial"},
        {"title": "TP-Link Archer AX55 Wi-Fi 6 Router", "cat": "Electronics", "sub": "Networking", "price": 6200, "brand": "TP-Link"},
        {"title": "Razer BlackWidow V4 Mechanical Keyboard", "cat": "Electronics", "sub": "Accessories", "price": 12500, "brand": "Razer"},
        {"title": "Elgato Stream Deck MK.2 Studio Controller", "cat": "Electronics", "sub": "Accessories", "price": 14999, "brand": "Elgato"},
        {"title": "Bose QuietComfort Ultra Earbuds", "cat": "Electronics", "sub": "Audio", "price": 25900, "brand": "Bose"},
        {"title": "Seagate Backup Plus 2TB External HDD", "cat": "Electronics", "sub": "Storage", "price": 5499, "brand": "Seagate"},
        {"title": "ASUS RT-AX88U Pro Dual-Band Router", "cat": "Electronics", "sub": "Networking", "price": 21000, "brand": "ASUS"},
        {"title": "Corsair Vengeance LPX 16GB RAM DDR4", "cat": "Electronics", "sub": "Components", "price": 4200, "brand": "Corsair"},
        {"title": "HyperX QuadCast S RGB USB Microphone", "cat": "Electronics", "sub": "Audio", "price": 13499, "brand": "HyperX"},
        {"title": "Wacom Intuos Medium Graphics Tablet", "cat": "Electronics", "sub": "Accessories", "price": 16500, "brand": "Wacom"},
        {"title": "SanDisk Ultra 128GB MicroSDXC Card", "cat": "Electronics", "sub": "Storage", "price": 1199, "brand": "SanDisk"},
        {"title": "Logitech C920x Pro HD Webcam", "cat": "Electronics", "sub": "Accessories", "price": 7999, "brand": "Logitech"},
        {"title": "Audio-Technica ATH-M50x Headphones", "cat": "Electronics", "sub": "Audio", "price": 11800, "brand": "Audio-Technica"},
        {"title": "Sennheiser HD 599 Open Back Headphones", "cat": "Electronics", "sub": "Audio", "price": 10999, "brand": "Sennheiser"},
        {"title": "Prestige Iris Plus 750W Mixer Grinder", "cat": "Home & Kitchen", "sub": "Appliances", "price": 3499, "brand": "Prestige"},
        {"title": "Kent 16025 Electric Glass Kettle 1.7L", "cat": "Home & Kitchen", "sub": "Appliances", "price": 1699, "brand": "Kent"},
        {"title": "Philips Daily Collection Air Fryer", "cat": "Home & Kitchen", "sub": "Appliances", "price": 6800, "brand": "Philips"},
        {"title": "Sleepwell Ortho Comfort King Mattress", "cat": "Home & Kitchen", "sub": "Bedding", "price": 18500, "brand": "Sleepwell"},
        {"title": "Solimo Premium Almonds 500g Pack", "cat": "Home & Kitchen", "sub": "Pantry", "price": 450, "brand": "Solimo"},
        {"title": "Pigeon Polypropylene Compact Chopper", "cat": "Home & Kitchen", "sub": "Kitchen Tools", "price": 299, "brand": "Pigeon"},
        {"title": "Hawkins Contura Hard Anodized Cooker 3L", "cat": "Home & Kitchen", "sub": "Cookware", "price": 1850, "brand": "Hawkins"},
        {"title": "Solimo 3-Piece Non-Stick Pan", "cat": "Home & Kitchen", "sub": "Cookware", "price": 1499, "brand": "Solimo"},
        {"title": "Eureka Forbes Trendy Zip Vacuum Cleaner", "cat": "Home & Kitchen", "sub": "Appliances", "price": 4299, "brand": "Eureka Forbes"},
        {"title": "Milton Thermosteel Flip Top Flask 1L", "cat": "Home & Kitchen", "sub": "Kitchen Tools", "price": 999, "brand": "Milton"},
        {"title": "Borosil Vision Glass Set of 6", "cat": "Home & Kitchen", "sub": "Cookware", "price": 540, "brand": "Borosil"},
        {"title": "Cello Novelty Big Plastic Shoe Rack", "cat": "Home & Kitchen", "sub": "Furniture", "price": 2499, "brand": "Cello"},
        {"title": "Bombay Dyeing Pure Cotton Bedsheet", "cat": "Home & Kitchen", "sub": "Bedding", "price": 1299, "brand": "Bombay Dyeing"},
        {"title": "Kurl-On Pure Coir 4-inch Mattress", "cat": "Home & Kitchen", "sub": "Bedding", "price": 9500, "brand": "Kurl-On"},
        {"title": "Bajaj New Shakti Neo 15L Water Heater", "cat": "Home & Kitchen", "sub": "Appliances", "price": 5999, "brand": "Bajaj"},
        {"title": "Usha Fontana Lotus Ceiling Fan", "cat": "Home & Kitchen", "sub": "Appliances", "price": 7500, "brand": "Usha"},
        {"title": "Wipro 16A Smart Wi-Fi Plug", "cat": "Home & Kitchen", "sub": "Automation", "price": 999, "brand": "Wipro"},
        {"title": "Philips Smart Wi-Fi LED Bulb E27", "cat": "Home & Kitchen", "sub": "Automation", "price": 699, "brand": "Philips"},
        {"title": "Prestige Omega Deluxe Granite Tawa", "cat": "Home & Kitchen", "sub": "Cookware", "price": 1150, "brand": "Prestige"},
        {"title": "Godrej E-Laptop Safety Locker", "cat": "Home & Kitchen", "sub": "Furniture", "price": 7999, "brand": "Godrej"},
        {"title": "Levi's Men's 511 Slim Fit Jeans", "cat": "Fashion", "sub": "Men Clothing", "price": 2899, "brand": "Levi's"},
        {"title": "Adidas Men's Ultraboost Light Shoes", "cat": "Fashion", "sub": "Footwear", "price": 14999, "brand": "Adidas"},
        {"title": "Puma Classic Unisex Suede Sneakers", "cat": "Fashion", "sub": "Footwear", "price": 5500, "brand": "Puma"},
        {"title": "Nike Dry-Fit Training T-Shirt", "cat": "Fashion", "sub": "Men Clothing", "price": 1999, "brand": "Nike"},
        {"title": "Tommy Hilfiger Leather Men's Wallet", "cat": "Fashion", "sub": "Accessories", "price": 2499, "brand": "Tommy Hilfiger"},
        {"title": "Casio Enticer Men's Analog Watch", "cat": "Fashion", "sub": "Watches", "price": 3995, "brand": "Casio"},
        {"title": "Fossil Gen 6 Smartwatch", "cat": "Fashion", "sub": "Watches", "price": 18495, "brand": "Fossil"},
        {"title": "Ray-Ban Classic Aviator Sunglasses", "cat": "Fashion", "sub": "Accessories", "price": 8590, "brand": "Ray-Ban"},
        {"title": "Biba Women's Cotton Printed Kurta", "cat": "Fashion", "sub": "Women Clothing", "price": 1599, "brand": "Biba"},
        {"title": "Zara Oversized Trench Coat", "cat": "Fashion", "sub": "Women Clothing", "price": 7990, "brand": "Zara"},
        {"title": "American Tourister Hard Suitcase", "cat": "Fashion", "sub": "Bags & Luggage", "price": 4800, "brand": "American Tourister"},
        {"title": "Wildcraft 35L Casual Backpack", "cat": "Fashion", "sub": "Bags & Luggage", "price": 1699, "brand": "Wildcraft"},
        {"title": "Allen Solly Men's Formal Shirt", "cat": "Fashion", "sub": "Men Clothing", "price": 1499, "brand": "Allen Solly"},
        {"title": "United Colors of Benetton Sweatshirt", "cat": "Fashion", "sub": "Men Clothing", "price": 2299, "brand": "UCB"},
        {"title": "Crocs Unisex Classic Clogs", "cat": "Fashion", "sub": "Footwear", "price": 2995, "brand": "Crocs"},
        {"title": "Skechers Men's Go Walk Max Shoes", "cat": "Fashion", "sub": "Footwear", "price": 4200, "brand": "Skechers"},
        {"title": "Titan Neo Analog Dial Men's Watch", "cat": "Fashion", "sub": "Watches", "price": 5495, "brand": "Titan"},
        {"title": "Fastrack UV Protected Sunglasses", "cat": "Fashion", "sub": "Accessories", "price": 999, "brand": "Fastrack"},
        {"title": "Fabindia Silk Blend Straight Kurta", "cat": "Fashion", "sub": "Men Clothing", "price": 3299, "brand": "Fabindia"},
        {"title": "Skybags Trooper 55cm Cabin Luggage", "cat": "Fashion", "sub": "Bags & Luggage", "price": 2699, "brand": "Skybags"},
        {"title": "Philips OneBlade Hybrid Trimmer QP2520", "cat": "Beauty & Care", "sub": "Grooming Tools", "price": 1899, "brand": "Philips"},
        {"title": "L'Oreal Paris Total Repair Shampoo 1L", "cat": "Beauty & Care", "sub": "Hair Care", "price": 650, "brand": "L'Oreal"},
        {"title": "The Derma Co 10% Niacinamide Serum", "cat": "Beauty & Care", "sub": "Skin Care", "price": 549, "brand": "The Derma Co"},
        {"title": "Neutrogena Ultra Sheer Sunscreen", "cat": "Beauty & Care", "sub": "Skin Care", "price": 670, "brand": "Neutrogena"},
        {"title": "Nivea Soft Light Moisturizer Cream", "cat": "Beauty & Care", "sub": "Skin Care", "price": 399, "brand": "Nivea"},
        {"title": "Oral-B Pro 3 Electric Toothbrush", "cat": "Beauty & Care", "sub": "Grooming Tools", "price": 3850, "brand": "Oral-B"},
        {"title": "Cetaphil Gentle Skin Cleanser 250ml", "cat": "Beauty & Care", "sub": "Skin Care", "price": 575, "brand": "Cetaphil"},
        {"title": "Mamaearth Onion Hair Fall Control Oil", "cat": "Beauty & Care", "sub": "Hair Care", "price": 399, "brand": "Mamaearth"},
        {"title": "Beardo Hair Growth Oil for Men 50ml", "cat": "Beauty & Care", "sub": "Grooming Tools", "price": 450, "brand": "Beardo"},
        {"title": "Park Avenue Signature Collection Deo", "cat": "Beauty & Care", "sub": "Fragrances", "price": 250, "brand": "Park Avenue"},
        {"title": "Tresemme Keratin Smooth Conditioner", "cat": "Beauty & Care", "sub": "Hair Care", "price": 420, "brand": "Tresemme"},
        {"title": "Garnier Skin Naturals Micellar Water", "cat": "Beauty & Care", "sub": "Skin Care", "price": 349, "brand": "Garnier"},
        {"title": "Maybelline New York Colossal Mascara", "cat": "Beauty & Care", "sub": "Makeup", "price": 449, "brand": "Maybelline"},
        {"title": "Lakme Absolute Skin Gloss Gel Cream", "cat": "Beauty & Care", "sub": "Skin Care", "price": 750, "brand": "Lakme"},
        {"title": "Gillette Mach3 Turbo Blades 4-Pack", "cat": "Beauty & Care", "sub": "Grooming Tools", "price": 849, "brand": "Gillette"},
        {"title": "Khadi Natural Herbal Hair Cleanser", "cat": "Beauty & Care", "sub": "Hair Care", "price": 220, "brand": "Khadi Natural"},
        {"title": "Plum Green Tea Pore Cleansing Wash", "cat": "Beauty & Care", "sub": "Skin Care", "price": 345, "brand": "Plum"},
        {"title": "Minimalist 2% Salicylic Acid Serum", "cat": "Beauty & Care", "sub": "Skin Care", "price": 499, "brand": "Minimalist"},
        {"title": "The Body Shop British Rose Shower Gel", "cat": "Beauty & Care", "sub": "Fragrances", "price": 695, "brand": "The Body Shop"},
        {"title": "Dove Cream Beauty Bathing Bar Set", "cat": "Beauty & Care", "sub": "Skin Care", "price": 380, "brand": "Dove"},
        {"title": "Yonex Nanoray Light Badminton Racket", "cat": "Sports", "sub": "Badminton", "price": 2150, "brand": "Yonex"},
        {"title": "Nivia Storm Rubber Football Size 5", "cat": "Sports", "sub": "Football", "price": 499, "brand": "Nivia"},
        {"title": "Decathlon Quechua 10L Hiking Backpack", "cat": "Sports", "sub": "Outdoor Gym", "price": 499, "brand": "Decathlon"},
        {"title": "Kakfit Rubber Coated Dumbbells 5kg x2", "cat": "Sports", "sub": "Weights", "price": 1899, "brand": "Kakfit"},
        {"title": "Spalding NBA Replica Basketball", "cat": "Sports", "sub": "Basketball", "price": 1599, "brand": "Spalding"},
        {"title": "Cosco Light Cricket Tennis Ball Pack", "cat": "Sports", "sub": "Cricket", "price": 450, "brand": "Cosco"},
        {"title": "SG Scorer Classic Leather Cricket Ball", "cat": "Sports", "sub": "Cricket", "price": 380, "brand": "SG"},
        {"title": "Boldfit Yoga Mat Premium 6mm", "cat": "Sports", "sub": "Yoga", "price": 799, "brand": "Boldfit"},
        {"title": "Vector X Dynamic Skipping Rope", "cat": "Sports", "sub": "Yoga", "price": 199, "brand": "Vector X"},
        {"title": "Stiga Pro Carbon Table Tennis Racket", "cat": "Sports", "sub": "Indoor Sports", "price": 8500, "brand": "Stiga"},
        {"title": "Speedo Unisex Adult Swimming Goggles", "cat": "Sports", "sub": "Indoor Sports", "price": 999, "brand": "Speedo"},
        {"title": "MRF Genius Grand Edition Cricket Bat", "cat": "Sports", "sub": "Cricket", "price": 14500, "brand": "MRF"},
        {"title": "Strauss Fitness Exercise Wheel", "cat": "Sports", "sub": "Weights", "price": 449, "brand": "Strauss"},
        {"title": "Aurion Leatherman Gym Training Gloves", "cat": "Sports", "sub": "Weights", "price": 349, "brand": "Aurion"},
        {"title": "Nivia Orthopedic Ankle Support Brace", "cat": "Sports", "sub": "Outdoor Gym", "price": 280, "brand": "Nivia"},
        {"title": "ProsourceFit Multi-Grip Pull-Up Bar", "cat": "Sports", "sub": "Weights", "price": 2499, "brand": "ProsourceFit"},
        {"title": "Wilson US Open Tennis Ball Can of 3", "cat": "Sports", "sub": "Indoor Sports", "price": 550, "brand": "Wilson"},
        {"title": "Giono Mountain Terrain Bike 21-Speed", "cat": "Sports", "sub": "Outdoor Gym", "price": 16800, "brand": "Giono"},
        {"title": "Camelbak Eddy+ Water Bottle 750ml", "cat": "Sports", "sub": "Outdoor Gym", "price": 1499, "brand": "Camelbak"},
        {"title": "Fitbit Charge 6 Fitness Tracker Black", "cat": "Sports", "sub": "Outdoor Gym", "price": 13999, "brand": "Fitbit"}
    ]

    seller_names = ["CloudTail India", "RetailNet", "EOrison Store", "Daraz First", "SuperCom Retail"]
    chat_rates = ["95%", "89%", "92%", "78%", "Not enough data", "100%"]

    with transaction.atomic():
        for index, p_data in enumerate(raw_products, 1):
            parent_cat, _ = Category.objects.get_or_create(name=p_data["cat"], parent=None)
            sub_cat, _ = Category.objects.get_or_create(name=p_data["sub"], parent=parent_cat)
            curr_price = float(p_data["price"])
            on_sale = random.choice([True, False])
            orig_price = curr_price + random.randint(50, 1500) if on_sale else curr_price
            delivery_date = datetime.now() + timedelta(days=random.randint(2, 5))
            delivery_str = f"Guaranteed by {delivery_date.strftime('%d %b')}"

            product = Product.objects.create(
                category=sub_cat,
                title=p_data["title"],
                brand_name=p_data["brand"],
                image="products/sample_product.jpg",
                description=f"Premium quality {p_data['title']} brought to you by {p_data['brand']}.",
                current_price=curr_price,
                original_price=orig_price,
                is_on_sale=on_sale,
                answered_questions=random.randint(0, 45),
                delivery_charge=random.choice([0, 45, 60, 105]),
                delivery_days=delivery_str,
                cash_on_delivery=random.choice([True, False]),
                change_of_mind=random.choice([True, False]),
                return_days=random.choice([7, 14]),
                warranty_available=random.choice([True, False]),
                warranty_info=random.choice(["1 Year Brand Warranty", "Warranty not available"]),
                seller_name=random.choice(seller_names),
                positive_seller_ratings=random.randint(70, 99),
                ship_on_time=random.randint(85, 100),
                chat_response_rate=random.choice(chat_rates),
                item_form=random.choice(["Solid", "Liquid", "Device", "Apparel"])
            )

            Stock.objects.create(
                product=product,
                quantity=random.randint(0, 150),
                low_stock_alert=random.choice([3, 5, 10])
            )
            print(f"✅ Loaded: {index}/100")

    print("\n🎉 बधाई हो दीपक जी! सभी 100 प्रोडक्ट्स आपके SQLite डेटाबेस में सेट हो चुके हैं।")

if __name__ == '__main__':
    start_seeding()