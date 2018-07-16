package com.example.suhyun.hanium_meetinganalysis;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.nfc.Tag;
import android.os.Build;
import android.os.Handler;
import android.os.Message;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.lang.reflect.Field;
import java.net.InetAddress;
import java.net.Socket;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Locale;
import java.util.logging.Logger;

public class MainActivity extends AppCompatActivity {

    Intent i;

    SpeechRecognizer mRecognizer;
    TextView textView;

    //퍼미션 위한 변수
    String[] permission = new String[]{Manifest.permission.INTERNET, Manifest.permission.RECORD_AUDIO, Manifest.permission.WAKE_LOCK};
    int PERMISSION_ALL = 1;
    String[] PERMISSIONS = {Manifest.permission.INTERNET, Manifest.permission.RECORD_AUDIO};

    // 음성인식 백그라운드로 계속 실행시키기 위한 변수
    boolean mBoolVoiceRecoStarted = false;
    private final int MSG_VOICE_RECO_STOP = 0;  //meg 로 사용하기 위한 변수
    private final int  MSG_VOICE_RECO_END=1;
    private final int  MSG_VOICE_RECO_RESTART=2;

    //버튼 클릭시 음성인식 실행,종료를 위한 변수설정
    boolean clickCount = false;


    //통신하기 위한 서버 url
    private static final String Socket_URL = "13.125.192.211";
//    private static final String Socket_URL = "175.204.115.54";
    private static final int Socket_PORT = 12345;

    private static SocketClass socketClass[] = new SocketClass[2];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



        //권한체크
        if(!hasPermissions(this, PERMISSIONS)){
            ActivityCompat.requestPermissions(this, PERMISSIONS, PERMISSION_ALL);
        }

        // 음성인식을 위한 준비작업
        i = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        i.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, getPackageName());
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "ko-KR");

        //버튼클릭시의 작업 설정
        mRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        mRecognizer.setRecognitionListener(listener);

        textView = (TextView) findViewById(R.id.textView);

       findViewById(R.id.button).setOnClickListener(mClickListener);


        // 소켓 미리 만들기
        try {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        socketClass[0] = new SocketClass(new Socket(Socket_URL, Socket_PORT));
                    } catch (IOException e) {
                        Log.d("Socket Main", "session - dis-connect" + e);
                    }
                }
            }).start();
        } catch (Exception e) {
            Log.d("Socket Main", "session - dis-connect" + e);
            socketClass[0].close();
        }
    }


    //권한 체크
    public static boolean hasPermissions(Context context, String... permissions) {
        if (context != null && permissions != null) {
            for (String permission : permissions) {
                if (ActivityCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {
                    return false;
                }
            }
        }
        return true;
    }





    // 다시 실행시키기 위한 핸들러
    private Handler mHdrVoiceRecoState = new Handler()
    {
        @Override
        public void handleMessage(Message msg)
        {
            switch (msg.what)
            {
                case MSG_VOICE_RECO_STOP	: break;
                case MSG_VOICE_RECO_END		:
                {
                    stopListening();
                    sendEmptyMessageDelayed(MSG_VOICE_RECO_RESTART, 100);
                    break;
                }
                case MSG_VOICE_RECO_RESTART	: startListening();	break;
                default:
                    super.handleMessage(msg);
            }
        }
    };

    // 비정상시 종료
    public void stopListening()
    {
        try
        {
            if (mRecognizer != null && mBoolVoiceRecoStarted == true)
            {
                mRecognizer.stopListening();
            }
        }
        catch(Exception ex)
        {
            Log.e("Main Activity","stopListening - 에러 문구 : "+ex);
//            Logger.e("Stop 예외:"+ StrUtil.trace(ex));
        }
        mBoolVoiceRecoStarted = false;
    }

    // 음성인식 실행 메소드
    public void startListening()
    {
        if(mBoolVoiceRecoStarted == false)
        {
//            if(mRecognizer == null)
//            {
//                mRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
//                mRecognizer.setRecognitionListener(listener);
//            }
            if(mRecognizer.isRecognitionAvailable(this))
            {
//                Intent itItent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
//                itItent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, this.getPackageName());
//                itItent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.KOREAN.toString());
//                itItent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 50);
                mRecognizer.startListening(i);
            }
        }
        mBoolVoiceRecoStarted = true;
    }



    Button.OnClickListener mClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            clickCount = !clickCount;
            startListening();

            //push 버튼 text
            Button button = (Button) findViewById(R.id.button);
            if(button.getText() == "push to stop"){
                button.setText("push to talk");
            }else{
                button.setText("push to stop");
            }
        }
    };





    private RecognitionListener listener = new RecognitionListener() {

        @Override
        public void onReadyForSpeech(Bundle params) {
        }
        @Override
        public void onBeginningOfSpeech() {
        }

        @Override
        public void onRmsChanged(float rmsdB) {
        }

        @Override
        public void onBufferReceived(byte[] buffer) {
        }

        @Override
        public void onEndOfSpeech() {
        }

        @Override
        public void onError(int error) {
            if(clickCount){
                mHdrVoiceRecoState.sendEmptyMessage(MSG_VOICE_RECO_END);
            }else{
                mHdrVoiceRecoState.sendEmptyMessage(MSG_VOICE_RECO_STOP);
                mBoolVoiceRecoStarted = false;
            }
        }

        @Override
        public void onResults(Bundle results) {
            if(clickCount){
                mHdrVoiceRecoState.sendEmptyMessage(MSG_VOICE_RECO_END);
            }else{
                mHdrVoiceRecoState.sendEmptyMessage(MSG_VOICE_RECO_STOP);
                mBoolVoiceRecoStarted = false;
            }

//            TextView textView = textView = (TextView) findViewById(R.id.textView);

            String key= "";
            key = SpeechRecognizer.RESULTS_RECOGNITION;
            ArrayList<String> mResult = results.getStringArrayList(key);
            String[] rs = new String[mResult.size()];
            mResult.toArray(rs);

            textView.setText("" + rs[0]);
            final String test = rs[0];
            try{
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        EditText input_text = (EditText) findViewById(R.id.input_text);

                        socketClass[0].send(input_text.getText()+"::"+test);
                        Log.d("onResults","onResults Socket send  befor");
                    }
                }).start();


            }catch (Exception e){
                Log.d("onResults","onResults Socket send  : "+e);
            }

            //mRecognizer.startListening(i);
        }

        @Override
        public void onPartialResults(Bundle partialResults) {
        }

        @Override
        public void onEvent(int eventType, Bundle params) {
        }
    };
}
