package com.example.vizbuzz.fragments

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.vizbuzz.R
import com.example.vizbuzz.adapter.PodcastsAdapter
import com.example.vizbuzz.models.Podcast
import com.example.vizbuzz.viewmodels.HomeViewModel

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
    private var viewModel: HomeViewModel? = null
    private var podcastsReceived: Int = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.i(TAG, "On create")

        arguments?.let {
            param1 = it.getString(ARG_PARAM1)
        }


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

        // Getting the view model this way makes it so the view model lives even if the fragment dies.
        viewModel = ViewModelProviders.of(this).get(HomeViewModel::class.java)
        val podcastsObserver: Observer<List<Podcast>> = Observer<List<Podcast>> { pods ->
            Log.i(TAG, "List of podcasts received")
            if (podcastsReceived == 0) {

                podcastsReceived = 1
                adapter?.addAll(pods)
            }

        }
        viewModel?.allPodcasts()?.observe(viewLifecycleOwner, podcastsObserver)
        initializeRvPodcasts()
        viewModel?.getPodcasts()
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