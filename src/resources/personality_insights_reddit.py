from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from os.path import join
import json

#Places IBM Watson profile big 5 trait percentiles into a list (percentile for) [agreeableness, conscientiousness, extraversion, emotional range, openness]
#assumes fixed order in big5
class RedditPersonality:
    authenticator = IAMAuthenticator('ALlGKY01Pa-PQHPoQeBULOGX-180mT7iGjuvD4cx9Mlq')
    personality_insights = PersonalityInsightsV3(
        version='2017-10-13',
        authenticator=authenticator
    )
    personality_insights.set_service_url('https://api.us-south.personality-insights.watson.cloud.ibm.com/instances/ca0246f9-d739-44e0-a8dc-7c9e98b26886')

    def traits_to_vector(self, profile):
        if profile is None:
            return {}
        big5_objects = profile["personality"]
        '''
        big5_vector = []
        for trait in big5_objects:
            big5_vector.append(trait["name"])
            big5_vector.append(trait["percentile"])
        '''
        big5_vector = {}
        for trait in big5_objects:
            big5_vector[trait["name"]] = trait["percentile"]
        return big5_vector
    
    def get_profile(self, filename):
        if os.path.getsize(filename) <= 0:
            return None
    
        f = open(filename, encoding = 'utf-8') 
        profile = RedditPersonality.personality_insights.profile(
                  " ".join(f),
                  'application/json',
                  content_type='text/plain',
                  consumption_preferences=True,
                  raw_scores=True
                  ).get_result()

        f.close()
        return profile
