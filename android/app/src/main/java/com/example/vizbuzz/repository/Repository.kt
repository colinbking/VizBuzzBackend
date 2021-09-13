package com.example.vizbuzz.repository

import com.example.vizbuzz.models.Podcast

class Repository {

    /* Query the server to get podcasts and their details */
    fun queryPodcasts(): List<Podcast> {
        // TODO: Query server to get podcasts and their details in JSON format then convert
        var pods = ArrayList<Podcast>()
        pods.add(Podcast.newInstance("Podcast 1", "Podcast 1 Transcript: Hello World!"))
        pods.add(Podcast.newInstance("Podcast 2", "Podcast 2 Transcript: Hello World!"))
        pods.add(Podcast.newInstance("Podcast 3", "Podcast 3 Transcript: Hello World!"))
        return pods
    }
}