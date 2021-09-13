package com.example.vizbuzz.models

class Podcast() {
    var name: String? = null
    var transcript: String? = null

    companion object {
        @JvmStatic
        fun newInstance(title: String?, trans: String?): Podcast {
            val newPodcast = Podcast();
            newPodcast.name = title
            newPodcast.transcript = trans
            return newPodcast
        }
    }
}