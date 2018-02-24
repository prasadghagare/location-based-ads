package com.example.sushilpatil.locationbasedads;

import android.Manifest;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Handler;
import android.provider.MediaStore;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.android.volley.VolleyError;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.googlecode.tesseract.android.TessBaseAPI;

import org.json.JSONObject;
import android.location.Location;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static android.app.Activity.RESULT_OK;


public class MainActivity extends AppCompatActivity {
    private TextView mUsernameView;
    private TextView mServerIp;
    private TextView mEmailId;
    private TextView mComments;

    private View mProgressView;

    private EditText mLocationX;
    private EditText mLocationY;

    private EditText mRadius;

    private String Username;
    private String ServerIP;
    private String EmailId;
    private FusedLocationProviderClient mFusedLocationClient;
    private String location_x="0";
    private String location_y="0";
    private int PICK_IMAGE_REQUEST = 1;

    //Tesseract
    Bitmap image; //our image
    public TessBaseAPI mTess; //Tess API reference

    String datapath = ""; //path to folder containing language data file

    private ProgressBar mProgressBar;



    public TessBaseAPI getmTess() {
        return mTess;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mProgressBar =(ProgressBar) findViewById(R.id.main_progress);


        Button mUploadBill = (Button) findViewById(R.id.UploadBill);
        Button mSendLocation = (Button) findViewById(R.id.SendLocation);

        mUsernameView =(TextView)findViewById(R.id.username);
        mServerIp = (TextView)findViewById(R.id.serverip);
        mEmailId =(TextView)findViewById(R.id.emailid);
        mComments=(TextView)findViewById(R.id.comments);

        mLocationX =(EditText) findViewById(R.id.location_x);
        mLocationY =(EditText) findViewById(R.id.location_y);

        mRadius=(EditText)findViewById(R.id.radius);

        Bundle bundle = getIntent().getExtras();

        Username = bundle.getString("username");
        ServerIP = bundle.getString("serverip");
        EmailId = bundle.getString("emailid");

        //Extract the data…
        mUsernameView.setText(Username);
        mServerIp.setText(ServerIP);
        mEmailId.setText(EmailId);

        //Location
        final  int MY_PERMISSION_ACCESS_COURSE_LOCATION = 11;

        if ( ContextCompat.checkSelfPermission( this, android.Manifest.permission.ACCESS_COARSE_LOCATION ) != PackageManager.PERMISSION_GRANTED ) {

            ActivityCompat.requestPermissions( this, new String[] {  android.Manifest.permission.ACCESS_COARSE_LOCATION  },
                    MY_PERMISSION_ACCESS_COURSE_LOCATION );
        }

        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);

        mFusedLocationClient.getLastLocation().addOnSuccessListener(MainActivity.this, new OnSuccessListener<Location>() {
            @Override
            public void onSuccess(Location location) {
                if (location != null) {
                    location_x=Double.toString(location.getLatitude());
                    location_y=Double.toString(location.getLongitude());

                    mLocationX.setText(location_x);
                    mLocationY.setText(location_y);

                }

            }
        });

        datapath = getFilesDir()+ "/tesseract/";

        System.out.println("Datapath"+datapath);

        //make sure training data has been copied
        checkFile(new File(datapath + "tessdata/"));

        //initialize Tesseract API
        String lang = "eng";
        mTess = new TessBaseAPI();
        mTess.init(datapath, lang);
        // Buttons

