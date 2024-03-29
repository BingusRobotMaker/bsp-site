import mysql.connector
from fastapi import FastAPI, Form, Response
from jinja2 import Environment, FileSystemLoader

app = FastAPI()
env = Environment(loader=FileSystemLoader("templates"))

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bingus2010!",
    database="MySQL"
)

cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content TEXT
    )
""")

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
    # Insert a new page into the database with the provided `page_text`
    try:
        cursor.execute("INSERT INTO pages (content) VALUES (%s)", (page_text,))
        db.commit()
    except Exception as e:
        return {"message": str(e)}

    template = env.get_template("success.html")
    return Response(content=template.render(), media_type="text/html")

@app.get("/pages")
async def pages():
    # Retrieve all pages from the database
    cursor.execute("SELECT id, content FROM pages ORDER BY id DESC")
    pages = cursor.fetchall()

    template = env.get_template("pages.html")
    return Response(template.render(pages=pages), media_type="text/html")

@app.get("/custom-{page_id}")
async def custom_page(page_id: int):
    try:
        # Get the page content from the database
        cursor.execute("SELECT content FROM pages WHERE id = %s", (page_id,))
        content = cursor.fetchone()[0]
    except Exception as e:
        return {"message": str(e)}

    return Response(content=content + "<a href='/page-creator'>Back to Page Creator</a>", media_type="text/html")


@app.get("/adminpanel")
async def admin_panel():
    template = env.get_template("adminpanel.html")
    return Response(content=template.render(), media_type="text/html")

@app.post("/clear-database")
async def clear_database():
    try:
        cursor.execute("DELETE FROM pages")
        cursor.execute("ALTER TABLE pages AUTO_INCREMENT = 1")  # Reset auto-increment counter
        db.commit()
    except Exception as e:
        return {"message": str(e)}

    template = env.get_template("cleared.html")
    return Response(content=template.render(), media_type="text/html")
