package com.example.suhyun.layout;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class Conference_pre extends AppCompatActivity {

    EditText subject,metting_room;
    Button add_invite,start_meeting;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_conference_pre);
        setTitle("Conference_pre");

        start_meeting = (Button) findViewById(R.id.start_meeting);
        start_meeting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Conference_pre.this,Conference.class);
//                intent.putExtra("text",String))
                startActivity(intent);
            }
        });
    }
}
