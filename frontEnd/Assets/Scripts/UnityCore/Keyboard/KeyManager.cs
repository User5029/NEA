using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityCore.Audio;
using UnityCore.Sockets;
using TMPro;
using UnityEngine.UI;

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

            public Image Source1Background;
            public Image Source2Background;

            private Color SelectedColour = new Color32(76,133,0,255);
            private Color NonSelectedColour = new Color32(88,88,88,255);

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

                if (Audio_Selected == 1)
                {
                    Source1Background.color = SelectedColour;
                    Source2Background.color = NonSelectedColour;
                }
                else if (Audio_Selected == 2)
                {
                    Source1Background.color = NonSelectedColour;
                    Source2Background.color = SelectedColour;
                }

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

                if (Input.GetKeyDown(KeyCode.Space))
                {
                    // Play the selected cue
                    string[] _args = (AudMessagePrefix + "play," + Audio_Selected).Split(",");
                    AudioManager.Play(_args);
                }

                if (Input.GetKeyDown(KeyCode.Escape))
                {
                    string[] _args = (AudMessagePrefix + "stop,ALL").Split(",");
                    AudioManager.Stop(_args);
                }

                if (Input.GetKeyDown(KeyCode.F))
                {
                    string[] _args = (AudMessagePrefix + "stop," + Audio_Selected).Split(",");
                    AudioManager.Stop(_args);
                }

                if (Input.GetKeyDown(KeyCode.V))
                {
                    string[] _args = (AudMessagePrefix + "fade," + Audio_Selected + ",2").Split(",");
                    AudioManager.FadeOut(_args);
                }

                if (Input.GetKeyDown(KeyCode.N))
                {
                    string[] _args = (AudMessagePrefix + "fade," + Audio_Selected + ",2").Split(",");
                    AudioManager.FadeIn(_args);
                }

                if (Input.GetKeyDown(KeyCode.C))
                {
                    string[] _args = (AudMessagePrefix + "fade," + Audio_Selected).Split(",");
                    AudioManager.Reduce(_args);
                }

                if (Input.GetKeyDown(KeyCode.X))
                {
                    string[] _args = (AudMessagePrefix + "fade," + Audio_Selected).Split(",");
                    AudioManager.Normal(_args);
                }

                if (Input.GetKeyDown(KeyCode.P))
                {
                    string[] _args = (AudMessagePrefix + "fade," + Audio_Selected).Split(",");
                    AudioManager.Pause(_args);
                }

                if (Input.GetKeyDown(KeyCode.H))
                {
                    string[] _args = (AudMessagePrefix + "fade," + Audio_Selected).Split(",");
                    AudioManager.Disarm(_args);
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
