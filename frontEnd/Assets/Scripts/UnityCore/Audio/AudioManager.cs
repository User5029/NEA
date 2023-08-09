using System.Collections;
using Unity.Burst.Intrinsics;
using UnityEngine;


namespace UnityCore
{
    namespace Audio
    {
        public class AudioManager : MonoBehaviour
        {
            private static AudioManager instance = null;
            public static AudioManager Instance;

            #region variables

            // Public Variables
            public static AudioSource audio1;
            public static AudioSource audio2;
            public bool Developer;

            public enum AudioStates
            {
                Disabled,   // Cannot be used
                Manual,     // User has control
                Automatic   // User does not have control except for (reduced, abort button, stop)
            }
            public enum AudioSubStates
            {
                Disarmed,   // No audio is selected (uses a local empty audio clip)
                Arming,     // Audio requested to be loaded and is being processed
                Armed,      // Audio is loaded and the play button is now able to be used
                WaitingIn,  // Song is on pre-wait
                FadeIn,     // If song has a crossfade or gradual volume increase (can be used by the user aswell)
                Playing,    // Song is playing normally
                Looping,    // Song is looping
                Reduced,    // Song has been reduced volume but is still playing
                Paused,     // Song has been stopped but not cleared
                Warning,    // Song is close to finishing (~20seconds TBD)
                FadeOut,    // Song is fading out (user, auto)
                WaitingOut, // Song is on post-wait
                Stopped,    // Song has been stopped by the user or panic has been pressed
                Ended,      // Song has finished naturally and can trigger next audio if AudioState = automatic on other audio source.
                Disarming   // Audio source is being disarmed
            }

            public static AudioStates Aud1_State = AudioStates.Disabled;
            public static AudioSubStates Aud1_SubState = AudioSubStates.Disarmed;
            public static AudioStates Aud2_State = AudioStates.Disabled;
            public static AudioSubStates Aud2_SubState = AudioSubStates.Disarmed;

            public static int Aud1_Cue = 0;
            public static string Aud1_Name = "None";
            public static int Aud2_Cue = 0;
            public static string Aud2_Name = "None";
            public static int CurrentCue = 0;

            // Private Variables
            private string[] Aud1_Data;
            private string[] Aud2_Data;


            #endregion

            #region Unity Functions
            private void Awake()
            {
                if (instance != null && instance != this)
                {
                    Destroy(this.gameObject);
                    return;
                }
                else
                {
                    instance = this;
                }
                DontDestroyOnLoad(this.gameObject);

                audio1 = GameObject.FindGameObjectWithTag("audio1").GetComponentsInChildren<AudioSource>()[0];
                audio2 = GameObject.FindGameObjectWithTag("audio2").GetComponentsInChildren<AudioSource>()[0];

                if (audio1 == null)
                {
                    LogError("Error getting Audio Source #1");
                    return;
                }
                if (audio2 == null)
                {
                    LogError("Error getting Audio Source #2");
                    return;
                }

                Disarm("0,1,2,3,ALL".Split(","));
            }


            private void Start()
            {
                Log("Setting Audio Sources to Manual.");
                Aud1_State = AudioStates.Manual;
                Aud2_State = AudioStates.Manual;

                string msg = "to,from,audio,arm,1,1,c:/music/test.mp3";
                string[] data = msg.Split(char.Parse(","));
                Arm(data);

            }

            private void Update()
            {
                if (Input.GetKeyDown(KeyCode.B))
                {
                    audio1.Play();
                }
                if (Input.GetKeyDown(KeyCode.N))
                {
                    audio1.Pause();
                }
                if (Input.GetKeyDown(KeyCode.M))
                {
                    audio1.Stop();
                }
                if (Input.GetKeyDown(KeyCode.C))
                {
                    instance.StartCoroutine(FadeOutCo(audio1, 5f));
                }
                if (Input.GetKeyDown(KeyCode.V))
                {
                    instance.StartCoroutine(FadeInCo(audio1, 5f));
                }
            }
            #endregion

            #region Audio Functions

            public static void Disarm(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.clip = Resources.Load("blank_audio") as AudioClip;
                        Aud1_SubState = AudioSubStates.Disarmed;
                        Aud1_Name = "None";
                        break;
                    case "2":
                        audio2.clip = Resources.Load("blank_audio") as AudioClip;
                        Aud2_SubState = AudioSubStates.Disarmed;
                        Aud2_Name = "None";
                        break;
                    case "ALL":
                        audio1.clip = Resources.Load("blank_audio") as AudioClip;
                        audio2.clip = Resources.Load("blank_audio") as AudioClip;
                        Aud1_SubState = AudioSubStates.Disarmed;
                        Aud1_Name = "None";
                        Aud2_SubState = AudioSubStates.Disarmed;
                        Aud2_Name = "None";
                        break;
                }
            }

