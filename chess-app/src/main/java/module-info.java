module org.example.chessapp {
    requires javafx.controls;
    requires javafx.fxml;
	requires javafx.graphics;


    opens org.example.chessapp to javafx.fxml;
    exports org.example.chessapp;
    exports ui.javafx;
}
