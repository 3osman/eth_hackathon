from scipy.stats import multivariate_normal
import numpy as np
import math
class ObservationSequence:
    def __init__(self, seq):
        self.seq = seq
class Observation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Token:
    def __init__(self, hypo, acc_prob, obs_index):
        self.hypo = hypo
        self.acc_prob = acc_prob
        self.obs_index = obs_index
def get_prob(sentence, cutoff=10):
	trie_model = trie.Trie()
	lm         = kenlm.LanguageModel('big.klm')
	words      = open('big.txt', 'r').read().split()
	for word in words:
		trie_model.add(word)
	
	if sentence[-1] == ' ':
		return
	words = sentence.split(' ')
	last_word = words[-1]
	
	possible_words = trie_model.start_with_prefix(last_word)
	scores = {}
	for possible_word in possible_words:
		words.append(possible_word)
		sentence = ' '.join(words)
		scores[possible_word] = lm.score(sentence)

	return sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[:cutoff]

# Populate the bigram with computed probabilities
bigram_lm = {'_a':0.05,'_b':0.05,'_c':0.05,'_d':0.05,\
      'aa':0.05,'ab':0.05,'ac':0.05,'ad':0.05,\
      'ba':0.05,'bb':0.05,'bc':0.05,'bd':0.05,\
      'ca':0.05,'cb':0.05,'cc':0.05,'cd':0.05,\
      'da':0.05,'db':0.05,'dc':0.05,'dd':0.05}
unigram = {'a': 0.08034221553373133, 'c': 0.02854112673771482, 'b': 0.014404733498550608, 'e': 0.12478255185877309, 'd': 0.04246686401389778, 'g': 0.01908011462834382, 'f': 0.023797036326538006, 'i': 0.07198468629586492, 'h': 0.05801504595449989, 'k': 0.006456900577472963, 'j': 0.0012668888988638753, 'm': 0.02501529716665761, 'l': 0.039108574839566784, 'o': 0.07616413997635928, 'n': 0.07265012288920757, 'q': 0.0008997175241348734, 'p': 0.0194732734676649, 's': 0.06593256016688677, 'r': 0.060943360714671026, 'u': 0.02731262841154379, 't': 0.09070806391026293, 'w': 0.019850879203177085, 'v': 0.010311707825298088, 'y': 0.017813225729479944, 'x': 0.0019311442438159677, 'z': 0.0007471396070222855}

# Modify get_prior to return prior for specified context
#def get_prior(context, bigram_lm):
 #   c = context[-1]
#    return lm[c]

def get_prior(context, unigram, bigram_lm):
	if len(context) > 1:
		c = context[-2:]
		return bigram_lm[c]
	else:
		c = context[0] 
		return unigram[c]

    #c = context[-2:] if len(context) > 1 else '_' + context[0]  
  # print(bigram_lm[c])
    #return bigram_lm[c]
obs_seq = []
#obs_seq = ObservationSequence([Observation(0.1,1.1),Observation(0.15,-0.1),Observation(1.05,0.95)]) #bad + noise
#obs_seq = ObservationSequence([Observation(0.1,1.1),Observation(0.15,-0.1),Observation(3.0,-2.7),Observation(1.05,0.95)]) #b - a - (Noisy input far away from any key) - d + noise
probable_sentences = [] #dictionary for kenlm stuff
completed_tokens = []
deletion_penalty = 0.02
insertion_penalty = 1.2
beam_width = 0.2

seed_token = Token("", 1.0, -1)

to_display_sentence = ""
def main_fun(x,y,char):
	if char == "<sp>":
		obs_seq = []
		return to_display_sentence
	else:
		obs_seq.push(Observation(x,y))
		propagate(token,obs_seq,completed_tokens)
		results = sorted(completed_tokens, key=lambda token: token.acc_prob, reverse=True)
		highest_prob = to_display_sentence + results[0].hypo
		sen = to_display_sentence.split()[:-1]
		' '.join(sen)
		return sen + " " + get_prob(highest_prob)[0][0]

def propagate(token, obs_seq, completed_tokens):
    # Which observation is the token in?
    ix = token.obs_index
    # Are there more observations?
    next_ix = ix + 1
    if next_ix == len(obs_seq.seq):
        # No more observations, add token to the list of completed tokens
        completed_tokens.append(token)
    else:
        # There is another observation, propagate tokens for all symbols to the next observation index
        next_obs = obs_seq.seq[next_ix]
        for symbol in symbols:
            if symbol == 'ɛ':
                acc_prob = token.acc_prob * deletion_penalty
                new_token = Token(token.hypo, acc_prob, next_ix)
                if not beam_prune(acc_prob, obs_seq, next_ix):
                    propagate(new_token, obs_seq, completed_tokens)
            else:
                key = get_key_for_symbol(symbol)
                prior = get_prior(token.hypo+symbol, lm)
                likelihood = get_likelihood(next_obs.x, next_obs.y, key)
                acc_prob = token.acc_prob * prior * likelihood
                new_token = Token(token.hypo+symbol, acc_prob, next_ix)
                if not beam_prune(acc_prob, obs_seq, next_ix):
                    propagate(new_token, obs_seq, completed_tokens)
    # Propagate tokens for all symbols (except epsilon) within the same observation index
    if ix >= 0:
        for symbol in sym bols:
            if not symbol == 'ɛ':
                key = get_key_for_symbol(symbol)
                prior = get_prior(token.hypo+symbol, lm)
                obs = obs_seq.seq[ix]
                acc_prob = token.acc_prob * prior * insertion_penalty
                # Create a new token but don't increment the observation index
                new_token = Token(token.hypo+symbol, acc_prob, ix)
                if not beam_prune(acc_prob, obs_seq, ix):
                    propagate(new_token, obs_seq, completed_tokens)