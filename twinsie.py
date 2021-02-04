class Twinsie:
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2
        self.str1_words = self._get_words(str1)
        self.str2_words = self._get_words(str2)
        self.common_words = self.str1_words & self.str2_words
        self.all_words = self.str1_words | self.str2_words
        self.uncommon_words = self.str1_words ^ self.str2_words
        
    def _get_words(self, s):
        return set(s.split())

    def run(self):
        pass