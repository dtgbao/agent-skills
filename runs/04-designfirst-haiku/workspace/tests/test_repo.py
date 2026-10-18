from notes.repo import NoteRepo


def test_add_and_list(tmp_path):
    repo = NoteRepo(tmp_path / "n.json")
    repo.add("a", "b")
    assert [n.title for n in repo.all()] == ["a"]