        mUploadBill.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {


                Intent intent = new Intent();
                // Show only images, no videos or anything else
                intent.setType("image/*");
                intent.setAction(Intent.ACTION_GET_CONTENT);


                Bundle b=new Bundle();
                b.putString("datapath",datapath);
                intent.putExtras(b);
                // Always show the chooser (if there are multiple options available)
                startActivityForResult(Intent.createChooser(intent, "Select Picture"), PICK_IMAGE_REQUEST);








            }
        });


        // Send location data

        mSendLocation.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                /* Example API call
               New API http://localhost:5000/sendlocation?location_x=10.2&location_y=31.3&username=sushilpatil&radius=2&count=100&emailid=sushil21patil@gmail.com
                 */
                //Get Location
                location_x=mLocationX.getText().toString();
                location_y=mLocationY.getText().toString();
                String radius=mRadius.getText().toString();

                String count="200"; //;TODO This is top 200 user ocr list , Can be used to limit offers that the user gets.

                String u = String.format("http://%s:5000/sendlocation?location_x=%s&location_y=%s&username=%s&radius=%s&count=%s&emailid=%s",ServerIP,location_x,location_y,Username,radius,count,EmailId);

                SendData(u);

                Toast.makeText(MainActivity.this,"Wait for server response",Toast.LENGTH_SHORT).show();
            }
        });

    }

    public void SendData(String url){

        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(this);

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 50 characters of the response string.
                        Toast.makeText(MainActivity.this,response,Toast.LENGTH_LONG).show();
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(MainActivity.this,"Failed. Network Error",Toast.LENGTH_LONG).show();
            }
        });
    // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }


    public String RequestData(String urlString){

        try {
            URL url = new URL(urlString);

            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            try {

                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                StringBuilder stringBuilder = new StringBuilder();
                String line;
                while ((line = bufferedReader.readLine()) != null) {
                    stringBuilder.append(line).append("\n");
                }
                bufferedReader.close();
                return stringBuilder.toString();
            }
            finally{
                urlConnection.disconnect();
            }
        }
        catch(Exception e) {
            Log.e("ERROR", e.getMessage(), e);
            return null;
        }
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        mProgressBar.setVisibility(View.VISIBLE);

        if (requestCode == PICK_IMAGE_REQUEST && resultCode == RESULT_OK && data != null && data.getData() != null) {

            Uri uri = data.getData();

            try {


                Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), uri);

                /*
                TODO; DO this once you figure how to send data over intents  using onactivity Result
                 */
                /*
                Bundle b2= data.getExtras();
                String dp= b2.getString("datapath");

                MyTaskParams taskParams= new MyTaskParams();
                taskParams.setDatapath(dp);

                taskParams.setImage(bitmap);



                */

                //Too slow Let me test with dapath = /data/user/0/com.example.sushilpatil.locationbasedads/files/tesseract/
                /*mProgressBar.setProgress(25);
                String OCRresult = null;
                mTess.setImage(bitmap);
                OCRresult = mTess.getUTF8Text();
                System.out.println(OCRresult);

                */





                new DoOCR().execute(bitmap);


                // Log.d(TAG, String.valueOf(bitmap));
                //init image
                //image = BitmapFactory.decodeResource(getResources(), R.drawable.test_image);




            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


    public JSONObject getOCRResults(List<String> s){



        JSONObject obj = new JSONObject();
        try {

            for (String element : s) {

                if (obj.has(element)){
                    System.out.println("JSONObject - Key "+element+" exists, incrementing");
                    int prevCount=(int)obj.get(element);
                    int newCount= prevCount++;

                    obj.remove(element);
                    obj.put(element,newCount);
                }
                else{
                    obj.put(element,1);
                }

            }



        } catch (Exception e){
            System.out.println("Error JSON "+e);
        }
        return obj;

    }

    private void copyFiles() {
        try {
            //location we want the file to be at
            String filepath = datapath + "/tessdata/eng.traineddata";

            //get access to AssetManager
            AssetManager assetManager = getAssets();


            //open byte streams for reading/writing
            InputStream instream = assetManager.open("tessdata/eng.traineddata");
            OutputStream outstream = new FileOutputStream(filepath);

            //copy the file to the location specified by filepath
            byte[] buffer = new byte[1024];
            int read;
            while ((read = instream.read(buffer)) != -1) {
                outstream.write(buffer, 0, read);
            }
            outstream.flush();
            outstream.close();
            instream.close();

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void checkFile(File dir) {
        //directory does not exist, but we can successfully create it
        if (!dir.exists()&& dir.mkdirs()){
            copyFiles();
        }
        //The directory exists, but there is no data file in it
        if(dir.exists()) {
            String datafilepath = datapath+ "/tessdata/eng.traineddata";
            File datafile = new File(datafilepath);
            if (!datafile.exists()) {
                copyFiles();
            }
        }
    }

    private class DoOCR extends AsyncTask<Bitmap, String, Void> {



        @Override
        protected Void doInBackground(Bitmap... params) {

            TessBaseAPI mTess = new TessBaseAPI();
            String lang = "eng";

            //TODO; I can replace this with the actual datapath

            mTess.init("/data/user/0/com.example.sushilpatil.locationbasedads/files/tesseract/", lang);

            String OCRresult = null;
            mTess.setImage(params[0]);
            OCRresult = mTess.getUTF8Text();


            publishProgress("OCR Done.. Requesting Valid item list");
            // String[] ocrsplit = OCRresult.split("\\s+"); // Regex for all spaces
            String[] ocrsplit = OCRresult.split(" ");
            String[] validItems=RequestData("http://"+ServerIP+":5000/getitemlist").split(",");


            publishProgress("Request Done.. Finding Common list");
            List<String> commonList= findCommonElements(ocrsplit,validItems);

            System.out.println("Split original");

            System.out.println(Arrays.toString(ocrsplit));

            System.out.println("Valid list");

            System.out.println(Arrays.toString(validItems));

            System.out.println("Common list");
            System.out.println(commonList);







            mProgressBar.setProgress(50);

            if(commonList.isEmpty()){
                publishProgress("No valid items. Not sending a network request");

            }
            else
            {
                publishProgress("Sending network request");
                JSONObject newOCRResults = getOCRResults(commonList);
                String u = String.format("http://%s:5000/uploadbill?billdetails=%s&username=%s", ServerIP, newOCRResults.toString(), Username);
                SendData(u);
                //Toast.makeText(MainActivity.this,"Wait for server response",Toast.LENGTH_SHORT).show();
                publishProgress("Send complete");
            }

            return null;
        }


        protected void onProgressUpdate(String... progress) {
            mComments.setText(progress[0]);
        }


        @Override
        protected void onPostExecute(Void result) {

            mProgressBar.setProgress(100);
            mProgressBar.setVisibility(View.GONE);



        }
    }

    public List<String> findCommonElements(String[] a, String[] b){



        List<String> commonElements = new ArrayList<String>();

        for(int i = 0; i < a.length ;i++) {
            for(int j = 0; j< b.length ; j++) {
                System.out.println("Checking "+a[i].toLowerCase().trim() +" AND "+ b[j].toLowerCase().trim());

                if(a[i].toLowerCase().trim() == b[j].toLowerCase().trim()) {
                    //Check if the list already contains the common element
                    if(!commonElements.contains(a[i].toLowerCase().trim())) {
                        //add the common element into the list
                        commonElements.add(a[i].toLowerCase().trim());
                    }
                }
            }
        }
        return commonElements;


    }

}

  class MyTaskParams {


    Bitmap image;
    String datapath;

    MyTaskParams(){

    }

    MyTaskParams( String datapath, Bitmap image) {

       this.datapath=datapath;
       this.image=image;
    }

      public Bitmap getImage() {
          return image;
      }

      public String getDatapath() {
          return datapath;
      }

      public void setDatapath(String datapath) {
          this.datapath = datapath;
      }

      public void setImage(Bitmap image) {
          this.image = image;
      }

  }


