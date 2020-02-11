from src.resources.articles import MusicGenreQuerier
from collections import Counter



# big_5_profile: dictionary of string(personality dimension) => float(percentile, 0 to 1)
# max: whether to return the trait with the maximum percentile in the profile(true/false)
# num_max: number of maximum traits to return if max is True. Must be in the range [1,5]
# boundary: if max is false, returns all traits with percentile above boundary
# Returns a list P of up to 5 strings, where each string is a personality dimension.
#       If max is True, p is in P iff p has one of the num_max highest percentile of all the traits in big_5_profile
#       If max is False, p is in P iff p has a percentile in big_5_profile greater than or equal to boundary
def threshold(big_5_profile, max = False, num_max = 1, boundary = .75):
    if max:
        profile_counter = Counter(big_5_profile)
        max_mappings = profile_counter.most_common(num_max)
        traits = [mapping[0] for mapping in max_mappings]
    else:
        traits = [trait for trait in big_5_profile if big_5_profile[trait] >= boundary]
    return traits

#big_5_profile: dictionary of string(personality dimension) => float(percentile, 0 to 1)
#Returns list of Music Discovery genres/aspects from traits in big_5_profile
def get_genres_from_profile(big_5_profile):
    traits = threshold(big_5_profile, max=True)
    rename_traits = []
    for trait in traits:
        if trait == "Emotional Range":
            trait = "Neuroticism"
        rename_traits.append(trait)
    music_genres = MusicGenreQuerier()
    return music_genres.get_genres(traits)
if __name__ == "__main__":
    sample = {"Openness": .5, "Conscientiousness": .6, "Extraversion":.4, "Agreeableness":.7, "Emotional Range":.2}
    print(threshold(sample, max=True))
    print(get_genres_from_profile(sample))
