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
        self.fuzzy_threshold = 0.5
        self.pos_window = 2
        self.char_score_scale = 0.95
        self.pos_score_scale = 0.95
    
    def _get_words(self, s, unique=True):
        s = self._sanitize(s)
        s = s.split()
        if unique:
            s = set(s)
        return s
    
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
        self.compare_word_pos()
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
            self.score = self.score + (fuzzy_score * remainder * self.char_score_scale)
    
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
            threshold = self.fuzzy_threshold

        match_found = False 
        
        for word in target_words:
            word_chars = set(word)
            source_word_chars = set(source_word)
            common_chars = word_chars & source_word_chars
            all_chars = word_chars | source_word_chars
            fuzzy_score = float(len(common_chars)) / float(len(all_chars))
            if fuzzy_score >= threshold:
                print(f'fuzzy_score(target = {word}, source = {source_word}) = {fuzzy_score}')
                match_found = True
        return match_found

    def compare_word_pos(self, window=None):
        if window is None:
            window = self.pos_window
        pos_matches = 0
        pos_counter = 0

        str1_pos_dict = self._get_positions_dict(self.str1)
        str2_pos_dict = self._get_positions_dict(self.str2)
        
        for word, positions in str1_pos_dict.items():
            if word in str2_pos_dict.keys():
                for pos in positions:
                    if self._position_match(
                        word, str2_pos_dict, 
                        pos, window):
                        pos_matches += 1
                    pos_counter += 1         

        print(f'str1_pos_dict = {str1_pos_dict}')
        print(f'str2_pos_dict = {str2_pos_dict}')
        print(f'pos_matches total = {pos_matches}')
        print(f'pos_counter total = {pos_counter}')
        
        pos_score = float(pos_matches) / float(pos_counter)
        print(f'pos_score = {pos_score}')

        remainder = 1 - self.score
        print(f'remainder = {remainder}')
        if self.score > 0:
            self.score = self.score + (pos_score * remainder * self.pos_score_scale)

    def _position_match(self, word, target_dict, position, window):
        upper_bound = position + window
        lower_bound = position - window
        for i in range(lower_bound, upper_bound):
            if i in target_dict[word]:
                print(f'position matches for {word}')
                return True
        return False

    def _get_positions_dict(self, source_str):
        s_dict = dict()
        words = self._get_words(source_str, unique=False)
        for word in words:
            s_dict[word] = [i for i, x in enumerate(words) if x == word]
        return s_dict