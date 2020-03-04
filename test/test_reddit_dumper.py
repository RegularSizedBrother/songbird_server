from src.resources.reddit_dumper import RedditDumper

def test_valid_user():
    dumper = RedditDumper()
    assert dumper.valid_user("thisisbillgates") == True

def test_invalid_user():
    dumper = RedditDumper()
    assert dumper.valid_user("asdfkjaskldfjalskdjfasd") == False

def test_get_all_posts():
    dumper = RedditDumper()
    text = dumper.get_all_text("PresidentObama")
    assert len(text) == 13
