from aiohttp import web
import sqlite3 as sq3

db_conn = sq3.connect("thought_overflow.db")
db = db_conn.cursor()

async def question_add(request):
    data = await request.post()
    if 'text' not in data:
        return web.HTTPBadRequest()
    lastid = db.execute(f"SELECT id FROM questions ORDER BY id DESC").fetchone()
    if lastid is None:
        lastid = 0 
    else:
        lastid = lastid[0]

    db.execute(f"INSERT INTO questions VALUES ({lastid + 1}, '{db_conn.escape_string(data['text'])}', 0, 0)") 
    db_conn.commit()
    return web.HTTPOk()

app = web.Application()
app.add_routes([
    web.post('/api/question/add', question_add),
    ])

if __name__ == '__main__':
    tables = {
            'questions': ("id", "text", "upvotes", "downvotes"),
            'answers': ("id", "question_id", "text", "upvotes", "downvotes"),
            'comments': ("id", "question_id", "answer_id", "upvotes", "downvotes"),
            }
    for name, columns in tables:
        if db.execute(f"SELECT name FROM sqlite_master WHERE name='{name}'").fetchone() is None;
            db.execute(f"CREATE TABLE {name}{str(columns).replace("'","")}")
    web.run_app(app)
