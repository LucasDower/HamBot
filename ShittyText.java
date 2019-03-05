import java.util.ArrayList;

public class ShittyText {

    private static ArrayList<WordFollowers> words = new ArrayList<WordFollowers>();

    private static void addWord(String word, String follower) {
        for (WordFollowers existing : words) {
            if (existing.word.equals(word)) {
                existing.addFollower(follower);
                return;
            }
        }
        words.add(new WordFollowers(word, follower));
    }

    private static WordFollowers findWF(String word) {
        for (int i = 0; i < words.size(); i++) {
            WordFollowers wf = words.get(i);
            if (wf.word.equals(word)) {
                return wf;
            }
        }
        return null;
    }

    private static String generateText(int wordCap) {
        // Get random starting word
        int rand = (int) Math.floor(Math.random() * words.size());
        WordFollowers wf = words.get(rand);
        String word = wf.word;

        String sentence = word;
        while (wordCap > 0) {
            String newFollower = wf.getWRandomFollower();
            wf = findWF(newFollower);
            if (wf == null) {
                break;
            }
            sentence += " " + newFollower;
            wordCap--;
        }
        return sentence;
    }

    public static void main(String[] args) {
        for (int i = 0; i < args.length-1; i++) {
            addWord(args[i], args[i+1]);
        }

        System.out.println(generateText(10));
    }

}
