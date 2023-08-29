using System.Collections;
using Unity.Burst.Intrinsics;
using UnityEngine;
using UnityCore.Sockets;


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

            public static int WarningTime = 20;

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

            //Set the initial states of the audio.

            public static AudioStates Aud1_State = AudioStates.Disabled;         
            public static AudioSubStates Aud1_SubState = AudioSubStates.Disarmed;
            public static AudioStates Aud2_State = AudioStates.Disabled;
            public static AudioSubStates Aud2_SubState = AudioSubStates.Disarmed;

            // Data used for each audio manager.
            public static int Aud1_Cue = 0;
            public static string Aud1_Name = "None";
            public static int Aud2_Cue = 0;
            public static string Aud2_Name = "None";
            public static int CurrentCue = 0;
            public static int NextCue = 0;

            // Private Variables
            private string[] Aud1_Data;
            private string[] Aud2_Data;

            
            // Allowing the fade in/out functions to be used.
            private static int Aud1_FadeInNeeded = 0;
            private static int Aud2_FadeInNeeded = 0;
            private static int Aud1_FadeOutNeeded = 0;
            private static int Aud2_FadeOutNeeded = 0;

            private static float Aud1_Length = 0;
            private static float Aud2_Length = 0;

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
            }


            private void Start()
            {
                Disarm("0,1,2,3,ALL".Split(","));
                Log("Setting Audio Sources to Manual.");
                Aud1_State = AudioStates.Manual;
                Aud2_State = AudioStates.Manual;

                WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());

                string msg = "to,from,audio,arm,1,1,c:/music/test3.mp3";
                string[] data = msg.Split(char.Parse(","));
                Arm(data);

            }

            // TMP Variables
            private static float Aud1_Time = 0;
            private static float Aud2_Time = 0;
            private void Update()
            {
                Aud1_Time = audio1.time;
                Aud2_Time = audio2.time;
                
                // Audio 1 checker
                if(Aud1_Time + WarningTime > Aud1_Length){
                    if(Aud1_SubState != AudioSubStates.Warning && Aud1_SubState != AudioSubStates.FadeOut){
                        Aud1_SubState = AudioSubStates.Warning;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString()); 
                    }
                    if(Aud1_Length - Aud1_FadeOutNeeded - 1 < Aud1_Time){
                        Aud1_SubState = AudioSubStates.FadeOut;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        instance.StartCoroutine(FadeOutCo("1", audio1, Aud1_FadeOutNeeded));                        
                    }
                }
                if(Aud1_Time == Aud1_Length){
                    Aud1_SubState = AudioSubStates.Ended;
                    WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                }

                // Audio 2 checker
                if(Aud2_Time + WarningTime > Aud2_Length){
                    if(Aud2_SubState != AudioSubStates.Warning && Aud2_SubState != AudioSubStates.FadeOut){
                        Aud2_SubState = AudioSubStates.Warning;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString()); 
                    }
                    if(Aud2_Length - Aud2_FadeOutNeeded - 1 < Aud2_Time){
                        Aud2_SubState = AudioSubStates.FadeOut;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString()); 
                        instance.StartCoroutine(FadeOutCo("2", audio2, Aud2_FadeOutNeeded));                        
                    }
                }
                if(Aud2_Time == Aud2_Length){
                    Aud2_SubState = AudioSubStates.Ended;
                    WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString()); 
                }
            }
            #endregion

            #region Audio Functions

            public static void Disarm(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.Stop();
                        audio1.clip = Resources.Load("blank_audio") as AudioClip;
                        Aud1_SubState = AudioSubStates.Disarmed;
                        Aud1_Name = "None";
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        Aud1_Length = 0;
                        break;
                    case "2":
                        audio2.Stop();
                        audio2.clip = Resources.Load("blank_audio") as AudioClip;
                        Aud2_SubState = AudioSubStates.Disarmed;
                        Aud2_Name = "None";
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        Aud2_Length = 0;
                        break;
                    case "ALL":
                        audio1.Stop();
                        audio2.Stop();
                        audio1.clip = Resources.Load("blank_audio") as AudioClip;
                        audio2.clip = Resources.Load("blank_audio") as AudioClip;
                        Aud1_SubState = AudioSubStates.Disarmed;
                        Aud1_Name = "None";
                        Aud2_SubState = AudioSubStates.Disarmed;
                        Aud2_Name = "None";
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        Aud1_Length = 0;
                        Aud2_Length = 0;
                        break;
                }
            }
            public static void Play(string[] _cmd)
            {

                switch (_cmd[4])
                {
                    case "1":
                        if (audio1.isPlaying == true) return;
                        audio1.volume = 0.95f;
                        CurrentCue = Aud1_Cue;
                        NextCue = CurrentCue + 1;

                        if (Aud1_FadeInNeeded > 0)
                        {
                            Aud1_SubState = AudioSubStates.FadeIn;
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                            instance.StartCoroutine(FadeInCo("1", audio1, Aud1_FadeInNeeded));
                        }
                        else
                        {
                            audio1.Play();
                            Aud1_SubState = AudioSubStates.Playing;
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        }
                        break;
                    case "2":
                        if (audio2.isPlaying == true) return;
                        audio2.volume = 0.95f;
                        CurrentCue = Aud2_Cue;
                        NextCue = CurrentCue + 1;
                        if (Aud2_FadeInNeeded > 0)
                        {
                            Aud2_SubState = AudioSubStates.FadeIn;
                            WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                            instance.StartCoroutine(FadeInCo("2", audio2, Aud2_FadeInNeeded));
                        }
                        else
                        {
                            audio2.Play();
                            Aud2_SubState = AudioSubStates.Playing;
                            WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        }
                        break;
                }
            }
            public static void Pause(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        if (audio1.isPlaying == true)
                        {
                            audio1.Pause();
                            Aud1_SubState = AudioSubStates.Paused;
                        }
                        else
                        {
                            audio1.UnPause();
                            Aud1_SubState = AudioSubStates.Playing;
                        }
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        break;
                    case "2":
                        if (audio2.isPlaying == true)
                        {
                            audio2.Pause();
                            Aud2_SubState = AudioSubStates.Paused;
                        }
                        else
                        {
                            audio2.UnPause();
                            Aud2_SubState = AudioSubStates.Playing;
                        }
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        break;
                    case "ALL":
                        audio1.Pause();
                        audio2.Pause();
                        Aud1_SubState = AudioSubStates.Paused;
                        Aud2_SubState = AudioSubStates.Paused;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        break;
                }
            }
            public static void Stop(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        audio1.Stop();
                        Aud1_SubState = AudioSubStates.Stopped;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        break;
                    case "2":
                        audio2.Stop();
                        Aud1_SubState = AudioSubStates.Stopped;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        break;
                    case "ALL":
                        audio1.Stop();
                        audio2.Stop();
                        Aud1_SubState = AudioSubStates.Stopped;
                        Aud1_SubState = AudioSubStates.Stopped;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        break;
                }
            }
            public static IEnumerator FadeInCo(string AudNum, AudioSource audioSource, float FadeTime)
            {
                audioSource.volume = 0.1f;
                audioSource.Play();
                while (audioSource.volume < 1)
                {
                    //audioSource.volume += startVolume * Time.deltaTime / FadeTime;
                    audioSource.volume += 1 * Time.deltaTime / FadeTime;

                    yield return null;
                }

                switch (AudNum)
                {
                    case "1":
                        Aud1_SubState = AudioSubStates.Playing;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        break;
                    case "2":
                        Aud2_SubState = AudioSubStates.Playing;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        break;
                }

            }
            public static void FadeIn(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        if (audio1.isPlaying == true) return;
                        Aud1_SubState = AudioSubStates.FadeIn;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        instance.StartCoroutine(FadeInCo("1", audio1, float.Parse(_cmd[5])));
                        break;
                    case "2":
                        if (audio2.isPlaying == true) return;
                        Aud2_SubState = AudioSubStates.FadeIn;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        instance.StartCoroutine(FadeInCo("2", audio2, float.Parse(_cmd[5])));
                        break;
                }
            }
            public static IEnumerator FadeOutCo(string AudNum, AudioSource audioSource, float FadeTime)
            {
                float startVolume = audioSource.volume;

                while (audioSource.volume > 0)
                {
                    audioSource.volume -= startVolume * Time.deltaTime / FadeTime;

                    yield return null;
                }

                audioSource.Stop();
                audioSource.volume = startVolume;

                switch (AudNum)
                {
                    case "1":
                        Aud1_SubState = AudioSubStates.Ended;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        break;
                    case "2":
                        Aud2_SubState = AudioSubStates.Ended;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        break;
                }
            }
            public static void FadeOut(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        if (audio1.isPlaying == false) return;
                        Aud1_SubState = AudioSubStates.FadeOut;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        instance.StartCoroutine(FadeOutCo("1", audio1, float.Parse(_cmd[5])));
                        break;
                    case "2":
                        if (audio2.isPlaying == false) return;
                        Aud2_SubState = AudioSubStates.FadeOut;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        instance.StartCoroutine(FadeOutCo("2", audio2, float.Parse(_cmd[5])));
                        break;
                }
            }
            public static void Reduce(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        if (audio1.isPlaying == false) return;
                        Aud1_SubState = AudioSubStates.Reduced;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        audio1.volume = 0.5f;
                        break;
                    case "2":
                        if (audio2.isPlaying == false) return;
                        Aud2_SubState = AudioSubStates.Reduced;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        audio2.volume = 0.5f;
                        break;
                }
            }
            public static void Normal(string[] _cmd)
            {
                switch (_cmd[4])
                {
                    case "1":
                        if (audio1.isPlaying == false) return;
                        Aud1_SubState = AudioSubStates.Reduced;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        audio1.volume = 0.95f;
                        break;
                    case "2":
                        if (audio2.isPlaying == false) return;
                        Aud2_SubState = AudioSubStates.Reduced;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        audio2.volume = 0.95f;
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
                if (_cmd.Length <= 8)
                {
                    return;
                }
                else
                {
                    switch (_cmd[4])
                    {
                        case "1":
                            Aud1_Cue = int.Parse(_cmd[5]);
                            Aud1_Name = _cmd[6];
                            Aud1_SubState = AudioSubStates.Arming;
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                            instance.StartCoroutine(Arm_LoadSong(audio1, _cmd[6]));
                            Aud1_FadeInNeeded = int.Parse(_cmd[9]);
                            Aud1_FadeOutNeeded = int.Parse(_cmd[9]);
                            Aud1_SubState = AudioSubStates.Armed;
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                            Aud1_Length = audio1.clip.length;
                            break;

                        case "2":
                            Aud2_Cue = int.Parse(_cmd[5]);
                            Aud2_Name = _cmd[6];
                            Aud2_SubState = AudioSubStates.Arming;
                            WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                            instance.StartCoroutine(Arm_LoadSong(audio2, _cmd[6]));
                            Aud2_FadeInNeeded = int.Parse(_cmd[9]);
                            Aud2_FadeOutNeeded = int.Parse(_cmd[9]);
                            Aud2_SubState = AudioSubStates.Armed;
                            WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                            Aud2_Length = audio2.clip.length;
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