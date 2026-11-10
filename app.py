from flask import Flask, render_template, request, redirect, url_for
import requests
import os


# =========================================================
# FLASK APP
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)


# =========================================================
# PEXELS API KEY
# =========================================================
# IMPORTANT:
# Keep your EXISTING Pexels API key here.
# =========================================================

PEXELS_API_KEY = "JtxRVkDU9AITR2bfiGIMJ7C2WRUuCXEDTblxXxvV4XiN0YgySlFCkwGh"


# =========================================================
# HOME PAGE GIFTS - 16
# =========================================================

local_gifts = [

    {
        "name": "Smart Watch",
        "category": "watch",
        "price": "₹999",
        "image": "watch.jpg"
    },

    {
        "name": "Teddy Bear",
        "category": "teddy",
        "price": "₹499",
        "image": "teddy.jpg"
    },

    {
        "name": "Flowers",
        "category": "flowers",
        "price": "₹699",
        "image": "flowers.jpg"
    },

    {
        "name": "Jewellery",
        "category": "jewellery",
        "price": "₹1499",
        "image": "jewellery.jpg"
    },

    {
        "name": "Coffee Cup",
        "category": "cup",
        "price": "₹299",
        "image": "cup.jpg"
    },

    {
        "name": "Photo Frame",
        "category": "photo",
        "price": "₹399",
        "image": "photo.jpg"
    },

    {
        "name": "Shirt",
        "category": "shirt",
        "price": "₹799",
        "image": "shirt.jpg"
    },

    {
        "name": "Shoes",
        "category": "shoes",
        "price": "₹1299",
        "image": "shoes.jpg"
    },

    {
        "name": "Handbag",
        "category": "handbag",
        "price": "₹999",
        "image": "handbag.jpg"
    },

    {
        "name": "Headphones",
        "category": "headphones",
        "price": "₹1499",
        "image": "headphones.jpg"
    },

    {
        "name": "Sunglasses",
        "category": "sunglasses",
        "price": "₹799",
        "image": "sunglasses.jpg"
    },

    {
        "name": "Backpack",
        "category": "backpack",
        "price": "₹1299",
        "image": "backpack.jpg"
    },

    {
        "name": "Makeup Kit",
        "category": "makeup",
        "price": "₹999",
        "image": "makeup.jpg"
    },

    {
        "name": "Wallet",
        "category": "wallet",
        "price": "₹699",
        "image": "wallet.jpg"
    },

    {
        "name": "Perfume",
        "category": "perfume",
        "price": "₹1199",
        "image": "perfume.jpg"
    },

    {
        "name": "Phone Accessories",
        "category": "phone",
        "price": "₹499",
        "image": "phone.jpg"
    }
]


# =========================================================
# CATEGORY SEARCH QUERIES
# =========================================================

category_queries = {

    "teddy": "teddy bear plush toy",
    "watch": "wrist watch",
    "flowers": "flower bouquet",
    "jewellery": "jewellery product",
    "cup": "coffee mug",
    "photo": "photo frame",
    "shirt": "shirt clothing",
    "shoes": "shoes product",
    "handbag": "fashion handbag",
    "headphones": "headphones product",
    "sunglasses": "sunglasses product",
    "backpack": "backpack product",
    "makeup": "makeup cosmetics",
    "wallet": "wallet product",
    "perfume": "perfume bottle",
    "phone": "phone accessories"
}


# =========================================================
# WATCH CATEGORIES
# =========================================================

watch_categories = [

    {
        "name": "Silver Watch",
        "category": "silver",
        "image": "silver_watch.jpg",
        "price": "₹999"
    },

    {
        "name": "Smart Watch",
        "category": "smart",
        "image": "smart_watch.jpg",
        "price": "₹1299"
    },

    {
        "name": "Sports Watch",
        "category": "sports",
        "image": "sports_watch.jpg",
        "price": "₹1099"
    },

    {
        "name": "Steel Watch",
        "category": "steel",
        "image": "steel_watch.jpg",
        "price": "₹1499"
    },

    {
        "name": "Waterproof Watch",
        "category": "waterproof",
        "image": "waterproof_watch.jpg",
        "price": "₹1199"
    },

    {
        "name": "Designer Watch",
        "category": "designer",
        "image": "designer_watch.jpg",
        "price": "₹1599"
    }
]


# =========================================================
# WATCH PEXELS SEARCH QUERIES
# =========================================================

