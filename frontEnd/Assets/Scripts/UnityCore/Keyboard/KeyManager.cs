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

            private static KeyManager instance = null;
            public static KeyManager Instance;

            #region Variables

            public bool Developer;
            public int Audio_Selected = 1;

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
