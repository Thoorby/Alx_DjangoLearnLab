\## Posts \& Comments API



\### Authentication

All write operations require token auth:

`Authorization: Token <token>`



\### Endpoints



\#### Posts

\- `GET /api/posts/` — list (paginated, supports `?search=<q>\&ordering=<field>`)

\- `POST /api/posts/` — create (auth required) `{ "title": "str", "content": "str" }`

\- `GET /api/posts/{id}/` — retrieve

\- `PATCH /api/posts/{id}/` — update (author only)

\- `DELETE /api/posts/{id}/` — delete (author only)



Search fields: `title`, `content`  

Ordering fields: `created\_at`, `updated\_at`, `title`  

Pagination: page size 10 (configure via DRF settings)



\#### Comments

\- `GET /api/comments/` — list (paginated; filter by post: `?post=<post\_id>`)

\- `POST /api/comments/` — create (auth required) `{ "post": <id>, "content": "str" }`

\- `GET /api/comments/{id}/` — retrieve

\- `PATCH /api/comments/{id}/` — update (author only)

\- `DELETE /api/comments/{id}/` — delete (author only)



Search fields: `content`  

Ordering fields: `created\_at`, `updated\_at`



\### Notes

\- Only owners can edit/delete their posts/comments (custom `IsOwnerOrReadOnly`).

\- Authors are set automatically from the authenticated user on create.