watch_queries = {

    "silver": "silver wrist watch",
    "smart": "smart watch",
    "sports": "sports wrist watch",
    "steel": "stainless steel wrist watch",
    "waterproof": "waterproof wrist watch",
    "designer": "designer luxury wrist watch"
}


# =========================================================
# DIFFERENT WATCH NAMES
# =========================================================

watch_names = [

    "Classic Wrist Watch",
    "Elegant Analog Watch",
    "Black Dial Watch",
    "Luxury Wrist Watch",
    "Digital Sports Watch",
    "Stylish Steel Watch",
    "Golden Wrist Watch",
    "Premium Leather Watch",
    "Modern Casual Watch",
    "Designer Wrist Watch",
    "Minimalist Watch",
    "Fashion Wrist Watch",
    "Classic Analog Watch",
    "Premium Smart Watch",
    "Elegant Fashion Watch",
    "Modern Dial Watch",
    "Stainless Steel Watch",
    "Sporty Digital Watch",
    "Luxury Analog Watch",
    "Stylish Casual Watch",
    "Premium Wrist Watch",
    "Modern Smart Watch",
    "Elegant Golden Watch",
    "Classic Leather Watch",
    "Trendy Wrist Watch",
    "Professional Watch",
    "Simple Analog Watch",
    "Premium Steel Watch",
    "Fashion Dial Watch",
    "Smart Digital Watch",
    "Elegant Black Watch",
    "Modern Luxury Watch",
    "Classic Fashion Watch",
    "Stylish Analog Watch",
    "Premium Designer Watch",
    "Sport Wrist Watch",
    "Everyday Wrist Watch",
    "Elegant Silver Watch",
    "Modern Steel Watch",
    "Luxury Fashion Watch"
]


# =========================================================
# PRICES
# =========================================================

prices = [

    499,
    599,
    699,
    799,
    899,
    999,
    1099,
    1199,
    1299,
    1499
]


# =========================================================
# GET PEXELS IMAGES
# =========================================================

def get_pexels_images(query, count=40):

    url = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization": "JtxRVkDU9AITR2bfiGIMJ7C2WRUuCXEDTblxXxvV4XiN0YgySlFCkwGh"
    }

    products = []

    used_images = set()

    page = 1

    while len(products) < count and page <= 5:

        params = {
            "query": query,
            "per_page": 40,
            "page": page
        }

        try:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=20
            )

            print(
                "API:",
                query,
                "PAGE:",
                page,
                "STATUS:",
                response.status_code
            )

            if response.status_code != 200:

                print(
                    "PEXELS ERROR:",
                    response.text
                )

                break

            data = response.json()

            photos = data.get(
                "photos",
                []
            )

            if not photos:

                print(
                    "NO PHOTOS FOUND FOR:",
                    query
                )

                break

            for photo in photos:

                if len(products) >= count:
                    break

                src = photo.get(
                    "src",
                    {}
                )

                image_url = (
                    src.get("large")
                    or src.get("medium")
                    or src.get("original")
                )

                if not image_url:
                    continue

                if image_url in used_images:
                    continue

                used_images.add(
                    image_url
                )

                if "watch" in query.lower():

                    product_name = watch_names[
                        len(products)
                        % len(watch_names)
                    ]

                else:

                    alt = photo.get(
                        "alt",
                        ""
                    ).strip()

                    if alt:

                        product_name = alt.title()

                    else:

                        product_name = (
                            query.title()
                            + " "
                            + str(
                                len(products) + 1
                            )
                        )

                products.append({

                    "name": product_name,

                    "price": "₹" + str(
                        prices[
                            len(products)
                            % len(prices)
                        ]
                    ),

                    "image": None,

                    "image_url": image_url
                })

            page += 1

        except requests.exceptions.RequestException as e:

            print(
                "PEXELS CONNECTION ERROR:",
                e
            )

            break

        except Exception as e:

            print(
                "PEXELS ERROR:",
                e
            )

            break

    print(
        "TOTAL IMAGES:",
        query,
        len(products)
    )

    return products


# =========================================================
# TEDDY BEAR IMAGES
# =========================================================

