using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityCore.Audio;
using UnityCore.Sockets;
using TMPro;

namespace UnityCore
{
    namespace Keyboard
    {
        public class KeyManager : MonoBehaviour
        {
            
            // Generates a single instance of this KeyManager
            private static KeyManager instance = null;
            public static KeyManager Instance;

            #region Variables

            public bool Developer;
            public int Audio_Selected = 1;

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

            }

            private void Start()
            {
                Log("Is now online.");
            }

            private void Update()
            {
                // Variable for later use. Don't want it over written.
                string AudMessagePrefix = "000,000,audio,";

                if (Input.GetKeyDown(KeyCode.Alpha1)) 
                {
                    // audio selector to audio source 1
                    Audio_Selected = 1;
                }

                if (Input.GetKeyDown(KeyCode.Alpha2))
                {
                    // audio selector to audio source 2
                    Audio_Selected = 2;
                }

                if (Input.GetKeyDown(KeyCode.B))
                {
                    // Tell the control server to send over info to arm the next cue.
                    WSManager.Send_CUEREQ(Audio_Selected.ToString(), AudioManager.NextCue.ToString());
                }

                if(Input.GetKeyDown(KeyCode.Space))
                {
                    // Play the selected cue
                    string[] _args = (AudMessagePrefix + "play," + Audio_Selected).Split(",");
                    AudioManager.Play(_args);
                }


            }
            #endregion

            #region DEBUG
            // These are custom functions to append the filename to the start of the log.
            // This is done to make sure that it is easy to identify where problems are comming from.
            private void Log(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.Log("[KeyManager] - " + _msg);
            }
            private static void LogStatic(string _msg)
            {
                Debug.Log("[KeyManager] - " + _msg);
            }
            private void LogWarn(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.LogWarning("[KeyManager] - " + _msg);
            }
            private void LogError(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.LogError("[KeyManager] - " + _msg);
            }
            #endregion

        }
    }
}
