module org.example.chessapp {
    requires javafx.controls;
    requires javafx.fxml;


    opens org.example.chessapp to javafx.fxml;
    exports org.example.chessapp;
}