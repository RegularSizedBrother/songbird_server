# Environment name: Personality Recommendation Environment
# Music collection name: Music Personality
# Music configuration name: Music Personality Configuration xn4povqm3l
# Music configuration ID: d8389d37-9f3d-4012-b0d1-0b7bf4fb606f
# Knowledge Studio custom model ID 1: 492dc2fa-b316-4261-a334-0a22d1cb3e01
# Knowledge Studio custom model ID 2: 3a529978-d785-4895-935b-43d467a57524

import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#A personality dimension is its name(string), variations of its name(alternate_names, list of string),
#genres it's positively correlated with(set of string), and genres it's negatively correlated with(set of string)
class PersonalityDimension:
    def __init__(self, name, alternate_names=[]):
        self.standard_name = name
        self.alternate_names = alternate_names
        self.pos_correlation_genres = set()
        self.neg_correlation_genres = set()

#A MusicGenreRecommender sets up a connection to the custom Discovery music model
# Its get_genres method can take lists of personality traits and return lists of the types of music
# the traits are positively or negatively correlated with
class MusicGenreQuerier:
    def __init__(self):
        self.pos_relation_name = "PositiveCorrelation"
        self.neg_relation_name = "NegativeCorrelation"

        #TODO: standardize different surface variations of same dimension(eg Extraversion vs Extroversion), eg with list?
        #self.dimension_entities = []
        #for dimension_name in ["Openness", "Agreeableness", "Neuroticism", "Conscientiousness", "Extroversion"]:
        #    self.dimension_entities.append(PersonalityDimension(dimension_name, []))

        self.discovery = None
        self.environment_name = "Personality Recommendation Environment"
        self.environment_id = None
        self.collection_name = "Music Personality"
        self.collection_id = None

        self.config_name = "Music Personality Configuration xn4povqm3l"
        self.config_id = 'd8389d37-9f3d-4012-b0d1-0b7bf4fb606f'
        self.model_id = "492dc2fa-b316-4261-a334-0a22d1cb3e01"

        self.api_key = 'HtXSJos-QBQdkbPW30YojoQD2Btbx0eVL8v-M4ZXIkHZ'
        self.url = 'https://api.us-south.discovery.watson.cloud.ibm.com/instances/0c9ea94a-f8d3-4c61-9ee7-984ab92c5cad'

        self.setup()

    #Sets up Discovery instance and gets relevant ids
    def setup(self):

        #Authenticate
        authenticator = IAMAuthenticator(self.api_key)
        self.discovery = DiscoveryV1(
            version='2019-04-30',
            authenticator=authenticator
        )

        self.discovery.set_service_url(self.url)

        # Get environment info
        environments = self.discovery.list_environments().get_result()
        system_environments = [x for x in environments['environments'] if x['name'] == self.environment_name]
        self.environment_id = system_environments[0]['environment_id']

        # Get collection info
        collections = self.discovery.list_collections(self.environment_id).get_result()
        #print(collections)
        system_collections = [x for x in collections['collections'] if x['name'] == self.collection_name]
        self.collection_id = system_collections[0]['collection_id']

    #Updates the Discovery instance configuration of this.collection to new custom model
    #NOTE: only documents added to the collection AFTER this update will be processed with the new model;
    # this does not change the processing of documents already in the collection
    def update_model(self, new_model_id):
        self.model_id = new_model_id
        config = self.discovery.get_configuration(
            self.environment_id,
            self.config_id).get_result()
        #print(json.dumps(config, indent=2))
        config["enrichments"][0]["options"]["features"]["entities"]["model"] = new_model_id
        self.discovery.update_configuration(self.environment_id, self.config_id, config["name"],
                                        description=config["description"],
                                        conversions=config["conversions"],
                                        enrichments=config["enrichments"],
                                        normalizations=config["normalizations"]).get_result()
        #print(self.discovery.get_configuration(self.environment_id, self.config_id))


    #Returns list of {correlation_type:, genre: , dimension: } dicts
    # of relevant relations in Discovery query results
    def clean_results(self, result):
        relation_list = []
        search_results = result["results"]
        for result in search_results:
            relations = result["enriched_text"]["relations"]

            #print("Relationship types",set([relation["type"] for relation in relations if relation["type"] == "PositiveCorrelation" or relation["type"] == "NegativeCorrelation"])) #TODO: remove diagnostic print statement
            #TODO: remove diagnostic entity prints
            #entities = result["enriched_text"]["entities"]
            #print("Dimensions", set([entity["text"] for entity in entities if entity["type"] == "Dimension"]))
            #print("Genres", set([entity["text"] for entity in entities if entity["type"] == "Genre"]))

            relevant_music_relations = [relation for relation in relations if
                                        relation["type"] == self.pos_relation_name or relation[
                                            "type"] == self.neg_relation_name] #Only get PositiveCorrelation and NegativeCorrelation results
            for correlation in relevant_music_relations:
                #print("Custom Correlation Found") #TODO: remove diagnostic print
                dimension_name = correlation["arguments"][0]["text"] #Dimension is argument 0
                genre = correlation["arguments"][1]["text"] #Genre is argument 1
                correlation_type = correlation["type"]
                print(correlation_type)
                relation_list.append({"correlation_type": correlation_type, "genre": genre, "dimension_name":dimension_name})
        return relation_list

    #Backup dummy method not using relationships to get genres from result
    #Returns a set of all genres co-occuring in the results
    #result: dictionary result from Discovery query, an aggregation of entities of type Genre
    def get_genre_entities_from_result(self, result):
        search_results = result["aggregations"][0]["aggregations"][0]["aggregations"][0]["results"]
        return set([result["key"] for result in search_results])
        # genre_list = []
        #for result in search_results:
        #    entities = result["enriched_text"]["entities"]
        #    genre_list = genre_list + [entity["text"] for entity in entities if entity["type"] == "Genre"]
        #return set(genre_list)

    # Takes list of results in form [{correlation_type:, genre: , dimension: }] and
    # returns list of PersonalityDimension objects
    def process_query_result(self, result_list):
        dimension_correlates = {} #key personality dimension objects by name for easy access
        for result in result_list:
            print(result["type"])
            dimension_name = result["dimension"]
            dimension = dimension_correlates.get(dimension_name, PersonalityDimension(dimension_name))
            if result["type"] == self.pos_relation_name:
                dimension.pos_correlation_genres.add(result["genre"])
            else:
                dimension.neg_correlation_genres.add(result["genre"])
            if dimension_name not in dimension_correlates.keys():
                dimension_correlates[dimension_name] = dimension
        return [dimension_correlates[name] for name in dimension_correlates]

    #Returns:
    #   list of positively correlating genres
    #   list of negatively correlating genres
    # The lists will include duplicates of genres if they are correlated with more than one trait in high_scoring_traits.
    # given a list of high scoring personality traits(list
    # of strings of the names: agreeableness, openness to experience, extroversion, conscientiousness, neuroticism
    #If dummy: uses only genres that co-occur with traits and returns all in the positive set
    #Else: uses genres that have positive or negative correlation with traits in the corresponding positive/negative set
    def get_genres(self, high_scoring_traits, dummy=True):
        if not dummy:
            query_result = self.discovery.query(self.environment_id, self.collection_id,
                                                natural_language_query=" and ".join(high_scoring_traits)).get_result()
            formatted_results = self.clean_results(query_result)
            dimension_results = self.process_query_result(formatted_results)
            pos_genres = [genre for dimension in dimension_results for genre in dimension.pos_correlation_genres]
            neg_genres = [genre for dimension in dimension_results for genre in dimension.neg_correlation_genres]
            return (pos_genres, neg_genres)
        else:
            if high_scoring_traits == []:
                return ([],[])
            query_result = self.discovery.query(self.environment_id, self.collection_id,natural_language_query= " and ".join(high_scoring_traits),
                                                aggregation="nested(enriched_text.entities).filter(enriched_text.entities.type::\"Genre\").term(enriched_text.entities.text,count:5)").get_result()
            return (self.get_genre_entities_from_result(query_result), [])


if __name__ == "__main__":
    music_querier = MusicGenreQuerier()
    print(music_querier.get_genres(["Openness to experience"]))
    print(music_querier.get_genres(["Openness to experience", "Agreeableness"], dummy=False))
    #sample_result = music_querier.discovery.query(music_querier.environment_id, music_querier.collection_id,natural_language_query= "openness",
    #                                           aggregation="nested(enriched_text.entities).filter(enriched_text.entities.type::\"Genre\").term(enriched_text.entities.text,count:5)").get_result()
    #json.dump(sample_result,open("../test/discovery_music_tests/empty_dummy_query_result", "w"), indent=2)










#config = discovery.get_configuration(
#    environment_id,
#    config_id).get_result()
#print(json.dumps(config, indent=2))
#config["enrichments"][0]["options"]["features"]["entities"]["model"] = model_id
# updated_config = discovery.update_configuration(environment_id, config_id, config["name"],
#                                description=config["description"],
#                                conversions=config["conversions"],
#                                enrichments=config["enrichments"],
#                                normalizations=config["normalizations"]).get_result()


