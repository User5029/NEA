using System;
using UnityEngine;
using WebSocketSharp;
using System.Collections;

namespace UnityCore
{
    namespace Sockets
    {
        public class WSManager : MonoBehaviour
        {

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
            private void Start()
            {
                Log("Loaded.");
                reconnectWS = true;
                ws = new WebSocket("ws://" + WebSocketURL);
                ReConnect(ws);
                ws.OnOpen += (sender, e) =>
                {
                    Log("Successfully connected to websocket.");
                    if(connectedB4 == false){
                        ws.Send("001,"+websocketId+",REGISTER");
                        connectedB4 = true;
                    } else {
                        ws.Send("001,"+websocketId+",RECONNECT");
                    }                    
                    reconnectWS = false;
                };

                ws.OnMessage += (sender, e) => {
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
                ws.Send("001,"+websocketId+",CLOSE");
                Log("Connection closed due to applicationQuit.");
                ws.CloseAsync();
            }

            #endregion
            // Logic for the connecting/reconnecting of the websocket when it has been disconnected.  
            #region Connection to the websocket 

            public static void ReConnect(WebSocket _ws)
            {
                if(_ws.IsAlive) return;
                _ws.ConnectAsync();

            }

            #endregion
            //Handling messages to/from the websocket.
            #region Message Handling
            public void WSMessage(string _message)
            {
                string[] cmd = _message.Split(char.Parse(","));

                switch (cmd[2]){
                    case "STATUS":
                        Status(cmd);
                        break;
                    case "AUDIO":
                        Audio(cmd);
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

            public void Audio(string[] _cmd)
            {
                //Control the audio requests from other apps.
                /*
                cmd[3] - subcommand cmd[4] - channel cmd[5...] - data per audio.
                */
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