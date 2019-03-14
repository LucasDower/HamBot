import wikipedia as w, random, re

class WordFollowers():
    def __init__(self, word, follower):
        self.word = word
        self.followers = [follower]

    def addFollower(self, follower):
        self.followers.append(follower)

    def getFollower(self):
        return random.choice(self.followers)

def shittytext(searchTerm):
    words = []
    articles = w.search(searchTerm)
    if len(articles) == 0:
        return "Search term not found"
    
    plaintext = re.sub('[^a-zA-Z ]+', '', w.summary(articles[0]))
    data = plaintext.lower().split(" ")

    def addWordFollower(word, follower):
        for j in words:
            if j.word == word:
                j.addFollower(follower)
                return
        words.append(WordFollowers(word, follower))

    for i in range(0, len(data)-1):
        addWordFollower(data[i], data[i+1])

    def findFollower(follower):
        for i in words:
            if i.word == follower:
                return i
        return None

    wordCap = 50
    word = random.choice(words)
    sentence = [word.word]
    while (wordCap > 0):
        follower = word.getFollower()
        sentence.append(follower)
        word = findFollower(follower)
        if (word == None):
            word = random.choice(words)
        wordCap -= 1

    return ' '.join(sentence)