            public static void Play(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.volume = 1;
                        audio1.Play();
                        Aud1_SubState = AudioSubStates.Playing;
                        break;
                    case "2":
                        audio2.volume = 1;
                        audio2.Play();
                        Aud1_SubState = AudioSubStates.Playing;
                        break;
                }
            }

            public static void Pause(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.Pause();
                        break;
                    case "2":
                        audio2.Pause();
                        break;
                    case "ALL":
                        audio1.Pause();
                        audio2.Pause();
                        break;
                }
            }

            public static void Stop(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.Stop();
                        break;
                    case "2":
                        audio2.Stop();
                        break;
                    case "ALL":
                        audio1.Stop();
                        audio2.Stop();
                        break;
                }
            }

            public static IEnumerator FadeInCo(AudioSource audioSource, float FadeTime)
            {
                audioSource.volume = 0.1f;

                audioSource.Play();
                while (audioSource.volume < 1)
                {
                    //audioSource.volume += startVolume * Time.deltaTime / FadeTime;
                    audioSource.volume += 1 * Time.deltaTime / FadeTime;

                    yield return null;
                }
            }
            public static void FadeIn(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.Play();
                        break;
                    case "2":
                        audio2.Play();
                        break;
                }
            }


            public static IEnumerator FadeOutCo(AudioSource audioSource, float FadeTime)
            {
                float startVolume = audioSource.volume;

                while (audioSource.volume > 0)
                {
                    audioSource.volume -= startVolume * Time.deltaTime / FadeTime;

                    yield return null;
                }

                audioSource.Stop();
                audioSource.volume = startVolume;
            }
            public static void FadeOut(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        instance.StartCoroutine(FadeOutCo(audio1, float.Parse(_cmd[5])));
                        break;
                    case "2":
                        instance.StartCoroutine(FadeOutCo(audio2, float.Parse(_cmd[5])));
                        break;
                }
            }

            public static void Reduce(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.Play();
                        break;
                    case "2":
                        audio2.Play();
                        break;
                }
            }

            public static void Normal(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.Play();
                        break;
                    case "2":
                        audio2.Play();
                        break;
                }
            }

            private static IEnumerator Arm_LoadSong(AudioSource _audiosource, string path)
            {
                string url = string.Format("file://{0}", path);
#pragma warning disable
                WWW www = new WWW(url);
                yield return www;

                _audiosource.clip = NAudioPlayer.FromMp3Data(www.bytes);
                yield return "true";
            }

            public static void Arm(string[] _cmd)
            {
                /*
                    cmd[4] - channel                // Default: none,   !: return
                    cmd[5] - cue #                  // Default: none,   !: return
                    cnd[6] - cue name               // Default: none,   !: song url
                    cmd[7] - song url               // Default: none,   !: return
                    cmd[8] - prewait                // Default: 0,      !: (Default)
                    cmd[9] - fadein                 // Default: 0,      !: (Default)
                    cmd[10] - fadeout                // Default: 2,      !: (Default)
                    cmd[11] - postwait              // Default: 1,      !: (Default)
                */

                string _build;

                // there is no cmd[4] cmd[5] cmd[6]
                if (_cmd.Length < 7)
                {
                    return;
                }
                else
                {
                    switch (_cmd[4])
                    {
                        case "1":
                            Aud1_SubState = AudioSubStates.Arming;
                            LogStatic(Aud1_SubState.ToString());
                            Aud1_Cue = int.Parse(_cmd[5]);
                            instance.StartCoroutine(Arm_LoadSong(audio1, _cmd[6]));
                            Aud1_SubState = AudioSubStates.Armed;
                            LogStatic(Aud1_SubState.ToString());
                            break;
                    }
                }


            }






            #endregion


            #region DEBUG
            private void Log(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.Log("[AudManager] - " + _msg);
            }
            private static void LogStatic(string _msg)
            {
                Debug.Log("[AudManager] - " + _msg);
            }
            private void LogWarn(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.LogWarning("[AudManager] - " + _msg);
            }
            private void LogError(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.LogError("[AudManager] - " + _msg);
            }
            #endregion
        }
    }
}