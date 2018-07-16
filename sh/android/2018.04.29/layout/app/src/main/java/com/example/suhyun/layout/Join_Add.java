package com.example.suhyun.layout;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;

public class Join_Add extends AppCompatActivity {

    Button recommend_list,getting_list,serarch_company,makeGroup;
    EditText input_id,company_id;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_join__add);
    }
}
