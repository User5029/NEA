using System.Collections;
using Unity.Burst.Intrinsics;
using UnityEngine;
using UnityCore.Sockets;
using System.IO;
using System.Threading.Tasks;
using UnityEngine.Networking;
using System;
using NAudio.Gui.TrackView;
using UnityCore.Audio;
using System.Linq;
using System.Collections.Generic;

namespace UnityCore
{
    namespace Audio
    {
        public class AudioManager : MonoBehaviour
        {
            // Creates the instance of the AudioManager
            private static AudioManager instance = null;
            public static AudioManager Instance;

            public static SongNAudio SongNAudio;


            #region variables

            // Public Variables
            public static AudioSource audio1;
            public static AudioSource audio2;
            public bool Developer;

            public static int WarningTime = 20;

            public static float Aud1_Length = 0;
            public static float Aud2_Length = 0;

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
            public static int Aud1_Cue = 1;
            public static string Aud1_Name = "None";
            public static int Aud2_Cue = 2;
            public static string Aud2_Name = "None";
            public static int CurrentCue = 0;
            public static int NextCue = 1;

            // Private Variables
            private string[] Aud1_Data;
            private string[] Aud2_Data;

            
            // Allowing the fade in/out functions to be used.
            private static int Aud1_FadeInNeeded = 0;
            private static int Aud2_FadeInNeeded = 0;
            private static int Aud1_FadeOutNeeded = 0;
            private static int Aud2_FadeOutNeeded = 0;

            #endregion

            #region Unity Functions
            private void Awake()
            {
                // Makes sure there is a non existing instance of this manager before proceeding
                if (instance != null && instance != this)
                {
                    Destroy(this.gameObject);
                    return;
                }
                else
                {
                    instance = this;
                }
                // Does not destory this manager when a scene is reloaded.
                DontDestroyOnLoad(this.gameObject);

                // These 3 objects make it so that less needs to be done in unity and more can be done in code.
                audio1 = GameObject.FindGameObjectWithTag("audio1").GetComponentsInChildren<AudioSource>()[0];
                audio2 = GameObject.FindGameObjectWithTag("audio2").GetComponentsInChildren<AudioSource>()[0];
                SongNAudio = GameObject.FindGameObjectWithTag("AudManager").GetComponentInChildren<SongNAudio>();

                // Check to make sure the correct objects are passed to this manager in the unity engine.
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
                if(!SongNAudio)
                {
                    LogError("Error getting SongNAudio");
                    return;
                }
            }


            private void Start()
            {
                // Starts the audio manager by loading the 'blank' track into the audio sources so no accidental noises is made.
                Disarm("0,1,2,3,ALL".Split(","));
                Log("Setting Audio Sources to Manual.");
                Aud1_State = AudioStates.Manual;
                Aud2_State = AudioStates.Manual;

                WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());

                //string msg = "to,from,audio,arm,1,1,test,c:/music/test3.mp3";
                //string[] data = msg.Split(char.Parse(","));
                //Arm(data, data);

            }

