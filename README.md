# Aptiv Connected Services Hack Yeah 2023 Backend

## Endpoints:

### POST /api/group/add

REQ JSON:
    - name (required)
    - category (optional) [default: "other"]

RESP 200: OK
RESP 400: Bad JSON

### GET /api/group/list

RESP JSON:
    - groups: list of:
        - name (string)
        - description (string)
        - category (string)

### GET /api/group/get

REQ JSON:
    - name (required)
    - category (required)

RESP JSON:
    - description (string)
    - posts: list of:
        - id (int)
        - title (string)
        - text (string)
        - date (string)
        - comments: list of:
            - text (string)
            - date (string)

RESP 400: Bad JSON
RESP 404: Group or category not found

### POST /api/post/add

REQ JSON:
    - group (required)
    - category (required)
    - title (required)
    - text (required)

RESP JSON:
    - id (int)

RESP 400: Bad JSON
RESP 404: Group or category not found

### POST /api/comment/add

REQ JSON:
    - group (required)
    - category (required)
    - post_id (required)
    - text (required)

RESP 200: OK
RESP 400: Bad JSON
RESP 404: Group or category or post_id not found
