using System;
using UnityEngine;
using WebSocketSharp;
using System.Collections;
using UnityCore.Audio;

namespace UnityCore
{
    namespace Sockets
    {
        public class WSManager : MonoBehaviour
        {

            public static WSManager instance;

            #region VARIABLES
            public static string websocketId = "002";

            // Public variables
            public static WebSocket ws;
            public bool Developer;
            public string WebSocketURL = "localhost:8080";

            // Private variables
            private bool reconnectWS = false;
            private bool connectedB4 = false;

            #endregion
            /*
             Logic for the normal functions in unity
            */
            #region Unity Functions, inc. ws.OnMessage --> WSMessage() + WS.AsyncConnect()

            //Runs at the start of the program.

            private void Awake()
            {
                GameObject[] wsObject = GameObject.FindGameObjectsWithTag("WSManager");
                if (wsObject.Length > 1)
                {
                    Destroy(this.gameObject);
                }
                else
                {
                    instance = this;
                }
                DontDestroyOnLoad(this.gameObject);

                ws = new WebSocket("ws://" + WebSocketURL);
                ws.Connect();
                Log("Successfully connected to websocket.");
                ws.Send("001," + websocketId + ",REGISTER");
                connectedB4 = true;
            }
            private void Start()
            {
                ws.Connect();
                Log("Loaded.");
                ws.OnOpen += (sender, e) =>
                {
                    Log("Successfully connected to websocket.");
                    if (connectedB4 == false)
                    {
                        ws.Send("001," + websocketId + ",REGISTER");
                        connectedB4 = true;
                    }
                    else
                    {
                        ws.Send("001," + websocketId + ",RECONNECT");
                    }
                    reconnectWS = false;
                };

                ws.OnMessage += (sender, e) =>
                {
                    string message = e.Data;
                    WSMessage(message);
                };
            }
            // Run on every frame update.
            public void Update()
            {
                if (ws.IsAlive == false)
                {
                    if (!reconnectWS)
                    {
                        LogWarn("Disconnected, trying to reconnect.");
                        ReConnect(ws);
                        reconnectWS = true;
                    }
                }
            }

            //Runs when application stops
            private void OnApplicationQuit()
            {
                ws.Send("001," + websocketId + ",CLOSE");
                Log("Connection closed due to applicationQuit.");
                ws.CloseAsync();
            }

            #endregion
            // Logic for the connecting/reconnecting of the websocket when it has been disconnected.  
            #region Connection to the websocket 

            public static void ReConnect(WebSocket _ws)
            {
                if (_ws.IsAlive) return;
                _ws.ConnectAsync();
            }

            #endregion
            //Handling messages to/from the websocket.
            #region Message Handling
            public void WSMessage(string _message)
            {
                // Parse message into an array
                string[] cmd = _message.ToUpper().Split(char.Parse(","));

                // Check to see if this should receive the message
                // websocketId = this device (defined above), 000 = general broadcast
                if (cmd[0] != websocketId && cmd[0] != "000") return;

                // check to see if its from the control server
                if (cmd[0] != "001") return;

                // All of the main commands
                // Some are not implemented yet but will be here for the future.
                switch (cmd[2])
                {
                    case "STATUS":
                        Status(cmd);
                        break;
                    case "AUDIO":
                        Audio(cmd);
                        break;
                    case "CUEREQ":
                        break;
                    case "NOTES":
                        break;
                }
            }

            public void Status(string[] _cmd)
            {
                // Get the status and resend for all the audio managers.
                /*
                cmd[3] = request / send --> ignore "send"
                cmd[3] - subCommand cmd[4] - audio channel
                */
            }

            public static void Send_Status(string audioNum, string State, string Substate)
            {
                Debug.Log("001," + websocketId + ",STATUS,SEND," + audioNum + "," + State + "," + Substate);
                ws.Send("001," + websocketId + ",STATUS,SEND," + audioNum + "," + State + "," + Substate);
            }

            public void Audio(string[] _cmd)
            {
                if (_cmd[4] != "1" && _cmd[4] != "2" && _cmd[4] != "ALL") return;
                switch (_cmd[3])
                {
                    case "DISARM":
                        AudioManager.Disarm(_cmd);
                        break;

                    case "PLAY":
                        AudioManager.Play(_cmd);
                        break;

                    case "STOP":
                        AudioManager.Stop(_cmd);
                        break;

                    case "FADEIN":
                        AudioManager.FadeIn(_cmd);
                        break;

                    case "FADEOUT":
                        AudioManager.FadeOut(_cmd);
                        break;

                    case "REDUCE":
                        AudioManager.Reduce(_cmd);
                        break;

                    case "NORMAL":
                        AudioManager.Normal(_cmd);
                        break;

                    case "ARM":
                        AudioManager.Arm(_cmd);
                        break;
                }
            }


            #endregion
            // Debug Stuff
            #region DEBUG
            private void Log(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.Log("[WSManager] - " + _msg);
            }
            private void LogStatic(string _msg)
            {
                Debug.Log("[WSManager] - " + _msg);
            }
            private void LogWarn(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.LogWarning("[WSManager] - " + _msg);
            }
            private void LogError(string _msg)
            {
                if (!Developer)
                {
                    return;
                }
                Debug.LogError("[WSManager] - " + _msg);
            }
            #endregion
        }
    }
}