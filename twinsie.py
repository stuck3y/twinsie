class Twinsie:
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2
        self.str1_words = self._get_words(str1)
        self.str2_words = self._get_words(str2)
        self.common_words = self.str1_words & self.str2_words
        self.all_words = self.str1_words | self.str2_words
        self.uncommon_words = self.str1_words ^ self.str2_words
        self.score = 0
        self.threshold = 0.5
        
    def _get_words(self, s):
        s = self._sanitize(s)
        return set(s.split())
    
    def _sanitize(self, s):
        s = s.lower()
        s = s.replace('.', '')
        s = s.replace('_', '')
        s = s.replace(',', '')
        s = s.replace(';', '')
        s = s.replace('?', '')
        s = s.replace('!', '')
        return s

    def run(self):
        self.compare_words()
        self.compare_chars()
        print(f'score = {self.score}')

    def compare_words(self):
        self.score = float(len(self.common_words))/float(len(self.all_words))

    def compare_chars(self):
        fuzzy_match_count = 0
        for word in self.uncommon_words:
            if word in self.str1_words:
                if self._fuzzy_match(word, self.str2_words):
                    fuzzy_match_count += 1
            else:
                if self._fuzzy_match(word, self.str1_words):
                    fuzzy_match_count += 1
        
        print(f'fuzzy_match_count = {fuzzy_match_count}')
        fuzzy_score = float(fuzzy_match_count)/float(len(self.all_words))
        print(f'fuzzy_match_count/self.all_words = {fuzzy_score}')

        remainder = 1 - self.score
        print(f'remainder = {remainder}')
        if self.score > 0:
            self.score = self.score + (fuzzy_score * remainder)


    def _fuzzy_match(self, source_word, target_words, threshold=None):
        """Check for a fuzzy match for source_word in target_words.

        This is based on the given threshold, set from 0 to 1.
        
        Args:
            source_word (str): word to try to fuzzy match to
            target_words (set/list): words to fuzzy match against
        Keyword Args:   
            threshold (float) Default `None` - strength of match requirement
        """
        if threshold == None:
            threshold = self.threshold

        match_found = False 
        
        for word in target_words:
            word_chars = set(word)
            source_word_chars = set(source_word)
            common_chars = word_chars & source_word_chars
            all_chars = word_chars | source_word_chars
            fuzzy_score = float(len(common_chars)) / float(len(all_chars))
            print(f'fuzzy_score(target = {word}, source = {source_word}) = {fuzzy_score}')
            if fuzzy_score >= threshold:
                match_found = True
        return match_found