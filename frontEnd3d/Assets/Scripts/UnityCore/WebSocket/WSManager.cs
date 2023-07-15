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
            public static string websocketId = "002";

            // Public variables
            WebSocket ws;
            public bool Developer;
            public string WebSocketURL = "localhost:8080";

            // Private variables
            private bool reconnectWS = false;

            /*
             Logic for the normal functions in unity
            */

            //Runs at the start of the program.
            private void Start()
            {
                Log("Loaded.");
                reconnectWS = true;
                ws = new WebSocket("ws://" + WebSocketURL);
                StartCoroutine(ConnectLoop());
                ws.OnOpen += (sender, e) =>
                {
                    Log("Successfully connected to websocket.");
                    ws.Send("001,"+websocketId+",REGISTER");
                    reconnectWS = false;
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
                        ReConnectLoopProxy();
                        reconnectWS = true;
                    }
                }
            }

            //Runs when application stops
            private void OnApplicationQuit()
            {
                ws.Send("001,"+websocketId+",CLOSE");
                ws.CloseAsync();
            }



            // Logic for the reconnecting of the websocket when it has been disconnected. 
            // Will retry every 5 seconds for a total of 5 times before giving an error.

            private void ReConnectLoopProxy()
            {
                StartCoroutine(ReConnectLoop());
            }

            //Variables for ReConnect
            private bool ReConnect_loop = true;
            private int ReConnect_int = 0;
            private int CheckCounter = 0;
            private IEnumerator ReConnectLoop()
            {
                ReConnect_int = 0;
                ReConnect_loop = true;
                while (ReConnect_loop)
                {
                    if (ws.IsAlive)
                    {
                        yield return true;
                        reconnectWS = false;
                        ReConnect_loop = false;
                        CheckCounter++;
                    }
                    Log("Reconnect Attempt: " + ReConnect_int);
                    ws.ConnectAsync();
                    yield return new WaitForSeconds(0.5f);
                    ReConnect_int++;

                    if (ReConnect_int == 5)
                    {
                        ReConnect_loop = false;
                    }

                    Log("(check counter) " + CheckCounter);

                }

                if (ReConnect_int >= 5)
                {
                    LogError("Unable to connect to WebSocket.");
                }
                StopCoroutine(ConnectLoop());
            }

            private IEnumerator ConnectLoop()
            {
                ws.ConnectAsync();
                yield return new WaitForSeconds(1);
            }





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
        }
    }
}