class WordCount():
    def __init__(self, word):
        self.word = word
        self.count = 1

    def incCount(self):
        self.count += 1

    def __str__(self):
        return "(" + word + ": " + str(count) + ")"

class WordFollowers(object):
    def __init__(self, word, follower):
        self.word = word
        self.followers = [follower]

    def addFollower(follower):
        for f in followers:
            if f.word == follower:
                f.incCount()
                return
        followers.append(WordCount(follower))

    def __str__(self):
        sen = "[" + word + ": "
        for follower in self.followers:
            sen += str(follower)
        return sen + "]"
            
data = "Hello my name is lucas and cake is my favourite food"
data = data.lower().split(" ")

print(data)

words = list(set(data))
wordCounts = []

for i in range(len(data)-1):
    word = data[i]
    follower = data[i+1]
    added = False
    for existing in wordCounts:
        if word == existing.word:
            existing.addFollower(follower)
            added = True
            break
    if not added:
        wordCounts.append(WordFollowers(word, follower))

print(wordCounts)
