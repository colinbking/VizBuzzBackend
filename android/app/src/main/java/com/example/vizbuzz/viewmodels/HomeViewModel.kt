package com.example.vizbuzz.viewmodels

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.vizbuzz.models.Podcast
import com.example.vizbuzz.repository.Repository

class HomeViewModel(application: Application) : AndroidViewModel(application) {
    private var allPodcasts: MutableLiveData<List<Podcast>> = MutableLiveData<List<Podcast>>()
    private val TAG = "HomeViewModel"

    private val repository = Repository()

    fun allPodcasts(): LiveData<List<Podcast>>? = allPodcasts

    /* Get podcasts from server and post them in allPodcasts live data */
    fun getPodcasts() {
        Log.i(TAG, "In get podcasts")
        // TODO add error handling
        allPodcasts.postValue(repository.queryPodcasts())
    }
}