def get_teddy_images(count=40):

    url = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization":"JtxRVkDU9AITR2bfiGIMJ7C2WRUuCXEDTblxXxvV4XiN0YgySlFCkwGh"
    }

    teddy_queries = [

        "teddy bear plush toy",
        "cute teddy bear",
        "stuffed teddy bear",
        "brown teddy bear",
        "white teddy bear"
    ]

    products = []

    used_images = set()

    unwanted_words = [

        "person",
        "people",
        "man",
        "woman",
        "boy",
        "girl",
        "child",
        "children",
        "baby",
        "couple",
        "family",
        "crowd",
        "wedding"
    ]

    teddy_names = [

        "Cute Teddy Bear",
        "Soft Teddy Bear",
        "Brown Teddy Bear",
        "Plush Teddy Bear",
        "Lovely Teddy Bear",
        "White Teddy Bear",
        "Fluffy Teddy Bear",
        "Adorable Teddy Bear",
        "Classic Teddy Bear",
        "Sweet Teddy Bear"
    ]

    for query in teddy_queries:

        if len(products) >= count:
            break

        for page in range(1, 4):

            if len(products) >= count:
                break

            params = {

                "query": query,
                "per_page": 40,
                "page": page
            }

            try:

                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=20
                )

                print(
                    "TEDDY API:",
                    query,
                    "PAGE:",
                    page,
                    "STATUS:",
                    response.status_code
                )

                if response.status_code != 200:
                    continue

                data = response.json()

                photos = data.get(
                    "photos",
                    []
                )

                for photo in photos:

                    if len(products) >= count:
                        break

                    src = photo.get(
                        "src",
                        {}
                    )

                    image_url = (
                        src.get("large")
                        or src.get("medium")
                        or src.get("original")
                    )

                    alt = photo.get(
                        "alt",
                        ""
                    ).lower()

                    if not image_url:
                        continue

                    if image_url in used_images:
                        continue

                    if any(
                        word in alt
                        for word in unwanted_words
                    ):
                        continue

                    used_images.add(
                        image_url
                    )

                    product_name = teddy_names[
                        len(products)
                        % len(teddy_names)
                    ]

                    products.append({

                        "name": product_name,

                        "price": "₹" + str(
                            prices[
                                len(products)
                                % len(prices)
                            ]
                        ),

                        "image": None,

                        "image_url": image_url
                    })

            except Exception as e:

                print(
                    "TEDDY ERROR:",
                    e
                )

    print(
        "TOTAL TEDDY IMAGES:",
        len(products)
    )

    return products


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "login.html",
        gifts=local_gifts
    )


# =========================================================
# RECOMMENDATION PAGE
# =========================================================

@app.route("/recommendation")
def recommendation():

    return render_template(
        "recommendation.html"
    )


# =========================================================
# GIFT RECOMMENDATION
# =========================================================

