
# Translate Big 5 to MBTI
class PersonalityTranslator:
    def __init__(self, traits):
        # Big 5
        self.neuro = traits['Emotional range'] * 100
        self.extra = traits['Extraversion'] * 100
        self.open = traits['Openness'] * 100
        self.agree = traits['Agreeableness'] * 100
        self.conscientious = traits['Conscientiousness'] * 100
        
        # MBTI
        # Extraversion vs Introversion
        self.E = 0
        self.I = 0

        # Sensation vs Intuition
        self.S = 0
        self.N = 0

        # Thinking vs Feeling
        self.T = 0
        self.F = 0

        # Judging vs Perceiving
        self.J = 0
        self.P = 0


    def calculator(self):
        self.E = self.neuro * (-0.24) + self.extra * 0.69 + self.open * 0.21 + self.agree * 0.00 + self.conscientious * 0.03
        self.I = self.neuro * 0.26 + self.extra * (-0.46) + self.open * 0.22 + self.agree * (-0.01) + self.conscientious * 0.06

        self.S = self.neuro * (-0.02) + self.extra * (-0.18) + self.open * 0.52 + self.agree * 0.03 + self.conscientious * 0.20
        self.N = self.neuro * 0.03 + self.extra * 0.16 + self.open * 0.49 + self.agree * 0.03 + self.conscientious * 0.24

        self.T = self.neuro * (-0.16) + self.extra * 0.09 + self.open * 0.22 + self.agree * 0.40 + self.conscientious * (-0.28)
        self.F = self.neuro * 0.18 + self.extra * 0.05 + self.open * 0.22 + self.agree * 0.40 + self.conscientious * (-0.28)

        self.J = self.neuro * 0.01 + self.extra * (-0.03) + self.open * (-0.24) + self.agree * 0.06 + self.conscientious * 0.50
        self.P = self.neuro * (-0.00) + self.extra * 0.02 + self.open * 0.24 + self.agree * 0.00 + self.conscientious * (-0.41)

        result = []
        if self.E > self.I:
           result.append('E')
        else:
           result.append('I')
    
        if self.S > self.N:
           result.append('S')
        else:
           result.append('N')      
    
        if self.T > self.F:
           result.append('T')
        else:
           result.append('F') 
    
        if self.J > self.P:
           result.append('J')
        else:
           result.append('P')

        return result

# Testing
if __name__ == "__main__":
   traits = {'Openness': 0.959140460372601, 'Conscientiousness': 0.5774119639163334, 'Extraversion': 0.17586422494357157, 'Agreeableness': 0.1091535571286823, 'Emotional range': 0.3187110015885801}
   pt = PersonalityTranslator(traits)
   print(pt.calculator())