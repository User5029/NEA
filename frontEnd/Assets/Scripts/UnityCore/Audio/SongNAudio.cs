using System.Collections;
using UnityEngine;

namespace UnityCore
{
    namespace Audio
    {
        public class SongNAudio : MonoBehaviour
        {
            public string path = "";
            //private string oldPath = "";
            public string toSet = "0";
            public bool done = false;
            public AudioSource aud1;
            public AudioSource aud2;
            public AudioManager audioManager;


            private void Start()
            {
                aud1 = GameObject.FindGameObjectWithTag("audio1").GetComponentsInChildren<AudioSource>()[0];
                aud2 = GameObject.FindGameObjectWithTag("audio2").GetComponentsInChildren<AudioSource>()[0];
            }
            private void Update()
            {
                if (path != "")
                {
                    if (toSet == "1")
                    {
                        StartCoroutine(LoadSongCoroutine(aud1, toSet));
                        path = "";
                        toSet = "0";
                    }
                    if(toSet == "2")
                    {
                        StartCoroutine(LoadSongCoroutine(aud2, toSet));
                        path = "";
                        toSet = "0";
                    }
                }
            }
            private IEnumerator LoadSongCoroutine(AudioSource aud, string num)
            {
                string url = string.Format("file://{0}", path);
                #pragma warning disable
                WWW www = new WWW(url);
                yield return www;

                string extension = System.IO.Path.GetExtension(url.ToString());

                if(extension == ".wav")
                {
                    Debug.Log("wav");
                    aud.clip = www.GetAudioClip();
                    done = true;
                    Debug.Log("Audio Armed");
                }
                if (extension == ".mp3")
                {
                    Debug.Log("mp3");
                    aud.clip = NAudioPlayer.FromMp3Data(www.bytes);

                    if (num == "1")
                    {
                        AudioManager.Aud1_Length = aud.clip.length;
                    } else if (num == "2")
                    {
                        AudioManager.Aud2_Length = aud.clip.length;
                    }
                    done = true;
                    Debug.Log("Audio Armed.");
                }

            }
        }
    }
}
