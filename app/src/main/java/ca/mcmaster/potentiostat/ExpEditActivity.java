package ca.mcmaster.potentiostat;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import android.util.Log;
import android.view.MenuItem;
import android.widget.Toast;

import ca.mcmaster.waterqualitymonitorsuite.R;


public class ExpEditActivity extends AppCompatActivity {
    private static final String TAG = ExpEditActivity.class.getSimpleName();

    private String expName;
    private Boolean editMode;
    //GUI elements


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_experiment_edit);

        //Get intent and extras
        final Intent intent = getIntent();
        expName = intent.getStringExtra(ExpSelectActivity.EXTRAS_EXP_NAME);
        editMode = intent.getBooleanExtra(ExpSelectActivity.EXTRAS_EDIT_MODE, false);

        if (getSupportActionBar()!=null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            if(editMode){
                if(expName!=null){
                    getSupportActionBar().setTitle(R.string.title_edit_exp);
                    getSupportActionBar().setSubtitle(expName);
                } else {
                    Log.e(TAG, "onCreate: Experiment name should not be null");
                    finish();
                }
            } else {
                getSupportActionBar().setTitle(R.string.title_new_exp);
            }
        } else {
            Log.e(TAG, "onCreate: Action support bar should not be null");
            finish();
        }
        if (editMode)
            showMessage("oh hai mark");
        else
            showMessage("oh, bai mark");

    }

    public boolean onOptionsItemSelected(MenuItem item) {
        switch(item.getItemId()) {
            case android.R.id.home:
                onBackPressed();
                return true;
        }
        return super.onOptionsItemSelected(item);
    }

    void showMessage(String s){
        Toast.makeText(this, s, Toast.LENGTH_LONG).show();
    }
    


}
