from fastapi import FastAPI, Form, Response
from jinja2 import Environment, FileSystemLoader
import os

app = FastAPI()
env = Environment(loader=FileSystemLoader("templates"))

@app.get("/")
async def info():
    template = env.get_template("index.html")
    return Response(content=template.render(), media_type="text/html")

@app.get("/page-creator")
async def page_creator_form():
    template = env.get_template("page_creator.html")
    return Response(content=template.render(), media_type="text/html")

@app.post("/create-page")
async def create_page(page_text: str = Form(...)):
    # Get the number of pages
    pages = os.listdir("pages/")
    page_count = len(pages)

    # Create a new page with the provided `page_text`
    try:
        with open(f"pages/custom-{page_count}.html", "w") as f:
            f.write(f"<h1>{page_text}</h1>")
    except Exception as e:
        return {"message": str(e)}

    return Response("""<h1>Page creation success!!</h1>
    <a href='/page-creator'>Back to Page Creator</a>""",
    media_type="text/html")

@app.get("/count")
async def count():
    pages = os.listdir("pages/")
    page_count = len(pages)
    template = env.get_template("count.html")
    return Response(template.render(page_count=page_count), media_type="text/html")

@app.get("/custom-{page_id}")
async def custom_page(page_id: int):
    try:
        with open(f"pages/custom-{page_id}.html", "r") as f:
            content = f.read()
    except Exception as e:
        return {"message": str(e)}

    return Response(content=content + "<a href='/page-creator'>Back to Page Creator</a>", media_type="text/html")