            // TMP Variables
            public static float Aud1_Time = -1;
            public static float Aud2_Time = -1;
            //private static float Aud1_Left = 0;
            //private static float Aud2_Left = 0;
            private void Update()
            {
                /*
                    Every time the frame updates it first checks to see if the audio source is playing
                    Then checks to see if the length of time left is less then the warning time
                    Then check to see if it should fade out the music if the time has exeeded.
                    Then checks if the length of the audio is the same as the length of the track
                */
                Aud1_Time = audio1.time;
                Aud2_Time = audio2.time;

                // Audio 1 checker
                if (audio1.isPlaying)
                {
                    
                    if (Aud1_Time + WarningTime > Aud1_Length || Aud1_Time + WarningTime == Aud1_Length)
                    {
                        if (Aud1_SubState != AudioSubStates.Warning && Aud1_SubState != AudioSubStates.FadeOut)
                        {
                            Aud1_SubState = AudioSubStates.Warning;
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        }
                        //Debug.Log(Aud1_Length - Aud1_FadeOutNeeded <= Aud1_Time);
                        //Debug.Log(Aud1_SubState != AudioSubStates.FadeOut);
                        //Aud1_Left = Aud1_Length - Aud1_Time;
                        //Debug.Log("Time Left: " + (Aud1_Left) + " " + (Aud1_Left < Aud1_FadeInNeeded));
                        if (Aud1_Length - Aud1_FadeOutNeeded <= Aud1_Time && Aud1_SubState != AudioSubStates.FadeOut)
                        {
                            Aud1_SubState = AudioSubStates.FadeOut;
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                            instance.StartCoroutine(FadeOutCo("1", audio1, Aud1_FadeOutNeeded));
                        }
                    } else
                    {
                        //LogStatic((Aud1_Time + WarningTime) + "/" + Aud1_Length + " :: " + (Aud1_Time + WarningTime > Aud1_Length));
                    }
                    if (Aud1_Time == Aud1_Length)
                    {
                        Aud1_SubState = AudioSubStates.Ended;
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                    }
                }
                // Audio 2 checker
                if (audio2.isPlaying)
                {
                    return;
                    if (Aud2_Time + WarningTime > Aud2_Length)
                    {
                        if (Aud2_SubState != AudioSubStates.Warning && Aud2_SubState != AudioSubStates.FadeOut)
                        {
                            Aud2_SubState = AudioSubStates.Warning;
                            WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                        }
                        if (Aud2_Length - Aud2_FadeOutNeeded - 1 < Aud2_Time)
                        {
                            Aud2_SubState = AudioSubStates.FadeOut;
                            WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                            instance.StartCoroutine(FadeOutCo("2", audio2, Aud2_FadeOutNeeded));
                        }
                    }
                    if (Aud2_Time == Aud2_Length)
                    {
                        Aud2_SubState = AudioSubStates.Ended;
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                    }
                }
            }
            #endregion

            #region Audio Functions

