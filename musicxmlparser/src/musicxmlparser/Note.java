package musicxmlparser;

/**
 * Created by Dorien Herremans on 01/02/15.
 */
public class Note {

    private Integer startTime;
    private Integer duration;
    private String pitch;     //Z is for rest
    private Integer voice;
    private String accidental;
    private Integer counter;

    public void setCounter(Integer counter) {
        this.counter = counter;
    }

    public Integer getCounter() {
        return counter;
    }

    public Integer getVoice() {
        return voice;
    }

    public void setVoice(Integer voice) {
        this.voice = voice;
    }

    public Note(Integer startTime) {
        this.startTime = startTime;
        this.accidental = "";

    }

    public void setStartTime(Integer startTime) {
        this.startTime = startTime;
    }

    public void setDuration(Integer duration) {
        this.duration = duration;
    }

    public void setPitch(String pitch) {
        this.pitch = pitch;
    }

    public Integer getStartTime() {
        return startTime;
    }

    public Integer getDuration() {
        return duration;
    }

    public String getPitch() {
        return pitch;
    }


    public void setAccidental(String accidental) {
        this.accidental =  accidental;
    }

    public String getAccidental() {

        return accidental;
    }
}