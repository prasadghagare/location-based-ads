package com.example.sushilpatil.locationbasedads;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
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

import org.json.JSONObject;
import android.location.Location;







public class MainActivity extends AppCompatActivity {
    private TextView mUsernameView;
    private TextView mServerIp;
    private TextView mEmailId;

    private TextView mLocationX;
    private TextView mLocationY;

    private String Username;
    private String ServerIP;
    private String EmailId;
    private FusedLocationProviderClient mFusedLocationClient;
    private String location_x="0";
    private String location_y="0";




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);




        Button mUploadBill = (Button) findViewById(R.id.UploadBill);
        Button mSendLocation = (Button) findViewById(R.id.SendLocation);

        mUsernameView =(TextView)findViewById(R.id.username);
        mServerIp = (TextView)findViewById(R.id.serverip);
        mEmailId =(TextView)findViewById(R.id.emailid);

        mLocationX =(TextView)findViewById(R.id.location_x);
        mLocationY =(TextView)findViewById(R.id.location_y);

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


        // Buttons

        mUploadBill.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {




                JSONObject obj = new JSONObject();
                try {

                    obj.put("bananas",4);
                    obj.put("bread",2);


                } catch (Exception e){
                    System.out.println("Error JSON "+e);
                }



                String u = String.format("http://%s:5000/uploadbill?billdetails=%s&username=sushilpatil",ServerIP,obj.toString());

                SendData(u,"data");

                Toast.makeText(MainActivity.this,"Sent Successfully",Toast.LENGTH_SHORT).show();
                /*Intent mainActivityIntent = new Intent(LoginActivity.this, MainActivity.class);
                startActivity(mainActivityIntent);
                Toast.makeText(LoginActivity.this,"Signed in successfully",Toast.LENGTH_SHORT).show();
                */



            }
        });

        // Send location data

        mSendLocation.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {


                /* Example API call
                http://localhost:5000/sendlocation?location_x=10.2&location_y=31.3&username=sushilpatil&radius=2
                 */
                //Get Location







                String radius="2";


                String u = String.format("http://%s:5000/sendlocation?location_x=%s&location_y=%s&username=sushilpatil&radius=%s",ServerIP,location_x,location_y,radius);

                SendData(u,"data");

                Toast.makeText(MainActivity.this,"Sent Successfully",Toast.LENGTH_SHORT).show();
                /*Intent mainActivityIntent = new Intent(LoginActivity.this, MainActivity.class);
                startActivity(mainActivityIntent);
                Toast.makeText(LoginActivity.this,"Signed in successfully",Toast.LENGTH_SHORT).show();
                */



            }
        });



    }

    public void SendData(String url, String data){

        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(this);

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 50 characters of the response string.
                        Toast.makeText(MainActivity.this,response,Toast.LENGTH_SHORT).show();
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(MainActivity.this,"Failed. Network Error",Toast.LENGTH_SHORT).show();
            }
        });
    // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }



}
