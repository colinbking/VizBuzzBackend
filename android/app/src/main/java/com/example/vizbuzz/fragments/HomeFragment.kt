package com.example.vizbuzz.fragments

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.vizbuzz.R
import com.example.vizbuzz.adapter.PodcastsAdapter
import com.example.vizbuzz.models.Podcast

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [HomeFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class HomeFragment : Fragment() {
    private var param1: String? = null
    private val TAG = "HomeFragment"
    private var rvPodcasts: RecyclerView? = null
    private var adapterPodcasts: ArrayList<Podcast> = ArrayList()
    private var adapter: PodcastsAdapter? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.i(TAG, "On create")

        arguments?.let {
            param1 = it.getString(ARG_PARAM1)
        }
        adapterPodcasts.add(Podcast.newInstance("Podcast 1", "Podcast 1 Transcript: Hello World!"))
        adapterPodcasts.add(Podcast.newInstance("Podcast 2", "Podcast 2 Transcript: Hello World!"))
        adapterPodcasts.add(Podcast.newInstance("Podcast 3", "Podcast 3 Transcript: Hello World!"))

    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        rvPodcasts = view.findViewById(R.id.rvPodcasts)
        initializeRvPodcasts()
    }

    private fun initializeRvPodcasts() {
        adapter = PodcastsAdapter(this, adapterPodcasts)
        rvPodcasts?.adapter = adapter

        // Set recyclerview layoutmanager
        val layoutManager = LinearLayoutManager(context)
        rvPodcasts?.layoutManager = layoutManager

        // Add lines between recycler view
        val itemDecoration: RecyclerView.ItemDecoration = DividerItemDecoration(context, DividerItemDecoration.VERTICAL)
        rvPodcasts?.addItemDecoration(itemDecoration)
    }

    companion object {
        @JvmStatic
        fun newInstance() = HomeFragment()
    }
}