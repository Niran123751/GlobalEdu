from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
async def get_country_outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != 200:
        return {"error": f"Could not fetch page for {country}"}

    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    markdown_outline = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])
        text = heading.get_text().strip()
        markdown_outline += f"{'#' * level} {text}\n\n"

    return {"country": country, "outline": markdown_outline}