            public static void Disarm(string[] _cmd)
            {
                // Takes in an array called _cmd and checks index4 for "1" or "2" or "ALL"
                switch (_cmd[4])
                {
                    case "1":
                        audio1.Stop(); // Stops the audio if playing
                        audio1.clip = Resources.Load("blank_audio") as UnityEngine.AudioClip; // Loads blank clip
                        Aud1_SubState = AudioSubStates.Disarmed; // Sets local property of the audio source
                        Aud1_Name = "None"; // Reset variables
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString()); // Sends info to control server
                        Aud1_Length = 0; // Reset variables
                        Aud1_Time = -1; // Reset variables
                        break;
                    case "2":
                        audio2.Stop(); // Stops the audio if playing
                        audio2.clip = Resources.Load("blank_audio") as UnityEngine.AudioClip; // Loads blank clip
                        Aud2_SubState = AudioSubStates.Disarmed; // Sets local property of the audio source
                        Aud2_Name = "None"; // Reset variables
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString()); // Sends info to control server
                        Aud2_Length = 0; // Reset variables
                        Aud2_Time = -1; // Reset variables
                        break;
                    case "ALL":
                        audio1.Stop(); // Stops the audio if playing
                        audio2.Stop(); // Stops the audio if playing
                        audio1.clip = Resources.Load("blank_audio") as UnityEngine.AudioClip; // Loads blank clip
                        audio2.clip = Resources.Load("blank_audio") as UnityEngine.AudioClip; // Loads blank clip
                        Aud1_SubState = AudioSubStates.Disarmed; // Sets local property of the audio source
                        Aud1_Name = "None"; // Reset variables
                        Aud2_SubState = AudioSubStates.Disarmed; // Sets local property of the audio source
                        Aud2_Name = "None"; // Reset variables
                        WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString()); // Sends info to control server
                        WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString()); // Sends info to control server
                        Aud1_Length = 0; // Reset variables
                        Aud2_Length = 0; // Reset variables
                        Aud1_Time = -1; // Reset variables
                        Aud2_Time = -1; // Reset variables
                        break;
                }
            }
            public static void Play(string[] _cmd)
            {

                // Takes in an array called _cmd and checks index4 for "1" or "2"
                switch (_cmd[4])
                {
                    case "1":
                        if (audio1.isPlaying == true) return; // Check to makes sure that the audio can actually be played
                        if (audio1.clip.length == 1.224f) return; // Check to makes sure that the audio can actually be played
                        audio1.volume = 0.95f; // Sets the volume to 95% to ensure there is no problems from the fadeout functions (safety)
                        CurrentCue = Aud1_Cue; // Sets the cue variables so that the automated part of the code can function
                        NextCue = CurrentCue + 1; // Sets the cue variables so that the automated part of the code can function

                        // Check to see if the audio needs to be faded in
                        if (Aud1_FadeInNeeded > 0)
                        {
                            // If it does it sets the Audio state to fade in
                            Aud1_SubState = AudioSubStates.FadeIn;
                            // Send an update to the control server
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                            // Starts the process of fading in the audio using another function
                            instance.StartCoroutine(FadeInCo("1", audio1, Aud1_FadeInNeeded));
                        }
                        else
                        {
                            // If it does not need 
                            audio1.Play();
                            Aud1_SubState = AudioSubStates.Playing;
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                        }
                        break;
                    case "2":
                        if (audio2.isPlaying == true) return; // Check to makes sure that the audio can actually be played
                        if (audio2.clip.length == 1.224f) return; // Check to makes sure that the audio can actually be played
                        audio2.volume = 0.95f; // Sets the volume to 95% to ensure there is no problems from the fadeout functions (safety)
                        CurrentCue = Aud2_Cue; // Sets the cue variables so that the automated part of the code can function
                        NextCue = CurrentCue + 1; // Sets the cue variables so that the automated part of the code can function
                        
                        // Check to see if the audio needs to be faded in
                        if (Aud2_FadeInNeeded > 0)
                        {
                            // If it needs to be faded in it will run this code
                            Aud2_SubState = AudioSubStates.FadeIn; // Sets the status of the audio source to fading in
                            // Updates the control server on the new status
                            WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                            // Runs the FadeIn function
                            instance.StartCoroutine(FadeInCo("2", audio2, Aud2_FadeInNeeded));
                        }
                        else
                        {
                            // If the audio source does not needed to be faded in it wil play normally
                            audio2.Play(); // Plays the audio
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


            private static IEnumerator LoadSongCoroutine(AudioSource aud, string path)
            {
                string url = string.Format("file://{0}", path);
                #pragma warning disable
                WWW www = new WWW(url);
                yield return www;

                aud.clip = NAudioPlayer.FromMp3Data(www.bytes);
                Debug.Log("Audio Armed");
            }



            public static async void Arm(string[] _cmd, string[] _ocmd)
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

                //string _build;

                // there is no cmd[4] cmd[5] cmd[6] cmd[7]

                List<string> newcmd = new List<string>(_cmd);


                if (newcmd.Count <= 8)
                {
                    return;
                }
                if (newcmd.Count == 8)
                {
                    newcmd.Add("0");
                    newcmd.Add("0");
                    newcmd.Add("0");
                }
                if (newcmd.Count == 9)
                {
                    newcmd.Add("0");
                    newcmd.Add("0");
                }
                if(newcmd.Count == 10)
                {
                    newcmd.Add("0");
                }
                if(newcmd.Count() < 11)
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
                            SongNAudio.toSet = "1";
                            SongNAudio.path = _ocmd[7];
                            while (SongNAudio.done == false) { }
                            SongNAudio.done = false;
                            LogStatic("1.1");
                            Aud1_FadeInNeeded = int.Parse(newcmd[9]);
                            LogStatic("1.2");
                            Aud1_FadeOutNeeded = int.Parse(newcmd[10]);
                            LogStatic("1.3");
                            Aud1_SubState = AudioSubStates.Armed;
                            LogStatic("1.4");
                            Debug.Log("Length: " + Aud1_Length + " FadeIn: " + Aud1_FadeInNeeded + " FadeOut: " + Aud1_FadeOutNeeded);
                            WSManager.Send_Status("1", Aud1_State.ToString(), Aud1_SubState.ToString());
                            
                            break;

                        case "2":
                            Aud2_Cue = int.Parse(_cmd[5]);
                            Aud2_Name = _cmd[6];
                            Aud2_SubState = AudioSubStates.Arming;
                            WSManager.Send_Status("2", Aud2_State.ToString(), Aud2_SubState.ToString());
                            //instance.StartCoroutine(LoadSongCoroutine(audio1, _cmd[7]));
                            Aud2_FadeInNeeded = int.Parse(_cmd[9]);
                            Aud2_FadeOutNeeded = int.Parse(_cmd[10]);
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