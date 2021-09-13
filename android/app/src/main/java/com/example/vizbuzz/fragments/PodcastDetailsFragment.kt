package com.example.vizbuzz.fragments

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import com.example.vizbuzz.R
import com.example.vizbuzz.models.Podcast

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val PODCAST_NAME = "podname"
private const val PODCAST_TRANSCRIPT = "podtrans"

/**
 * A simple [Fragment] subclass.
 * Use the [PodcastDetailsFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class PodcastDetailsFragment : Fragment() {
    // TODO: Rename and change types of parameters
    private var podcastName: String? = null
    private var podcastTranscript: String? = null
    private var title: TextView? = null
    private var transcript: TextView? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            podcastName = it.getString(PODCAST_NAME)
            podcastTranscript = it.getString(PODCAST_TRANSCRIPT)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_podcast_details, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        title = view.findViewById(R.id.title)
        transcript = view.findViewById(R.id.transcript)
        title?.text = podcastName
        transcript?.text = podcastTranscript
    }

    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment PodcastDetailsFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(podcast: Podcast) =
            PodcastDetailsFragment().apply {
                arguments = Bundle().apply {
                    putString(PODCAST_NAME, podcast.name)
                    putString(PODCAST_TRANSCRIPT, podcast.transcript)
                }
            }
    }
}