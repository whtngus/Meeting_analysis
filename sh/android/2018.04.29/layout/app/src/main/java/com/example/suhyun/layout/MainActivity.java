package com.example.suhyun.layout;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.beardedhen.androidbootstrap.BootstrapButton;
import com.beardedhen.androidbootstrap.TypefaceProvider;

public class MainActivity extends AppCompatActivity {
    BootstrapButton favorites,start_meeting,search_meeting,participation_meeting,view_accounts,calender,setting;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TypefaceProvider.registerDefaultIconSets();
        setContentView(R.layout.activity_main);
        setTitle("MainActivity");

        start_meeting = (BootstrapButton) findViewById(R.id.start_meeting);
        favorites = (BootstrapButton) findViewById(R.id.favorites);
        setting = (BootstrapButton) findViewById(R.id.setting);
        search_meeting = (BootstrapButton) findViewById(R.id.search_meeting);

        start_meeting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this,Conference_pre.class);
//                intent.putExtra("text",String))
                startActivity(intent);
            }
        });

        favorites.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this,Join_Add.class);
                startActivity(intent);
            }
        });

        setting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this,Setting.class);
                startActivity(intent);
            }
        });

        search_meeting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this,history.class);
                startActivity(intent);
            }
        });
    }

}
