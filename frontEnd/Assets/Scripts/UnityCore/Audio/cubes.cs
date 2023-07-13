using System.Collections;
using System.Collections.Generic;
using System.Numerics;
using UnityEngine;

public class cubes : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject _sampleCubePrefab;
    GameObject[] _sampleCube = new GameObject[512];
    public float _maxScale;
    void Start()
    {
        for(int i =0; i < 512; i++)
        {
            GameObject _instanceSampleCube = (GameObject)Instantiate (_sampleCubePrefab);
            _instanceSampleCube.transform.position = this.transform.position;
            _instanceSampleCube.transform.parent = this.transform;
            _instanceSampleCube.name = "SampleCube" + i;
            this.transform.eulerAngles = new UnityEngine.Vector3(0, -0.703125f * i, 0);
            _instanceSampleCube.transform.position = UnityEngine.Vector3.forward * 100;
            _sampleCube[i] = _instanceSampleCube;
        }        
    }

    // Update is called once per frame
    void Update()
    {
        for(int i=0; i<512; i++)
        {
            if(_sampleCube != null){
                _sampleCube[i].transform.localScale = new UnityEngine.Vector3(10, (AudioPeer._samples[i] * _maxScale) +2, 10);
            }
        }        
    }
}
