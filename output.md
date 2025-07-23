
# API - Implement File Download Endpoint

**Story Points:** 5

---

## User Story
As an API consumer, I want to call a dedicated endpoint to download a file so that I can retrieve stored assets from the server.

## Acceptance Criteria
- Given a new GET endpoint is created, for example `/download/{file_id}` or `/download/{filename}`.
- When a GET request is made to the endpoint with a valid file identifier, then the server should respond with the file stream and a `200 OK` status.
- Given a successful file retrieval, the response headers must include `Content-Type` appropriate for the file and `Content-Disposition: attachment; filename="..."` to trigger a browser download.
- When a GET request is made for a file that does not exist, then the server must respond with a `404 Not Found` status code.
- Given the existing `/files/` upload endpoint requires a `token`, when a download request is made without a valid token, then the server should respond with a `401 Unauthorized` status code.
