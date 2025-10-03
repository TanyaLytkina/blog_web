from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from datetime import datetime
from fastapi.responses import RedirectResponse
from models import User, Post
from schemas import UserCreate, PostCreate

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Хранение пользователей и постов в памяти
users_db = {}
posts_db = {}
next_user_id = 1
next_post_id = 1

# Пользователи API
@app.post("/users/", response_model=dict)
async def create_user(user: UserCreate):
    global next_user_id
    new_user = User(id=next_user_id, **user.dict())
    users_db[next_user_id] = new_user
    next_user_id += 1
    return {
        "id": new_user.id,
        "email": new_user.email,
        "login": new_user.login,
        "createdAt": new_user.createdAt,
        "updatedAt": new_user.updatedAt
    }

@app.get("/users/", response_model=List[dict])
async def read_users():
    return [
        {
            "id": user.id,
            "email": user.email,
            "login": user.login,
            "createdAt": user.createdAt,
            "updatedAt": user.updatedAt
        }
        for user in users_db.values()
    ]

@app.get("/users/{user_id}", response_model=dict)
async def read_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "login": user.login,
        "createdAt": user.createdAt,
        "updatedAt": user.updatedAt
    }

@app.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: int, user_data: UserCreate):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.email = user_data.email
    user.login = user_data.login
    user.password = user_data.password
    user.updatedAt = datetime.now()
    
    return {
        "id": user.id,
        "email": user.email,
        "login": user.login,
        "createdAt": user.createdAt,
        "updatedAt": user.updatedAt
    }

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    return {"detail": "User deleted"}

# Посты API
@app.post("/posts/", response_model=dict)
async def create_post(post: PostCreate):
    global next_post_id
    new_post = Post(id=next_post_id, authorId=1, **post.dict())
    posts_db[next_post_id] = new_post
    next_post_id += 1
    return {
        "id": new_post.id,
        "authorId": new_post.authorId,
        "title": new_post.title,
        "content": new_post.content,
        "createdAt": new_post.createdAt,
        "updatedAt": new_post.updatedAt
    }

@app.get("/posts/", response_model=List[dict])
async def read_posts():
    return [
        {
            "id": post.id,
            "authorId": post.authorId,
            "title": post.title,
            "content": post.content,
            "createdAt": post.createdAt,
            "updatedAt": post.updatedAt
        }
        for post in posts_db.values()
    ]

@app.get("/posts/{post_id}", response_model=dict)
async def read_post(post_id: int):
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": post.id,
        "authorId": post.authorId,
        "title": post.title,
        "content": post.content,
        "createdAt": post.createdAt,
        "updatedAt": post.updatedAt
    }

@app.put("/posts/{post_id}", response_model=dict)
async def update_post(post_id: int, post_data: PostCreate):
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.title = post_data.title
    post.content = post_data.content
    post.updatedAt = datetime.now()
    
    return {
        "id": post.id,
        "authorId": post.authorId,
        "title": post.title,
        "content": post.content,
        "createdAt": post.createdAt,
        "updatedAt": post.updatedAt
    }

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    
    del posts_db[post_id]
    return {"detail": "Post deleted"}

# HTML-шаблоны
# HTML-шаблоны
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    posts_list = [
        {
            "id": post.id,
            "authorId": post.authorId,
            "title": post.title,
            "content": post.content,
            "createdAt": post.createdAt,
            "updatedAt": post.updatedAt
        }
        for post in posts_db.values()
    ]
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts_list})

@app.get("/post/{post_id}", response_class=HTMLResponse)  # Изменил с /posts/ на /post/
async def view_post(request: Request, post_id: int):
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_data = {
        "id": post.id,
        "authorId": post.authorId,
        "title": post.title,
        "content": post.content,
        "createdAt": post.createdAt,
        "updatedAt": post.updatedAt
    }
    return templates.TemplateResponse("post.html", {"request": request, "post": post_data})

@app.get("/create-post", response_class=HTMLResponse)  # Изменил с /posts/create на /create-post
async def create_post_page(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/create-post")  # Изменил с /posts/create на /create-post
async def create_post_action(request: Request):
    global next_post_id
    form_data = await request.form()
    title = form_data["title"]
    content = form_data["content"]
    
    new_post = Post(id=next_post_id, authorId=1, title=title, content=content)
    posts_db[next_post_id] = new_post
    next_post_id += 1
    
    return {"detail": "Post created"}

@app.post("/create-post")
async def create_post_action(request: Request):
    global next_post_id
    form_data = await request.form()
    title = form_data["title"]
    content = form_data["content"]
    
    new_post = Post(id=next_post_id, authorId=1, title=title, content=content)
    posts_db[next_post_id] = new_post
    next_post_id += 1
    
    return HTMLResponse("""
    <html>
        <body>
            <h2>Post created successfully!</h2>
            <a href="/">Back to posts</a>
            <script>
                setTimeout(() => { window.location.href = "/"; }, 2000);
            </script>
        </body>
    </html>
    """)
@app.post("/edit-post/{post_id}")
async def edit_post_action(request: Request, post_id: int):
    form_data = await request.form()
    
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    title = form_data["title"]
    content = form_data["content"]
    
    post.title = title
    post.content = content
    post.updatedAt = datetime.now()
    
    # Редирект на страницу поста вместо возврата JSON
    return RedirectResponse(url=f"/post/{post_id}", status_code=303)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)