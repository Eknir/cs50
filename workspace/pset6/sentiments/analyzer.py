import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # make positive list in memory
        open(positives)
        with open("positive-words.txt") as lines:
            self.positives = set()
            for line in lines:
                # continue only if the line does not start with ; or space
                if not line.startswith(";"):
                        if not line.startswith(" "):
                            # make sure that there are no trailing whitespaces
                            line = line.rstrip()
                            #append line to dictionary
                            self.positives.add(line.rstrip("\n"))

        # make negative list in memory
        open(negatives)
        with open("negative-words.txt") as lines:
            self.negatives = set()
            for line in lines:
                # continue only if the line does not start with ; or space
                if not line.startswith(";"):
                    if not line.startswith(" "):
                        # make sure that there are no trailing whitespaces
                        line = line.rstrip()
                        #append line to dictionary
                        self.negatives.add(line.rstrip("\n"))

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        # split text into a list with words
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        # initialize score
        score = 0
        # construct analyzer
        # run over the list of words
        for word in tokens:
            # make word lowercase to match dictionary
            word = str.lower(word)
            # increase score if in positives
            if word in self.positives:
                score += 1
            # decrease score if in negatives
            elif word in self.negatives:
                score -= 1

        return score
