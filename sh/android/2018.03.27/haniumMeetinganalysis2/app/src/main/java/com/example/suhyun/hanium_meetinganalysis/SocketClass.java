package com.example.suhyun.hanium_meetinganalysis;

import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

/**
 * Created by Suhyun on 2018-03-20.
 */


import android.util.Log;

import java.io.*;
import java.net.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

/**
 * 소켓 통신 문자열 송수신 유틸
 *
 * @author jsh
 */
public class SocketClass {
    private Socket socket;
    private OutputStream out;
    private InputStream in;

    public SocketClass() {
    }

    /**
     * 소켓 생성과 동시에 생성 SocketSR socketSR = new SocketSR(new Socket(주소, 포트)); 소켓
     * close할땐 socket을 close하지말고 이 객체를 close해야함
     *
     * @param socket
     */
    public SocketClass(Socket socket) {
        try {
            this.socket = socket;
            this.in = this.socket.getInputStream();
            this.out = this.socket.getOutputStream();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 문자열 수신 사용법 String input = socketSR.recv();
     *
     * @return null 이면 실패!
     */
    public String recv() {
        String result = "";
        try {
            int size = this.in.read();
            if (size == -1) {
                return null;
            } else if (size == 0) {
                return "";
            }
            byte[] tempBuffer = new byte[5];

            do {
                if (this.in.read(tempBuffer) <= 0) break;
                size = size - 5;
                String temp = (new String(tempBuffer));
                if ((int) temp.charAt(0) == 0) {
                    System.out.println("first is 0!!!!");
                    size = size + 5;
                    continue;
                }
                result += temp;
                tempBuffer = new byte[5];
            } while (size > 0);

            System.out.println("[recv] : " + result);
            return result;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * 문자열 전송 사용법 send(string) 빈문자열 전송시 빈칸하나 전송됨.
     *
     * @return true, false
     */
    public Boolean send(String str) {
        try {
            Log.d("send","send fuction in str : "+ str);
//            if (str.length() == 0)
//                str = " ";
//            byte[] buff = (str).getBytes();
//            this.out.write(buff.length);

            OutputStreamWriter writer = new OutputStreamWriter(socket.getOutputStream(),StandardCharsets.UTF_8);

            writer.write(str);
            writer.flush();

//            OutputStream os = this.socket.getOutputStream();
//            Log.d("send","send fuction in str 1: "+ str);
//            OutputStreamWriter osw = new OutputStreamWriter(os, StandardCharsets.UTF_8);
//            Log.d("send","send fuction in str 2: "+ str);
//            PrintWriter pw = new PrintWriter(osw);
//            Log.d("send","send fuction in str3 : "+ str);
//            pw.println(test.getBytes("UTF-8"));

//            pw.flush();
//            pw.close();
//            this.out.flush();
//            System.out.println(str);
            return true;
        } catch (Exception e) {
            Log.d("send","send fuction in str -- faile : "+ str+e);
            return false;
        }
    }

    /**
     * 소켓 닫을때 이걸로 닫음
     *
     * @return
     */
    public Boolean close() {
        Log.d("send","send fuction in str -- close : ");
        try {
            this.in.close();
            this.out.close();
            this.socket.close();
            return true;
        } catch (Exception e) {
            return false;
        }
    }

}