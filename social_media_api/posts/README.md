## Follows & Feed

### Manage Follows
- `POST /api/accounts/follow/<user_id>/` — follow a user
- `POST /api/accounts/unfollow/<user_id>/` — unfollow a user
- `GET /api/accounts/following/` — list users I follow

### Feed
- `GET /api/feed/` — paginated list of posts by users I follow (newest first)

**Notes**
- You must be authenticated (Token) to follow/unfollow and view the feed: `Authorization: Token <token>`.
- Users cannot follow/unfollow themselves.
- The `User.following` M2M drives the feed.