@app.route("/gift", methods=["POST"])
def recommend_gift():

    relationship = request.form.get(
        "relationship",
        ""
    ).strip().lower()

    occasion = request.form.get(
        "occasion",
        ""
    ).strip().lower()

    budget = request.form.get(
        "budget",
        ""
    ).strip()


    # =====================================================
    # BUDGET RANGE
    # =====================================================

    if budget == "Below ₹500":

        min_price = 0
        max_price = 499

        api_prices = [
            199,
            249,
            299,
            349,
            399,
            449
        ]

    elif budget == "₹500 - ₹1000":

        min_price = 500
        max_price = 1000

        api_prices = [
            549,
            599,
            649,
            699,
            749,
            799,
            899,
            999
        ]

    elif budget == "₹1000 - ₹2000":

        min_price = 1000
        max_price = 2000

        api_prices = [
            1099,
            1199,
            1299,
            1399,
            1499,
            1699,
            1799,
            1999
        ]

    elif budget == "Above ₹2000":

        min_price = 2001
        max_price = 5000

        api_prices = [
            2199,
            2499,
            2799,
            2999,
            3499,
            3999,
            4499
        ]

    else:

        min_price = 0
        max_price = 5000

        api_prices = [
            499,
            699,
            999,
            1299,
            1499,
            1999
        ]


    # =====================================================
    # RELATIONSHIP BASED API SEARCHES
    # =====================================================

    recommendation_queries = {

        "father": [
            "gifts for father",
            "men wallet gift",
            "men watch gift",
            "men shirt gift",
            "men perfume gift",
            "sunglasses for men",
            "men shoes gift",
            "men backpack gift",
            "coffee mug gift"
        ],

        "mother": [
            "gifts for mother",
            "women handbag gift",
            "jewellery gift",
            "perfume for women",
            "flowers gift",
            "photo frame gift",
            "coffee mug gift",
            "women watch gift"
        ],

        "sister": [
            "gifts for sister",
            "women handbag",
            "jewellery gift",
            "makeup gift",
            "perfume for women",
            "fashion shoes",
            "teddy bear gift",
            "flowers gift",
            "women watch"
        ],

        "brother": [
            "gifts for brother",
            "men watch",
            "headphones gift",
            "wallet gift",
            "men shoes",
            "men shirt",
            "sunglasses for men",
            "backpack gift",
            "men perfume"
        ],

        "friend": [
            "gifts for friend",
            "gift box",
            "perfume gift",
            "watch gift",
            "headphones",
            "flowers gift",
            "teddy bear",
            "photo frame gift",
            "coffee mug gift"
        ],

        "wife": [
            "gifts for wife",
            "women jewellery",
            "handbag gift",
            "perfume for women",
            "flowers gift",
            "makeup gift",
            "fashion shoes",
            "watch for women",
            "teddy bear gift"
        ],

        "husband": [
            "gifts for husband",
            "men watch",
            "wallet gift",
            "men perfume",
            "men shirt",
            "men shoes",
            "sunglasses for men",
            "headphones",
            "backpack gift"
        ]
    }


    # =====================================================
    # OCCASION BASED SEARCH
    # =====================================================

    occasion_queries = {

        "birthday": "birthday gift",
        "anniversary": "anniversary gift",
        "wedding": "wedding gift",
        "festival": "festival gift"
    }


    queries = recommendation_queries.get(

        relationship,

        [
            "gift ideas",
            "birthday gifts",
            "gift products"
        ]
    )


    if occasion in occasion_queries:

        queries = (
            [occasion_queries[occasion]]
            + queries
        )


    # =====================================================
    # FETCH PEXELS API RECOMMENDATIONS
    # =====================================================

    api_recommendations = []

    used_images = set()


    for query in queries:

        if len(api_recommendations) >= 40:
            break

        products = get_pexels_images(
            query,
            5
        )

        for product in products:

            if len(api_recommendations) >= 40:
                break

            image_url = product.get(
                "image_url"
            )

            if not image_url:
                continue

            if image_url in used_images:
                continue

            used_images.add(
                image_url
            )

            api_recommendations.append(
                product
            )


    # =====================================================
    # APPLY SELECTED BUDGET TO API GIFTS
    # =====================================================

    for i, product in enumerate(
        api_recommendations
    ):

        product["price"] = (
            "₹"
            + str(
                api_prices[
                    i % len(api_prices)
                ]
            )
        )


    # =====================================================
    # LOCAL GIFT RELATIONSHIPS
    # =====================================================

    gift_rules = {

        "Smart Watch": [
            "friend",
            "brother",
            "sister",
            "father",
            "husband"
        ],

        "Teddy Bear": [
            "friend",
            "brother",
            "sister"
        ],

        "Flowers": [
            "friend",
            "mother",
            "wife",
            "husband",
            "sister"
        ],

        "Jewellery": [
            "sister",
            "mother",
            "wife"
        ],

        "Coffee Cup": [
            "friend",
            "brother",
            "sister",
            "mother",
            "father"
        ],

        "Photo Frame": [
            "friend",
            "brother",
            "sister",
            "mother",
            "father",
            "wife",
            "husband"
        ],

        "Shirt": [
            "friend",
            "brother",
            "father",
            "husband"
        ],

        "Shoes": [
            "friend",
            "brother",
            "sister",
            "father",
            "husband"
        ],

        "Handbag": [
            "sister",
            "mother",
            "wife"
        ],

        "Headphones": [
            "friend",
            "brother",
            "sister"
        ],

        "Sunglasses": [
            "friend",
            "brother",
            "sister",
            "father",
            "husband"
        ],

        "Backpack": [
            "friend",
            "brother",
            "sister"
        ],

        "Makeup Kit": [
            "sister",
            "mother",
            "wife"
        ],

        "Wallet": [
            "friend",
            "brother",
            "father",
            "husband"
        ],

        "Perfume": [
            "friend",
            "brother",
            "sister",
            "mother",
            "father",
            "wife",
            "husband"
        ],

        "Phone Accessories": [
            "friend",
            "brother",
            "sister"
        ]
    }


    # =====================================================
    # LOCAL RECOMMENDATIONS
    # =====================================================

    local_recommendations = []


    for gift in local_gifts:

        name = gift["name"]

        price = int(
            gift["price"].replace(
                "₹",
                ""
            )
        )


        if name not in gift_rules:
            continue


        if relationship not in gift_rules[name]:
            continue


        if not (
            min_price
            <= price
            <= max_price
        ):
            continue


        if name in [
            "Smart Watch",
            "Teddy Bear",
            "Coffee Cup",
            "Shirt",
            "Shoes",
            "Headphones",
            "Sunglasses",
            "Backpack",
            "Phone Accessories"
        ]:

            allowed_occasions = [
                "birthday",
                "festival"
            ]

        elif name in [
            "Jewellery",
            "Handbag",
            "Makeup Kit"
        ]:

            allowed_occasions = [
                "birthday",
                "anniversary",
                "wedding",
                "festival"
            ]

        else:

            allowed_occasions = [
                "birthday",
                "anniversary",
                "wedding",
                "festival"
            ]


        if occasion not in allowed_occasions:
            continue


        local_recommendations.append(
            gift
        )


    # =====================================================
    # COMBINE LOCAL + API GIFTS
    # =====================================================

    recommended = (
        local_recommendations
        + api_recommendations
    )


    if not recommended:
        recommended = api_recommendations


    # =====================================================
    # SHOW RESULTS
    # =====================================================

    return render_template(

        "gift_results.html",

        gifts=recommended,

        category="recommendation",

        title="Recommended Gifts",

        watch_categories=watch_categories
    )


