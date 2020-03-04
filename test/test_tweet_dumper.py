from src.resources.tweet_dumper import TwitterDumper

def test_valid_user():
    dumper = TwitterDumper()
    assert dumper.valid_user("BarackObama") == True

def test_invalid_user():
    dumper = TwitterDumper()
    assert dumper.valid_user("asdfkjasdkfjsalkjfsd") == False

def test_get_new_tweets():
    dumper = TwitterDumper()
    tweets = dumper.get_next_tweets("BarackObama", count=10)
    assert len(tweets) == 10

def test_get_all_text():
    dumper = TwitterDumper()
    tweets = dumper.get_all_text("Lucas_Nestor")
    assert len(tweets) == 315
