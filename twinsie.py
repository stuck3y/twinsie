class Twinsie:
    """The Twinsie class/module compares two strings and scores their similarity.

    The overall score ranges from 0 (not similar at all) to 1 (perfectly
    similar, or exactly the same). Twinsie uses three methods to determine
    this score. First, it looks at common words in comparison to all of the words.
    This is similar to the Jaccard's distance calculation. This is the most basic 
    of the three methods and can be a poor similarity method on its own. 
    
    To mitigate that, and add more precision, method two attempts to take all 
    of the uncommon words between the two strings and see if we can fuzzy match 
    them against each other. Any fuzzy matches are accounted for and factored 
    into the overall score. 
    
    Lastly, we look at the order of the words to add even more precision to the 
    final score. We take all of the common words and evaluate their position in
    one text string in relation to its position in the other text string. If it
    exist within the bounds of a pre-defined window, we consider that a "match"
    and that is factored into the final score.

    """
    def __init__(self, str1, str2):
        """The class takes in the two text strings as parameters.

        In the init (constructor), I preset some of the most frequent operations
        including union, intersecting and xor'ing the set/list that consists of
        the words in the strings passed in.

        Args:
            str1 (str): text string number one
            str1 (str): text string number two
        """
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
        """Sanitize and split up the string into the words that make it up.
        
        Args:
            s (str): the raw string
        Keyword Args:
            unique (bool) `default: True` - flag for unique set or all words
        Returns:
            s (set or list): the clean set or list of words
        """
        s = self._sanitize(s)
        s = s.split()
        if unique:
            s = set(s)
        return s
    
    def _sanitize(self, s):
        """Clean up the string in preparation for comparison operations.
        
        Args:
            s (str): the raw string
        Returns:
            s (str): the clean string
        """
        s = s.lower()
        s = s.replace('.', '')
        s = s.replace('_', '')
        s = s.replace(',', '')
        s = s.replace(';', '')
        s = s.replace('?', '')
        s = s.replace('!', '')
        return s

    def run(self):
        """Kickoff the comparison methods."""
        self.compare_words()
        self.compare_chars()
        self.compare_word_pos()
        # print(f'score = {self.score}')
        return f'score = {self.score}'

    def compare_words(self):
        """Calculate a basic score with common words divided by all words."""
        self.score = float(len(self.common_words))/float(len(self.all_words))

    def compare_chars(self):
        """Leverage fuzzy matching to add precision to the overall score.

            The goal here is to use the uncommon words not included in the 
            score as it stands (after the basic calculation), and see if 
            we can find fuzzy matches between them. If we do, we factor 
            those into the score with a similar calculation to the basic one
            above. 

            It is worth mentioning that there is a threshold we can tweak
            at the top of the module, which allows us to be more lenient or
            more strict in our matching. See that in action in the code for
            the fuzzy match method.

            Note that I have added a scale to this in order to prevent a
            perfect score from being reached without the two strings being
            exactly the same.

        """
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
            threshold (float) `default: None` - strength of match requirement
        Returns:
            match_found (bool): flag indicating whether a match was found or not
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
        """This third method compares word positions between the two strings.

        With this one, we create a dictionary out of the words that exist
        in each text string. At each dictionary index is a list of all 
        occurrences of that word in the string. The occurrences are stored
        as numerical positions.

        I use the numerical positions (list indexes) to compare between
        the two word dictionaries. There is a tolerance window that can be
        widened or narrowed above (the pos_window instance variable).

        This gives order the proper place to factor into the final score.

        Note (again) that I have added a scale to this in order to prevent a
        perfect score from being reached without the two strings being
        exactly the same.

        Keyword Args:
            window (float) `default: None` - tolerance window for order scoring
        """
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
        pos_total = self._get_pos_total()
        print(f'pos_counter total = {pos_total}')
        
        pos_score = float(pos_matches) / pos_total
        print(f'pos_score = {pos_score}')

        remainder = 1 - self.score
        print(f'remainder = {remainder}')
        if self.score > 0:
            self.score = self.score + (pos_score * remainder * self.pos_score_scale)

    def _position_match(self, word, target_dict, position, window):
        """Check for positional matches of words in two strings
        
        Args:
            word (str): the word that's being matched
            target_dict (dict): the dictionary of word positions
            position (int): the current position(s) of the word in string
            window (int): the tolerance window for matching, the wider the looser
        Returns:
            True/False (bool): flag indicating whether a match was found
        """
        upper_bound = position + window
        lower_bound = position - window
        for i in range(lower_bound, upper_bound):
            if i in target_dict[word]:
                print(f'position matches for {word}')
                return True
        return False

    def _get_positions_dict(self, source_str):
        """Convert a string into a dict of lists containing positions for its words.

        Args:
            source_str (str): the input string to convert
        Returns: 
            s_dict (dict): dictionary with a strings words as keys and positions (list) as values
        """
        s_dict = dict()
        words = self._get_words(source_str, unique=False)
        for word in words:
            s_dict[word] = [i for i, x in enumerate(words) if x == word]
        return s_dict

    def _get_pos_total(self):
        """Set total word positions to the max word list length between the two strings.

        This is the conservative choice since it's better that order of words have too
        little of a say in the final score than too much.

        Returns: 
            pos_total (float): max length of words list 
        """
        str1_word_count = float(len(self._get_words(self.str1, unique=False)))
        str2_word_count = float(len(self._get_words(self.str2, unique=False)))
        if str1_word_count > str2_word_count:
            return str1_word_count
        return str2_word_count