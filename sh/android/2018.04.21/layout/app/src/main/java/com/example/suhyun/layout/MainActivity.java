package com.example.suhyun.layout;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    Button favorites,start_meeting,search_meeting,participation_meeting,view_accounts,calender,setting;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setTitle("MainActivity");

        start_meeting = (Button) findViewById(R.id.start_meeting);
        start_meeting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this,Conference_pre.class);
//                intent.putExtra("text",String))
                startActivity(intent);
            }
        });
    }


}
