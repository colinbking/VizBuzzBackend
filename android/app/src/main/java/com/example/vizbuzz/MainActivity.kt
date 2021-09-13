package com.example.vizbuzz

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.FragmentTransaction
import com.example.vizbuzz.fragments.HomeFragment

class MainActivity : AppCompatActivity() {
    private val HOME_TAG = "HomeFragment"
    private val TAG = "MainActivity"
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.i(TAG, "On create")
        setContentView(R.layout.activity_main)

        val homeFrag = HomeFragment.newInstance()
        val ft: FragmentTransaction = supportFragmentManager.beginTransaction()
        ft.add(R.id.flContainer, homeFrag, HOME_TAG)
        ft.addToBackStack(null)
        ft.commit()

    }
}