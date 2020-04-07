
# Translate Big 5 to MBTI
class PersonalityTranslator:
    def __init__(self):
        # Big 5
        self.neuro = 0
        self.extra = 0
        self.open = 0
        self.agree = 0
        self.conscientious = 0
        
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


    def calculator(self, traits):
        self.neuro = traits['Emotional range'] * 100
        self.extra = traits['Extraversion'] * 100
        self.open = traits['Openness'] * 100
        self.agree = traits['Agreeableness'] * 100
        self.conscientious = traits['Conscientiousness'] * 100
        
        self.E = self.neuro * (-0.24) + self.extra * 0.69  + self.open * (-0.30) + self.agree * 0.00  + self.conscientious * (-0.11) 
        self.I = self.neuro * 0.26 + self.extra * (-0.46) + self.open * 0.30 + self.agree * (-0.01)  + self.conscientious * 0.01 

        self.S = self.neuro * (-0.02) * 0.05 + self.extra * (-0.18) * 0.11 + self.open * 0.52 * 0.48 + self.agree * (-0.11) * 0.04 + self.conscientious * 0.20 * (-0.15)
        self.N = self.neuro * 0.03 * 0.05 + self.extra * 0.16 * 0.11 + self.open * 0.49 * 0.48 + self.agree * 0.29 * 0.04 + self.conscientious * 0.24 * (-0.15)

        self.T = self.neuro * (-0.16) * 0.06 + self.extra * 0.09 * 0.19 + self.open * 0.22 * 0.02 + self.agree * 0.40 * 0.44 + self.conscientious * (-0.28) * (-0.15)
        self.F = self.neuro * 0.18 * 0.06 + self.extra * 0.05 * 0.19 + self.open * 0.22 * 0.02 + self.agree * 0.40 * 0.44 + self.conscientious * (-0.28) * (-0.15)

        self.J = self.neuro * (-0.25) + self.extra * (-0.03) + self.open * (-0.24) + self.agree * 0.06 + self.conscientious * 0.50 
        self.P = self.neuro * 0.30 + self.extra * 0.02 + self.open * 0.24 + self.agree * 0.00 + self.conscientious * (-0.41)

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

        return ('').join(result)
