from google import genai
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    print("Please check your .env file.")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)


# Extract article text from URL
def get_article_text(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary elements
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):
            element.decompose()

        # Extract paragraphs
        paragraphs = soup.find_all("p")

        article_text = "\n".join(
            paragraph.get_text(" ", strip=True)
            for paragraph in paragraphs
        )

        return article_text

    except Exception as e:
        print("Error while fetching article:", e)
        return None


# Ask user for article URL
url = input("Enter the news article URL: ")

print("\nFetching article...")

article = get_article_text(url)

if article and article.strip():

    print("Article extracted successfully!")
    print("\nGenerating summary...\n")

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are a professional news summarizer.

Summarize the following news article into exactly 5
simple and clear bullet points.

Rules:
- Use only information from the article.
- Do not add outside information.
- Keep each bullet point short and easy to understand.

News article:

{article}
"""
        )

        print("================================")
        print("        NEWS SUMMARY")
        print("================================")
        print(response.text)

    except Exception as e:
        print("Error while generating summary:", e)

else:

    print("\nCould not extract the article.")
    print("Please check the URL and try again.")