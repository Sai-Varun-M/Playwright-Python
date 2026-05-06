"""
API Tests — REST API validation using Playwright's APIRequestContext.
Target:    https://jsonplaceholder.typicode.com
Run with:  pytest tests/api/ -m api
"""
import json
import pytest
from playwright.sync_api import APIRequestContext

from utils.test_data import SAMPLE_POST, SAMPLE_TODO
from utils.helpers   import assert_response_ok


@pytest.mark.api
class TestGetRequests:
    """GET endpoint tests."""

    def test_get_all_posts(self, api_request: APIRequestContext) -> None:
        """GET /posts should return 100 posts."""
        response = api_request.get("/posts")
        assert_response_ok(response.status, "/posts")
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 100

    def test_get_single_post(self, api_request: APIRequestContext) -> None:
        """GET /posts/1 should return a post with id=1."""
        response = api_request.get("/posts/1")
        assert_response_ok(response.status, "/posts/1")
        post = response.json()
        assert post["id"] == 1
        assert "title" in post
        assert "body" in post
        assert "userId" in post

    def test_get_all_users(self, api_request: APIRequestContext) -> None:
        """GET /users should return 10 users."""
        response = api_request.get("/users")
        assert_response_ok(response.status, "/users")
        users = response.json()
        assert len(users) == 10

    def test_get_user_by_id(self, api_request: APIRequestContext) -> None:
        """GET /users/1 should return user with id=1."""
        response = api_request.get("/users/1")
        assert_response_ok(response.status, "/users/1")
        user = response.json()
        assert user["id"] == 1
        assert "name" in user
        assert "email" in user

    def test_get_comments_for_post(self, api_request: APIRequestContext) -> None:
        """GET /posts/1/comments should return a list of comments."""
        response = api_request.get("/posts/1/comments")
        assert_response_ok(response.status)
        comments = response.json()
        assert isinstance(comments, list)
        assert len(comments) > 0
        assert "email" in comments[0]

    def test_get_todos(self, api_request: APIRequestContext) -> None:
        """GET /todos should return 200 items."""
        response = api_request.get("/todos")
        assert_response_ok(response.status)
        todos = response.json()
        assert len(todos) == 200

    def test_get_nonexistent_resource(self, api_request: APIRequestContext) -> None:
        """GET on a non-existent ID should return 404."""
        response = api_request.get("/posts/99999")
        assert response.status == 404


@pytest.mark.api
class TestPostRequests:
    """POST endpoint tests."""

    def test_create_post(self, api_request: APIRequestContext) -> None:
        """POST /posts should return 201 and echo the created resource."""
        response = api_request.post("/posts", data=json.dumps(SAMPLE_POST),
                                    headers={"Content-Type": "application/json"})
        assert response.status == 201
        created = response.json()
        assert created["title"] == SAMPLE_POST["title"]
        assert created["body"]  == SAMPLE_POST["body"]
        assert "id" in created

    def test_create_todo(self, api_request: APIRequestContext) -> None:
        """POST /todos should create a new todo."""
        response = api_request.post("/todos", data=json.dumps(SAMPLE_TODO),
                                    headers={"Content-Type": "application/json"})
        assert response.status == 201
        todo = response.json()
        assert todo["title"] == SAMPLE_TODO["title"]
        assert todo["completed"] is False


@pytest.mark.api
class TestPutRequests:
    """PUT endpoint tests."""

    def test_update_post(self, api_request: APIRequestContext) -> None:
        """PUT /posts/1 should update and return the modified resource."""
        updated = {**SAMPLE_POST, "id": 1, "title": "Updated Title"}
        response = api_request.put("/posts/1", data=json.dumps(updated),
                                   headers={"Content-Type": "application/json"})
        assert_response_ok(response.status)
        result = response.json()
        assert result["title"] == "Updated Title"
        assert result["id"] == 1


@pytest.mark.api
class TestDeleteRequests:
    """DELETE endpoint tests."""

    def test_delete_post(self, api_request: APIRequestContext) -> None:
        """DELETE /posts/1 should return 200 with empty body."""
        response = api_request.delete("/posts/1")
        assert_response_ok(response.status)
        body = response.json()
        # JSONPlaceholder returns {} on delete
        assert body == {}


@pytest.mark.api
class TestResponseHeaders:
    """HTTP header validation."""

    def test_content_type_json(self, api_request: APIRequestContext) -> None:
        """Response Content-Type should be application/json."""
        response = api_request.get("/posts/1")
        content_type = response.headers.get("content-type", "")
        assert "application/json" in content_type

    def test_response_time_acceptable(self, api_request: APIRequestContext) -> None:
        """Response should arrive within a reasonable time (10s budget)."""
        import time
        start = time.time()
        api_request.get("/posts")
        elapsed = time.time() - start
        assert elapsed < 10, f"Response took {elapsed:.2f}s — too slow"
