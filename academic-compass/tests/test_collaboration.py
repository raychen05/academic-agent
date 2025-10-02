import pytest
from tools.collaboration import CollaborationManager
import os

@pytest.fixture
def collab_manager(tmp_path):
    db_path = tmp_path / "comments.db"
    manager = CollaborationManager(str(db_path))
    yield manager
    manager.close()

def test_add_and_get_comments_by_paper(collab_manager):
    paper_id = "paper123"
    user_id = "userA"
    content = "This is a test annotation."

    comment_id = collab_manager.add_comment(paper_id, user_id, content)
    assert isinstance(comment_id, int)

    comments = collab_manager.get_comments_by_paper(paper_id)
    assert len(comments) == 1
    assert comments[0]["content"] == content
    assert comments[0]["paper_id"] == paper_id

def test_update_comment(collab_manager):
    paper_id = "paper123"
    user_id = "userA"
    content = "Original comment."
    comment_id = collab_manager.add_comment(paper_id, user_id, content)

    new_content = "Updated comment content."
    success = collab_manager.update_comment(comment_id, new_content)
    assert success

    comments = collab_manager.get_comments_by_paper(paper_id)
    assert comments[0]["content"] == new_content

def test_delete_comment(collab_manager):
    paper_id = "paper123"
    user_id = "userA"
    content = "Comment to delete."
    comment_id = collab_manager.add_comment(paper_id, user_id, content)

    success = collab_manager.delete_comment(comment_id)
    assert success

    comments = collab_manager.get_comments_by_paper(paper_id)
    assert len(comments) == 0

def test_get_comments_by_user(collab_manager):
    paper_id1 = "paper1"
    paper_id2 = "paper2"
    user_id = "userB"

    collab_manager.add_comment(paper_id1, user_id, "Comment 1")
    collab_manager.add_comment(paper_id2, user_id, "Comment 2")

    comments = collab_manager.get_comments_by_user(user_id)
    assert len(comments) == 2
    contents = [c["content"] for c in comments]
    assert "Comment 1" in contents
    assert "Comment 2" in contents