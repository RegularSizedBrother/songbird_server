from src.resources.bob.playlist import BobPlaylist

from mock import mock

data = [
        {"error": False, "playlist": "https://open.spotify.com/playlist/5EF18jWof9VRYaC7ss3Wte"},
        {"error": False, "playlist": "https://open.spotify.com/playlist/0RKi2UxVDVMrZqBA9uRSuT"},
        {"error": False, "playlist": "https://open.spotify.com/playlist/5KMBhQon3ArWQe2vPzC8KW"},
]

def test_playlist_1():
    with mock.patch('random.randint', return_value=1):
        index = 1
        curr = BobPlaylist()
        assert curr.get(index) == data[index-1]

def test_playlist_2():
    with mock.patch('random.randint', return_value=1):
        index = 2
        curr = BobPlaylist()
        assert curr.get(index) == data[index-1]

def test_playlist_3():
    with mock.patch('random.randint', return_value=1):
        index = 3
        curr = BobPlaylist()
        assert curr.get(index) == data[index-1]

def test_wait():
    with mock.patch('random.randint', return_value=0):
        index = 1
        curr = BobPlaylist()
        assert curr.get(index) == {"wait": True}

def test_error():
    with mock.patch('random.randint', return_value=1):
        index = 0
        curr = BobPlaylist()
        assert curr.get(index) == {"error": True}
