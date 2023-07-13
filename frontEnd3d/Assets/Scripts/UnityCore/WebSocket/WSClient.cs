using System;
using UnityEngine;
using WebSocketSharp;
using System.Collections;

namespace UnityCore
{
    namespace Audio
    {
        public class WsClient : MonoBehaviour
        {
            WebSocket ws;
            public SongNAudio Audio;

            private void Start()
            {
                ws = new WebSocket("ws://localhost:8080");
                ws.Connect();
                ws.OnMessage += (sender, e) =>
                {
                    Debug.Log("Message Received from " + ((WebSocket)sender).Url + ", Data : " + e.Data);
                    Audio.path = e.Data;
                };

                ws.OnClose += (sender, e) =>
                {
                    Debug.LogWarning("WEBSOCKET: Disconnected");
                };

                ws.OnOpen += (sender, e) =>
                {
                    Debug.Log("WEBSOCKET: Connection Opened");
                };
            }


            private void Update()
            {
                if (ws == null)
                {
                    return;
                }
                if (Input.GetKeyDown(KeyCode.Space))
                {
                    ws.Send("Hello");
                }

                if (Input.GetKeyDown(KeyCode.B))
                {

                }
            }
        }
    }
}