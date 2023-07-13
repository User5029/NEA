using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AudioPeer : MonoBehaviour
{
    // Start is called before the first frame update
    public AudioSource _audio;
    public static float[] _samples = new float[512];


    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        GetSpectrumAudioSource();
    }

    void GetSpectrumAudioSource()
    {
        _audio.GetSpectrumData(_samples,0, FFTWindow.Blackman);
    }
}
