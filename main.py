from aiohttp import web
import sqlite3 as sq3

db_conn = sq3.connect("thought_overflow.db")
db = db_conn.cursor()

async def group_add(request):
    data = await request.json()
    if 'name' not in data:
        return web.HTTPBadRequest("Missing name")
    lastid = db.execute("SELECT id FROM groups ORDER BY id DESC").fetchone()
    if lastid is None:
        lastid = 0 
    else:
        lastid = lastid[0]

    cat_id = 0
    if 'category' in data:
        cat_id = db.execute("SELECT id FROM categories WHERE name == ?", (data["category"],)).fetchone()
        if cat_id is None:
            cat_id = db.execute("SELECT id FROM categories ORDER BY id DESC").fetchone()[0] + 1
            db.execute("INSERT INTO categories VALUES (?, ?)", (cat_id, data['category']));
        else:
            cat_id = cat_id[0]
        
    db.execute("INSERT INTO groups VALUES (?, ?, ?, ?)", (lastid + 1, cat_id, data['name'], data.get('description', ''))) 
    db_conn.commit()
    return web.HTTPOk()

async def group_list(request):
    return web.json_response({
        "groups": [
            {
                "id": id,
                "name": name,
                "description": description,
                "category": db.execute("SELECT name FROM categories WHERE id == ?", (cat_id,)).fetchone()[0]
            } for (id, cat_id, name, description)
            in db.execute("SELECT * FROM groups").fetchall()
            ]
        })
    
async def group_get(request):
    data = await request.json()
    if 'name' not in data:
        return web.HTTPBadRequest("Missing name")
    gid = 0
    if 'category' in data:
        cid = db.execute("SELECT id FROM categories WHERE name == ?", (data["category"],)).fetchone()
        if cid is None:
            return web.HTTPNotFound()
        gid = db.execute("SELECT id, description, category_id FROM groups WHERE name == ? AND category_id == ?", (data["name"], cid[0])).fetchone()
    else:
        gid = db.execute("SELECT id, description, category_id FROM groups WHERE name == ?", (data["name"],)).fetchone()

    if gid is None:
        return web.HTTPNotFound()

    return web.json_response({
        "description": gid[1],
        "posts": [
            {
                "title": title,
                "text": text,
                "date": date,
                "comments": [
                    {
                        "text": comment_text,
                        "date": comment_date,
                    } for (comment_text, comment_date)
                    in db.execute("SELECT text, date FROM comments WHERE group_id == ? AND category_id == ? AND post_id == ?", (gid[0], gid[2], id)).fetchall()
                ]
            } for (id, title, text, date)
            in db.execute("SELECT id, title, text, date FROM posts WHERE group_id == ? AND category_id == ?", (gid[0], gid[2])).fetchall()
        ]})
    

app = web.Application()
app.add_routes([
    web.post('/api/group/add', group_add),
    web.get('/api/group/list', group_list),
    web.get('/api/group/get', group_get),
    ])

if __name__ == '__main__':
    tables = {
            'categories': ("id", "name"),
            'groups': ("id", "category_id", "name", "description"),
            'posts': ("id", "group_id", "category_id", "title", "text", "date"),
            'comments': ("id", "group_id", "category_id", "post_id", "text", "date"),
            }
    for name, columns in tables.items():
        db.execute("CREATE TABLE IF NOT EXISTS {}{}".format(name, str(columns).replace("'","")))
        if name == "categories" and db.execute("SELECT 1 FROM categories").fetchone() is None:
            db.execute("INSERT INTO categories VALUES (0, 'other')")
            db_conn.commit()
    web.run_app(app)
