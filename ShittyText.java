import java.util.ArrayList;

public class ShittyText {

    public static void main(String[] args) {

        ArrayList<WordFollowers> words = new ArrayList<WordFollowers>();
        String[] data = args.toLowerCase().split(" ");
        //String input = "Hello my name is lucas and cake is my favourite food is my";
        //String[] data = input.toLowerCase().split(" ");

        for (int i = 0; i < data.length-1; i++) {
            String word = data[i];
            String follower = data[i+1];
            boolean added = false;
            for (WordFollowers existing : words) {
                if (existing.word.equals(word)) {
                    existing.addFollower(word);
                    added = true;
                    break;
                }
            }
            if (!added) {
                words.add(new WordFollowers(word, follower));
            }
        }

        for (int j = 0; j < words.size(); j++) {
            System.out.println(words.get(j).toString());
        }
    }

}