# =========================================================
# WATCH CATEGORY
# =========================================================

@app.route("/category/watch")
def watch_category():

    products = get_pexels_images(
        "wrist watch",
        40
    )

    return render_template(

        "gift_results.html",

        gifts=products,

        category="watch",

        title="Watch Gifts",

        watch_categories=watch_categories
    )


# =========================================================
# OTHER CATEGORY PAGES
# =========================================================

@app.route("/category/<category>")
def category(category):

    if category not in category_queries:

        return redirect(
            url_for("home")
        )


    if category == "teddy":

        products = get_teddy_images(
            40
        )

        title = "Teddy Gifts"


    elif category == "watch":

        products = get_pexels_images(
            "wrist watch",
            40
        )

        title = "Watch Gifts"


    else:

        query = category_queries[
            category
        ]

        products = get_pexels_images(
            query,
            40
        )

        title = (
            category
            .replace("_", " ")
            .title()
            + " Gifts"
        )


    return render_template(

        "gift_results.html",

        gifts=products,

        category=category,

        title=title,

        watch_categories=watch_categories
    )


# =========================================================
# WATCH SUB-CATEGORY
# =========================================================

@app.route("/watch/<subcategory>")
def watch_subcategory(subcategory):

    if subcategory not in watch_queries:

        return redirect(
            url_for("watch_category")
        )


    query = watch_queries[
        subcategory
    ]

    products = get_pexels_images(
        query,
        40
    )


    selected_watch = None


    for watch in watch_categories:

        if watch["category"] == subcategory:

            selected_watch = watch

            break


    if selected_watch:

        title = selected_watch[
            "name"
        ]

    else:

        title = (
            subcategory.title()
            + " Watch"
        )


    return render_template(

        "gift_results.html",

        gifts=products,

        category="watch",

        title=title,

        watch_categories=watch_categories
    )


# =========================================================
# SEARCH
# =========================================================

@app.route("/search")
def search():

    query = request.args.get(
        "query",
        ""
    ).strip()


    if not query:

        return redirect(
            url_for("home")
        )


    products = get_pexels_images(
        query,
        40
    )


    return render_template(

        "gift_results.html",

        gifts=products,

        category="search",

        title="Search Results",

        watch_categories=watch_categories
    )


# =========================================================
# NEW: PEXELS GIFT DETAILS
# =========================================================
# This is the ONLY NEW FUNCTIONALITY.
# It receives the clicked Pexels gift's
# name, price and image URL.
# =========================================================

@app.route("/product")
def product_details():

    name = request.args.get(
        "name",
        "Gift"
    )

    price = request.args.get(
        "price",
        "₹499"
    )

    image = request.args.get(
        "image",
        ""
    )

    gift = {

        "name": name,

        "price": price,

        "image": None,

        "image_url": image
    }

    return render_template(

        "gift_details.html",

        gift=gift
    )


# =========================================================
# EXISTING HOME GIFT DETAILS
# =========================================================

@app.route("/gift/<int:index>")
def gift_details(index):

    if (
        index < 0
        or index >= len(local_gifts)
    ):

        return redirect(
            url_for("home")
        )


    gift = local_gifts[index]


    return render_template(

        "gift_details.html",

        gift=gift
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact")
def contact():

    return render_template(
        "contact.html"
    )


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )