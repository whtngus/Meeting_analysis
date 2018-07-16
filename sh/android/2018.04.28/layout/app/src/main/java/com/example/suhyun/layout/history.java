package com.example.suhyun.layout;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;

public class history extends AppCompatActivity {
    Button serarch_date,search_keyword,serach_subject,getting_detail,delete;
    EditText input_keyword,input_subject;
    ListView sort_standard;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);
        setTitle("history");
        getting_detail = (Button) findViewById(R.id.geting_detail);

        getting_detail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(history.this,Detail_history.class);
                startActivity(intent);
            }
        });
    }
}
