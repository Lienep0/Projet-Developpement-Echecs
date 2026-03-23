package logic.exceptions;

public class OutOfBoardException extends RuntimeException {
    public OutOfBoardException(String message) {
        super(message);
    }
}
