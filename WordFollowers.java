import java.util.ArrayList;

public class WordFollowers {

    public String word;
    public ArrayList<WordCount> followers = new ArrayList<WordCount>();

    public WordFollowers(String w, String follower) {
        word = w;
        followers.add(new WordCount(follower));
    }

    public void addFollower(String follower) {
        for (WordCount existing : followers) {
            if (existing.word.equals(follower)) {
                existing.incCount();
                return;
            }
        }
        followers.add(new WordCount(follower));
    }

    public String toString() {
        String sen = "[";
        for (WordCount wc : followers) {
            sen += word + " -> " + wc.toString();
        }
        return sen + "]";
    }

}
