using System.Collections;
using UnityEngine;

namespace UnityCore
{
    namespace Audio
    {
        public class SongNAudio : MonoBehaviour
        {
            public string path = "";
            private string oldPath = "";
            public AudioSource aud;


            private void Update()
            {
                if (path != oldPath)
                {
                    Debug.Log("Received Audio");
                    if(aud == null)
                    {
                        Debug.LogWarning("Cannot access audioSource");
                        return;
                    };

                    StartCoroutine(LoadSongCoroutine());
                    oldPath = path;
                }
                if (Input.GetKeyDown(KeyCode.B))
                {
                    aud.Play();
                };
                if (Input.GetKeyDown(KeyCode.N))
                {
                    aud.Stop();
                }
            }
            private IEnumerator LoadSongCoroutine()
            {
                string url = string.Format("file://{0}", path);
                #pragma warning disable
                WWW www = new WWW(url);
                yield return www;

                aud.clip = NAudioPlayer.FromMp3Data(www.bytes);
                Debug.Log("Audio Armed");
            }
        }
    }
}
