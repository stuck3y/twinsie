from flask import Flask

app = Flask(__name__)

def main_compare(string1, string2):
    
    # compare words - simplest
    word_score = word_compare(string1, string2)
    remainder = 1 - word_score

    # for leftover non-matches compare characters
    uncommon_words = set(string1.split()) ^ set(string2.split())
    
    # get string 1 words not in string 2
    string1_xor = []
    # get string 2 words not in string 1
    string2_xor = []
    for word in uncommon_words:
        if word in string1.split():
            string1_xor.append(word)
        else:
            string2_xor.append(word)
    
    # for each of those lists, each word, compare characters (using char compare)
    sim_char_count = 0
    sim_char_score_total = 0
    for word1 in string1_xor:
        for word2 in string2_xor:
            sim_char_count += 1
            sim_char_score = char_compare(word1, word2)
            sim_char_score_total += sim_char_score
    
    # average all char compare scores
    final_char_score = sim_char_score_total/sim_char_count
    
    # multiply that by the remainder to add that as a factor into the overall score
    final_score = word_score + remainder * final_char_score
    
    # update the remainder
    remainder = 1 - final_score

    # get pos_score (call pos_compare)
    pos_score = pos_compare(string1, string2)

    # multiply pos_score and remainder and add that to the score to get final_score
    final_score += remainder * pos_score

    return final_score

def pos_compare(string1, string2, window=3):
    """Compare the positions of words in the two strings. Scored based on tolerance window, 3 words by default."""
    def makeDict(s):
        """Convert a string to a dict indexed at each word. Each word's position is stored in a list at it's index. """
        s_dict = dict()
        s_list = s.split()
        for word in s_list:
            s_dict[word] = [i for i, x in enumerate(s_list) if x == word]
        return s_dict

    dict1 = makeDict(string1)
    dict2 = makeDict(string2)
        
    pos_counter = 0
    pos_matches = 0
    for word, pos_list in dict1.items():
        if word in dict2.keys():
            for pos in pos_list:
                pos_counter += 1
                upper_bound = pos + window
                lower_bound = pos - window
                for i in range(lower_bound, upper_bound):
                    if i in dict2[word]:
                        pos_matches += 1
                        break
    
    pos_raw_score = pos_matches/pos_counter
    return pos_raw_score

def char_compare(string1, string2):
    """Compare two strings by character to determine similarity."""
    common_chars = set(string1) & set(string2)
    all_chars = set(string1) | set(string2)
    char_raw_score = len(common_chars)/len(all_chars)
    return char_raw_score

def word_compare(string1, string2):
    """Compare two sentences or phrases by word to determine similarity."""
    def sentence_to_set(s):
        return set(s.split())

    common_words = sentence_to_set(string1) & sentence_to_set(string2)
    all_words = sentence_to_set(string1) | sentence_to_set(string2)
    raw_score = len(common_words)/len(all_words)
    return raw_score

@app.route('/')
def run():
    sample1 = "The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you."
    sample2 = "The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you."
    sample3 = "We are always looking for opportunities for you to earn more points, which is why we also give you a selection of Special Offers. These Special Offers are opportunities to earn bonus points on top of the regular points you earn every time you purchase a participating brand. No need to pre-select these offers, we'll give you the points whether or not you knew about the offer. We just think it is easier that way."

    score = main_compare(sample1, sample2)
    msg1 = f'Sample 1 compared to sample 2: {score}'

    score = main_compare(sample1, sample3)
    msg2 = f'Sample 1 compared to sample 3: {score}'

    return f'{msg1}\n{msg2}'

