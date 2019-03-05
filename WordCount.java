public class WordCount {
    public String word;
    public int count;

    public WordCount(String w) {
        word = w;
        count = 1;
    }

    public void incCount() {
        count++;
    }

    public String toString() {
        return String.format("(%s:%d)", word, count);
    }
}
