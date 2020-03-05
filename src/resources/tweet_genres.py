from src.resources.articles import MusicGenreQuerier
from collections import Counter



# big_5_profile: dictionary of string(personality dimension) => float(percentile, 0 to 1)
# max: whether to return the trait with the maximum percentile in the profile(true/false)
# num_max: number of maximum traits to return if max is True. Must be in the range [1,5]
# boundary: if max is false, returns all traits with percentile above boundary
# Returns a dictionary of traits sorted by positive/negative correlations
#       If max is True, trait returned has one of the num_max highest percentile of all the traits in big_5_profile
#       If max is False, a trait is included if it differs from the mean percentile of all traits by at least one standard deviation
def threshold(big_5_profile, max = False, num_max = 1, boundary = .75):
    if max:
        profile_counter = Counter(big_5_profile)
        max_mappings = profile_counter.most_common(num_max)
        traits = [mapping[0] for mapping in max_mappings]
    #else:
    #    traits = [trait for trait in big_5_profile if big_5_profile[trait] >= boundary]
    #return traits
    else:
        mean = 0
        vals = []
        for trait in big_5_profile:
            mean = mean + big_5_profile[trait]
            vals.append(big_5_profile[trait])
        mean = mean/5.0
        std_dev = 0
        for val in vals:
            new_val = val - mean
            new_val = new_val * new_val
            std_dev = std_dev + new_val
        std_dev = std_dev/4.0
        traits = {}
        traits["pos"] = []
        traits["neg"] = []
        for trait in big_5_profile:
            if big_5_profile[trait] >= mean+std_dev:
                traits["pos"].append(trait)
            elif big_5_profile[trait] <= mean-std_dev:
                traits["neg"].append(trait)
        return traits



#big_5_profile: dictionary of string(personality dimension) => float(percentile, 0 to 1)
#Returns dictionary with keys "pos" and "neg" to list entries of personality traits
def get_genres_from_profile(big_5_profile):
    traits = threshold(big_5_profile, max=False)
    rename_traits = {}
    rename_traits["pos"] = []
    rename_traits["neg"] = []
    for trait in traits["pos"]:
        if trait == "Emotional Range":
           trait = "Neuroticism"
        rename_traits["pos"].append(trait)
    for trait in traits["neg"]:
        if trait == "Emotional Range":
           trait = "Neuroticism"
        rename_traits["neg"].append(trait)
    music_genres = MusicGenreQuerier()
    return music_genres.get_genres(traits, dummy=False)
if __name__ == "__main__":
    sample = {"Openness": .5, "Conscientiousness": .6, "Extraversion":.4, "Agreeableness":.7, "Emotional Range":.2}
    print(threshold(sample, max=True))
    print(get_genres_from_profile(sample))
