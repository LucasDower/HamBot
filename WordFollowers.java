import java.util.ArrayList;
import java.util.Arrays;

public class WordFollowers {

    public String word;
    public int totalOccurances; // The sum of the counts of all followers
    public ArrayList<WordCount> followers = new ArrayList<WordCount>();

    public WordFollowers(String w, String follower) {
        word = w;
        totalOccurances = 1;
        followers.add(new WordCount(follower));
    }

    // Return a weighted random follower
    public String getWRandomFollower() {
        int rand = (int) Math.floor(Math.random() * totalOccurances);
        int runningSum = 0;
        for (int i = 0; i < followers.size(); i++) {
            WordCount wc = followers.get(i);
            runningSum += wc.count;
            if (runningSum > rand) {
                return wc.word;
            }
        }
        return "null";
    }

    public void addFollower(String follower) {
        totalOccurances++;
        for (WordCount existing : followers) {
            if (existing.word.equals(follower)) {
                existing.incCount();
                return;
            }
        }
        followers.add(new WordCount(follower));
    }

    public String toString() {
        String sen = "[" + word + " -> ";
        for (WordCount wc : followers) {
            sen += wc.toString();
        }
        return sen + "]";
    }

}
