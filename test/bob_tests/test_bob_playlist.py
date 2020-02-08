from songbird_server.resources.playlist import Playlist

data = [
    {"playlist": "https://open.spotify.com/playlist/5EF18jWof9VRYaC7ss3Wte"},
    {"playlist": "https://open.spotify.com/playlist/0RKi2UxVDVMrZqBA9uRSuT"},
    {"playlist": "https://open.spotify.com/playlist/5KMBhQon3ArWQe2vPzC8KW"},
]

def test_playlist_1():
    index = 1
    curr = Playlist()
    assert curr.get(index) == data[index-1]

def test_playlist_2():
    index = 2
    curr = Playlist()
    assert curr.get(index) == data[index-1]

def test_playlist_3():
    index = 3
    curr = Playlist()
    assert curr.get(index) == data[index-1]

def test_playlist_0():
    empty_dict = {"playlist": ""}
    index = 0
    curr = Playlist()
    assert curr.get(index) == empty_dict

def test_playlist_4():
    empty_dict = {"playlist": ""}
    index = 4
    curr = Playlist()
    assert curr.get(index) == empty_dict


