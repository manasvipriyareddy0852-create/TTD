

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("📰 News Explorer")

countries = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

country = st.sidebar.selectbox(
    "Select Country",
    list(countries.keys())
)

category = st.sidebar.selectbox(
    "Select Category",
    [
        "general",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ]
)

keyword = st.sidebar.text_input(
    "Search Keyword",
    placeholder="AI, Cricket, Tesla..."
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=10
)

# -----------------------
# TITLE
# -----------------------
st.title("🌍 Advanced News Explorer")
st.markdown(
    "Get the latest headlines from around the world."
)

# -----------------------
# FETCH NEWS
# -----------------------
params = {
    "apiKey": API_KEY,
    "country": countries[country],
    "category": category,
    "pageSize": article_count
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:

    data = response.json()
    articles = data.get("articles", [])

    # Keyword Filter
    if keyword:
        articles = [
            article for article in articles
            if keyword.lower() in (
                (article.get("title") or "") +
                (article.get("description") or "")
            ).lower()
        ]

    st.success(f"Found {len(articles)} articles")

    if not articles:
        st.warning("No matching articles found.")

    for article in articles:

        with st.container():

            col1, col2 = st.columns([1, 2])

            with col1:
                if article.get("urlToImage"):
                    st.image(
                        article["urlToImage"],
                        use_container_width=True
                    )

            with col2:

                st.subheader(article.get("title", "No Title"))

                source = article.get("source", {}).get("name", "Unknown Source")
                published = article.get("publishedAt", "")

                try:
                    published = datetime.strptime(
                        published,
                        "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%d %b %Y %H:%M")
                except:
                    pass

                st.caption(f"📰 {source} | 📅 {published}")

                st.write(
                    article.get(
                        "description",
                        "No description available."
                    )
                )

                st.link_button(
                    "Read Full Article",
                    article["url"]
                )

            st.divider()

else:
    st.error(
        f"Error fetching news: {response.status_code}"
    )