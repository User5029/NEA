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
            public AudioSource audio1;
            public AudioSource audio2;
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
                Reduced,    // Song has been reduced volume but is still playing
                Warning,    // Song is close to finishing (~20seconds TBD)
                FadeOut,    // Song is fading out (user, auto)
                WaitingOut, // Song is on post-wait
                Stopped,    // Song has been stopped by the user or panic has been pressed
                Ended,      // Song has finished naturally and can trigger next audio if AudioState = automatic on other audio source.


            }

            public AudioStates Aud1_State = AudioStates.Disabled;
            public AudioSubStates Aud1_SubState = AudioSubStates.Disarmed;
            public AudioStates Aud2_State = AudioStates.Disabled;
            public AudioSubStates Aud2_Substate = AudioSubStates.Disarmed;

            public int Aud1_Cue = 0;
            public int Aud2_Cue = 0;
            public int CurrentCue = 0;

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
                //DontDestroyOnLoad(this.gameObject);

                if (audio1 == null)
                {
                    LogError("Audio source #1 is not set, please set this.");
                    return;
                }
                if (audio2 == null)
                {
                    LogError("Audio source #2 is not set, please set this.");
                    return;
                }

                audio1.clip = Resources.Load("blank_audio") as AudioClip;
                audio2.clip = Resources.Load("blank_audio") as AudioClip;
            }


            private void Start()
            {
                Log("Setting Audio Sources to Manual.");
                Aud1_State = AudioStates.Manual;
                Aud2_State = AudioStates.Manual;

                string msg = "to,from,audio,arm,audio1,1,c:/music/test2.mp3";
                string[] data = msg.Split(char.Parse(","));
                Arm(data);

            }

            private void Update() {
                if(Input.GetKeyDown(KeyCode.B))
                {
                    Log("Playing Audio");
                    audio1.Play();
                }
            }
            #endregion

            #region Audio Functions

            public void Disarm(string[] _cmd)
            {
                switch (_cmd[3])
                {
                    case "audio1":
                        audio1.clip = Resources.Load("blank_audio") as AudioClip;
                        break;
                    case "audio2":
                        audio2.clip = Resources.Load("blank_audio") as AudioClip;
                        break;
                }
            }

            private IEnumerator Arm_LoadSong(AudioSource _audiosource, string path)
            {
                string url = string.Format("file://{0}", path);
                #pragma warning disable
                WWW www = new WWW(url);
                yield return www;

                _audiosource.clip = NAudioPlayer.FromMp3Data(www.bytes);
                yield return "true";
            }

            public void Arm(string[] _cmd)
            {
                /*
                    cmd[4] - channel                // Default: none,   !: return
                    cmd[5] - cue #                  // Default: none,   !: return
                    cmd[6] - song url               // Default: none,   !: return
                    cmd[7] - prewait                // Default: 0,      !: (Default)
                    cmd[8] - fadein                 // Default: 0,      !: (Default)
                    cmd[9] - fadeout                // Default: 2,      !: (Default)
                    cmd[10] - postwait              // Default: 1,      !: (Default)
                    cmd[11] - automatic next        // Default: 0,      !: (Default)
                    cmd[12] - crossfade (auto only) // Default: 0,      !: (Default)
                */

                 string _build;

               // there is no cmd[4] cmd[5] cmd[6]
                if(_cmd.Length< 7){
                    return;
                } else {
                    switch (_cmd[4])
                    {
                        case "audio1":
                            Aud1_SubState = AudioSubStates.Arming;
                            Log(Aud1_SubState.ToString());
                            Aud1_Cue = int.Parse(_cmd[5]);
                            StartCoroutine(Arm_LoadSong(audio1, _cmd[6]));
                            Aud1_SubState = AudioSubStates.Armed;
                            Log(Aud1_SubState.ToString());
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