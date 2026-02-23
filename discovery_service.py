import random

class DiscoveryService:
    # Accurate Neighborhood-specific Data
    REAL_DATA = {
        "koramangala": [
            {
                "name": "Marcopolo Cafe", "type": "Italian & Continental", "price_per_person": 550, "rating": 4.4, 
                "photo": "https://images.unsplash.com/photo-1554118811-1e0d58224f24", "cake_price": 500, "offer": "Buy 2 Pizzas Get 1 Free",
                "timings": "11:00 AM - 11:00 PM", "best_time": "7:00 PM", "peak_hours": "8:00 PM - 10:00 PM", "crowd": "Moderate",
                "menu_highlights": ["Wood-fired Pizza", "Creamy Alfredo Pasta", "Tiramisu"]
            },
            {
                "name": "Bistro OUI", "type": "Italian & Chinese", "price_per_person": 600, "rating": 4.2, 
                "photo": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4", "cake_price": 600, "offer": "10% Student Discount",
                "timings": "12:00 PM - 10:30 PM", "best_time": "6:30 PM", "peak_hours": "7:30 PM - 9:30 PM", "crowd": "High",
                "menu_highlights": ["Dim Sum Platter", "Pesto Ravioli", "Choco Lava Cake"]
            },
            {
                "name": "Dome Cafe", "type": "Glass Domes / Rooftop", "price_per_person": 1000, "rating": 4.7, 
                "photo": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3", "cake_price": 800, "offer": "Decoration + 500g Cake included in special package",
                "timings": "4:00 PM - 1:00 AM", "best_time": "7:30 PM", "peak_hours": "8:00 PM - 11:00 PM", "crowd": "Exclusive (Booking Required)",
                "menu_highlights": ["Glass House Cocktail", "Exotic Mezze Platter", "Red Velvet Cheesecake"]
            },
            {
                "name": "DYU Art Cafe", "type": "Artistic Traditional", "price_per_person": 450, "rating": 4.5, 
                "photo": "https://images.unsplash.com/photo-1559339352-11d035aa65de", "cake_price": 400, "offer": "Free Brownie for Birthday Person",
                "timings": "10:00 AM - 10:30 PM", "best_time": "4:00 PM", "peak_hours": "12:00 PM - 2:00 PM", "crowd": "Peaceful",
                "menu_highlights": ["Banoffee Pie", "Cold Coffee", "Chicken Club Sandwich"]
            },
            {
                "name": "The Hole in the Wall", "type": "Brunch Spot", "price_per_person": 500, "rating": 4.3, 
                "photo": "https://images.unsplash.com/photo-1447078806655-40579c2520d6", "cake_price": 450, "offer": "Complimentary Breakfast Pancake",
                "timings": "8:00 AM - 9:00 PM", "best_time": "10:00 AM", "peak_hours": "9:00 AM - 12:00 PM", "crowd": "Very High",
                "menu_highlights": ["English Breakfast", "Waffles", "Blueberry Pancakes"]
            },
            {
                "name": "Truffles", "type": "American Burgers", "price_per_person": 400, "rating": 4.6, 
                "photo": "https://images.unsplash.com/photo-1550547660-d9450f859349", "cake_price": 500, "offer": "Custom Birthday Burger Platter",
                "timings": "11:30 AM - 10:30 PM", "best_time": "6:00 PM", "peak_hours": "1:00 PM - 3:00 PM", "crowd": "Massive",
                "menu_highlights": ["All American Burger", "Mississippi Mud Pie", "Chicken Wings"]
            },
            {
                "name": "Social Koramangala", "type": "Bar & Kitchen", "price_per_person": 800, "rating": 4.4, 
                "photo": "https://images.unsplash.com/photo-1538332576228-eb5b4c4de6ec", "cake_price": 600, "offer": "Free Shots for Groups",
                "timings": "9:00 AM - 12:30 AM", "best_time": "9:00 PM", "peak_hours": "10:00 PM - 12:00 AM", "crowd": "Party Animals",
                "menu_highlights": ["Social Platters", "Death Wings", "Butter Chicken Biryani"]
            },
            {
                "name": "Brooks and Bonds", "type": "Brewery", "price_per_person": 900, "rating": 4.1, 
                "photo": "https://images.unsplash.com/photo-1571613316887-6f8d5cbf7ef7", "cake_price": 700, "offer": "Unlimited Beer for 2 Hours",
                "timings": "12:00 PM - 12:00 AM", "best_time": "8:00 PM", "peak_hours": "9:00 PM - 11:30 PM", "crowd": "Corporate",
                "menu_highlights": ["Craft Beers", "Pepper Chicken", "Chilli Paneer"]
            }
        ],
        "indiranagar": [
            {
                "name": "Lazy Suzy", "type": "Deli & Cafe", "price_per_person": 700, "rating": 4.6, 
                "photo": "https://images.unsplash.com/photo-1559925393-8be0ec41b513", "cake_price": 750, "offer": "Custom Dessert Platter",
                "timings": "11:00 AM - 10:30 PM", "best_time": "5:00 PM", "peak_hours": "7:00 PM - 10:00 PM", "crowd": "Moderate",
                "menu_highlights": ["Suzy's Special Burger", "Quiche of the Day", "Macarons"]
            },
            {
                "name": "Araku Coffee", "type": "Specialty Coffee", "price_per_person": 800, "rating": 4.8, 
                "photo": "https://images.unsplash.com/photo-1502444330042-d1a1ddf9bb5c", "cake_price": 900, "offer": "Brewing Session for Groups",
                "timings": "8:30 AM - 10:00 PM", "best_time": "11:00 AM", "peak_hours": "4:00 PM - 7:00 PM", "crowd": "Sophisticated",
                "menu_highlights": ["Pour Over Coffee", "Nitro Brew", "Artisanal Breads"]
            },
            {
                "name": "Cafe Max", "type": "German & Rooftop", "price_per_person": 900, "rating": 4.5, 
                "photo": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30", "cake_price": 850, "offer": "German Beer Tasting",
                "timings": "12:00 PM - 11:30 PM", "best_time": "7:00 PM", "peak_hours": "8:30 PM - 10:30 PM", "crowd": "Lively",
                "menu_highlights": ["Schnitzel", "Sausage Platter", "Apple Strudel"]
            },
            {
                "name": "Little Italy", "type": "Fine Veg Italian", "price_per_person": 600, "rating": 4.2, 
                "photo": "https://images.unsplash.com/photo-1525610553991-2bede1a236e2", "cake_price": 550, "offer": "Authentic Tiramisu Free",
                "timings": "12:00 PM - 3:30 PM, 7:00 PM - 11:00 PM", "best_time": "8:00 PM", "peak_hours": "8:30 PM - 10:30 PM", "crowd": "Family Orientated",
                "menu_highlights": ["Lasagna Napoletana", "Nachos with Salsa", "Spaghetti Pasta"]
            },
            {
                "name": "Glen's Bakehouse", "type": "Bakery & Pizza", "price_per_person": 500, "rating": 4.3, 
                "photo": "https://images.unsplash.com/photo-1571115177098-24ec42ed2bb4", "cake_price": 400, "offer": "Free Cupcakes for Groups",
                "timings": "9:00 AM - 12:00 AM", "best_time": "8:00 PM", "peak_hours": "7:00 PM - 10:00 PM", "crowd": "High",
                "menu_highlights": ["Red Velvet Cupcake", "Thin Crust Pizza", "Hot Chocolate"]
            },
            {
                "name": "Windmills Craftworks", "type": "Premium Brewery & Jazz", "price_per_person": 1500, "rating": 4.7, 
                "photo": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1", "cake_price": 1000, "offer": "Dedicated Jazz Corner",
                "timings": "12:00 PM - 1:00 AM", "best_time": "8:30 PM", "peak_hours": "9:00 PM - 11:30 PM", "crowd": "Elite",
                "menu_highlights": ["Stout Beer", "Risotto", "Chocolate Mousse"]
            }
        ],
        "hsr layout": [
            {
                "name": "Cafe Here & Now", "type": "All Day Dining", "price_per_person": 550, "rating": 4.5, 
                "photo": "https://images.unsplash.com/photo-1516733725897-1aa73b87c8e8", "cake_price": 500, "offer": "Board Games + Free Fries",
                "timings": "11:00 AM - 11:00 PM", "best_time": "6:00 PM", "peak_hours": "7:00 PM - 9:30 PM", "crowd": "Student Friendly",
                "menu_highlights": ["Peri Peri Fries", "Loaded Nachos", "Oreo Shake"]
            },
            {
                "name": "The Pet People Cafe", "type": "Pet Friendly", "price_per_person": 700, "rating": 4.4, 
                "photo": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b", "cake_price": 600, "offer": "Free Treat for Your Pet",
                "timings": "10:00 AM - 9:30 PM", "best_time": "12:00 PM", "peak_hours": "1:00 PM - 3:00 PM", "crowd": "Animal Lovers",
                "menu_highlights": ["Healthy Bowls", "Smoothies", "Pet-friendly Cupcakes"]
            },
            {
                "name": "Shift Lounge", "type": "Pub & Bistro", "price_per_person": 900, "rating": 4.2, 
                "photo": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5", "cake_price": 700, "offer": "Happy Hour Prices on Parties",
                "timings": "12:00 PM - 12:00 AM", "best_time": "8:30 PM", "peak_hours": "9:00 PM - 11:30 PM", "crowd": "Party Vibes",
                "menu_highlights": ["Craft Beer", "Spicy Chicken Wings", "Cheese Platter"]
            },
            {
                "name": "Onion Knight Cafe", "type": "Quick Bites", "price_per_person": 350, "rating": 4.0, 
                "photo": "https://images.unsplash.com/photo-1559339352-11d035aa65de", "cake_price": 300, "offer": "Unlimited Chai for Groups",
                "timings": "11:00 AM - 10:00 PM", "best_time": "4:00 PM", "peak_hours": "5:00 PM - 7:00 PM", "crowd": "Cozy",
                "menu_highlights": ["Grilled Sandwich", "Masala Chai", "Momos"]
            }
        ],
        "default": [
            {
                "name": "Aromas Cafe", "type": "Global Cuisine", "price_per_person": 600, "rating": 4.3, 
                "photo": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3", "cake_price": 550, "offer": "Free Balloons & Cake",
                "timings": "11:00 AM - 11:00 PM", "best_time": "7:00 PM", "peak_hours": "8:00 PM - 10:00 PM", "crowd": "Professional",
                "menu_highlights": ["Mezze Platter", "Pasta Primavera", "Fruit Tart"]
            },
            {
                "name": "The Local Hub", "type": "Multi-cuisine", "price_per_person": 450, "rating": 4.1, 
                "photo": "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3", "cake_price": 400, "offer": "15% Group Discount",
                "timings": "11:30 AM - 10:30 PM", "best_time": "6:30 PM", "peak_hours": "7:30 PM - 9:30 PM", "crowd": "Casual",
                "menu_highlights": ["Burger Slider Platter", "Masala Fries", "Hot Chocolate"]
            },
            {
                "name": "Sky High", "type": "Rooftop Lounge", "price_per_person": 1000, "rating": 4.6, 
                "photo": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4", "cake_price": 900, "offer": "Live Music Request",
                "timings": "5:00 PM - 1:00 AM", "best_time": "7:00 PM", "peak_hours": "9:00 PM - 12:00 AM", "crowd": "Vibrant Rooftop",
                "menu_highlights": ["Cosmopolitan", "Grilled Prawns", "Blueberry Cheesecake"]
            },
            {
                "name": "Cafe Coffee Day", "type": "Coffee & Snacks", "price_per_person": 300, "rating": 3.9, 
                "photo": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085", "cake_price": 350, "offer": "Free Cake slice on app",
                "timings": "10:00 AM - 11:00 PM", "best_time": "5:00 PM", "peak_hours": "6:00 PM - 8:00 PM", "crowd": "High",
                "menu_highlights": ["Devil's Own", "Garlic Bread", "Samosa"]
            }
        ]
    }

    @staticmethod
    def get_nearby_plans(city, area, budget, needs):
        area_key = area.lower().strip()
        city_key = city.lower().strip()
        
        # Build a robust pool of venues (Area + City + Default)
        venue_pool = []
        if area_key in DiscoveryService.REAL_DATA:
            venue_pool.extend(DiscoveryService.REAL_DATA[area_key])
            
        # Also always add some defaults to ensure variety if area size is small
        venue_pool.extend(DiscoveryService.REAL_DATA["default"])
        
        # Add additional cities if needed
        venue_pool.extend(DiscoveryService.REAL_DATA.get("hsr layout", [])) # Mixing nearby areas
        
        # Deduplicate by name and shuffle
        unique_venues = {v['name']: v for v in venue_pool}.values()
        base_options = list(unique_venues)
        random.shuffle(base_options)

        plans = []
        needs_list = needs.split(',') if needs else []
        
        # User wants exactly 10 unique plans if possible
        num_plans = min(10, len(base_options))
        
        for i in range(num_plans):
            venue = base_options[i] # Each one is now unique
            
            # Simple simulation logic
            group_size = 10
            est_food = (venue['price_per_person'] * group_size) if 'food' in needs_list else 0
            est_cake = venue['cake_price'] if 'cake' in needs_list else 0
            est_decor = 1000 if 'decor' in needs_list else 0
            
            est_total = est_food + est_cake + est_decor + 500
            est_total *= (0.85 + random.random() * 0.3) # More realistic jitter (0.85 to 1.15)

            radius = round(0.5 + random.random() * 4.5, 1) # Random distance within 5KM
            map_search_query = f"{venue['name']} {area} {city}".replace(' ', '+')
            map_link = f"https://www.google.com/maps/search/{map_search_query}"

            plans.append({
                "id": i + 1,
                "title": f"Plan {i + 1}: {venue['name']}",
                "venue_name": venue['name'],
                "venue_type": venue['type'],
                "rating": venue['rating'],
                "distance": f"{radius} KM",
                "map_link": map_link,
                "photo": venue['photo'] + f"?auto=format&fit=crop&w=800&q=80&sig={random.randint(1,1000)}",
                "est_cost": round(est_total, 2),
                "offer": venue['offer'],
                "basic_price": venue['price_per_person'],
                "cake_price": venue['cake_price'],
                "timings": venue['timings'],
                "best_time": venue['best_time'],
                "peak_hours": venue['peak_hours'],
                "crowd": venue['crowd'],
                "menu_highlights": venue['menu_highlights'],
                "breakdown": {
                    "food": est_food,
                    "cake": est_cake,
                    "decor": est_decor,
                    "others": 500
                },
                "includes": [n.capitalize() for n in needs_list if n] or ["Venue Entry"]
            })
        
        return plans
