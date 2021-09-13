package com.example.vizbuzz.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentTransaction
import androidx.recyclerview.widget.RecyclerView
import com.example.vizbuzz.R
import com.example.vizbuzz.fragments.PodcastDetailsFragment
import com.example.vizbuzz.models.Podcast

class PodcastsAdapter(private val fragment: Fragment, private val podcasts: MutableList<Podcast>): RecyclerView.Adapter<PodcastsAdapter.ViewHolder>() {
    private val context: Context? = fragment.context
    private val DETAILS_TAG = "PodcastDetailsFragment"

    inner class ViewHolder(itemView: View): RecyclerView.ViewHolder(itemView) {
        private val podcastTitle: TextView = itemView.findViewById(R.id.name)
        fun bind(podcast: Podcast) {
            podcastTitle.text = podcast.name
            itemView.setOnClickListener {
                val detailsFragment = PodcastDetailsFragment.newInstance(podcast)
                val ft: FragmentTransaction? = fragment.fragmentManager?.beginTransaction()
                ft?.replace(R.id.flContainer, detailsFragment, DETAILS_TAG)
                ft?.addToBackStack(null)
                ft?.commit()
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.podcast_layout, parent, false)
        return ViewHolder(view)
    }

    override fun getItemCount(): Int {
        return podcasts.size
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val podcast = podcasts[position]
        holder.bind(podcast)
    }

    fun addAll(newPods: List<Podcast>?) {
        if (newPods != null) {
            podcasts.addAll(newPods)
        }
        notifyDataSetChanged()
    }
}