# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes
from routes.categories import categories_routes
from routes.routes import routes_routes
from routes.courses import courses_routes
from routes.classes import classes_routes
from routes.comments import comments_routes
from routes.blogs import blogs_routes
from routes.forums import forums_routes
from routes.tutorials import tutorials_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.include_router(categories_routes, prefix='/categoria')
app.include_router(routes_routes, prefix='/rutas')
app.include_router(courses_routes, prefix='/cursos')
app.include_router(classes_routes, prefix='/clases')
app.include_router(comments_routes, prefix='/comentarios')
app.include_router(blogs_routes, prefix='/blogs')
app.include_router(forums_routes, prefix='/foros')
app.include_router(tutorials_routes, prefix='/tutoriales')


# Home
from home import HOME

@app.get(
    path="/",
    tags=["Home"]
)
def home():
    print(HOME)
    return {
        "Platzi": "Never stop learning, because life never stops teaching"
    }
