import {Heading} from "./components/Heading";
import {Inputs} from "./components/Inputs";
import {Paths} from "./components/Paths";
import './App.css';
import React from 'react';
import { MapComponent } from "./components/MapComponent";
import {useState} from 'react';
import { useRef, useEffect } from 'react';
import $ from 'jquery';
import {
  GoogleMap,
  Marker,
  DirectionsRenderer,
} from '@react-google-maps/api'

const center = { lat: 44.564588, lng: -123.275705 }
var waypointsElena = [];
var waypointsShortest = [];
function App() {
  const [isHidden, setIsHidden] = useState(true)
  const [origin,setOrigin] = useState(null);
  const [destination, setDestination] = useState(null)
  const [directionsResponseElena, setDirectionsResponseElena] = useState(null);
  const [directionsResponseShortest, setDirectionsResponseShortest] = useState(null);
  const [threshold, setThreshold] = useState("");
  const [algorithm, setAlgorithm] = useState("");
  const [elevation ,setElevation] = useState("");
  const [isDisabled, setIsDisabled] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [thresholdError, setThresholdError] = useState("");
  const [typeOfPath, setTypeOfPath] = useState("elena");
  const [shortestDistanceValue, setShortestDistanceValue] = useState(0.0000);
  const [shortestDistanceGain, setShortestDistanceGain] = useState(0.0000);
  const [elenaDistanceValue, setElenaDistanceValue] = useState(0.0000);
  const [elenaDistanceGain, setElenaDistanceGain] = useState(0.0000);
  const [isPathButtonDisabled, setIsPathButtonDisabled] = useState(true);

  const setHiddenState = (hidden) => {
    setIsHidden(hidden);
  };

  const fetchData = (src, dest) => {
    const responseToBackend = {
      origin_location: [src.geometry.location.lat(), src.geometry.location.lng()],
      destination_location: [dest.geometry.location.lat(), dest.geometry.location.lng()],
      elevation_option: elevation,
      selected_algorithm: algorithm,
      path_limit: threshold
    };
  
    $.ajax({
      type: 'POST',
      url: 'http://localhost:5000/get_elena_path',
      data: JSON.stringify(responseToBackend),
      contentType: 'application/json',
      success: function (data) {
        parseBackendResponse(data);
        console.log('Response of the output data:', data);
      },
      error: function (error) {
        console.error('Error:', error);
      }
    });
  };

  // eslint-disable-next-line no-undef
  const directionServiceElena =  new google.maps.DirectionsService()
  // eslint-disable-next-line no-undef
  const directionServiceShortest =  new google.maps.DirectionsService()

  function parseBackendResponse(jsonData)
  {
    jsonData = JSON.parse(jsonData)
    console.log("#######$$$$");
    console.log(jsonData, typeof(jsonData));
    console.log("#######$$$$");

    setShortestDistanceValue(jsonData.shortest_distance)
    setShortestDistanceGain(jsonData.shortest_elevation_gain)
    setElenaDistanceValue(jsonData.elevation_path_distance)
    setElenaDistanceGain(jsonData.elevation_path_gain)
    
    for(var i = 0; i<jsonData.path_elevation.shape.data_points.length; i++)
    {
      var tempList = {lat: 0 , lng: 0};
      tempList.lat = jsonData.path_elevation.shape.data_points[i][1];
      tempList.lng = jsonData.path_elevation.shape.data_points[i][0];
      var tempList2 = {location: null, stopover: false }
      tempList2.location = tempList;

      if(i%4==0){
        waypointsElena.push(tempList2);
      }
    }
    // console.log("waypointsElena",waypointsElena);

    for(var i = 0; i<jsonData.path_shortest.shape.data_points.length; i++)
    {
      var tempList = {lat: 0 , lng: 0};
      tempList.lat = jsonData.path_shortest.shape.data_points[i][1];
      tempList.lng = jsonData.path_shortest.shape.data_points[i][0];
      var tempList2 = {location: null, stopover: false }
      tempList2.location = tempList;

      if(i%4==0){
        waypointsShortest.push(tempList2);
      }
    }
    // console.log("waypointsShortest", waypointsShortest);

    const requestElena = {
      origin: waypointsElena[0].location,
      destination: waypointsElena[waypointsElena.length - 1].location,
      waypoints: waypointsElena.slice(1, waypointsElena.length - 1),
      travelMode: 'WALKING'
    };
    const requestShortest = {
      origin: waypointsShortest[0].location,
      destination: waypointsShortest[waypointsShortest.length - 1].location,
      waypoints: waypointsShortest.slice(1, waypointsShortest.length - 1),
      travelMode: 'WALKING'
    }

    directionServiceElena.route(requestElena, function(response, status) {
      if (status === 'OK') {
        setDirectionsResponseElena(response);
        setIsLoading(false);
      } else {
        console.error('Directions request failed due to ' + status);
      }
    });

    directionServiceShortest.route(requestShortest, function(response, status) {
      if (status === 'OK') {
        setDirectionsResponseShortest(response);
        setIsLoading(false);
        console.log("direction response:",directionsResponseShortest);
      } else {
        console.error('Directions request failed due to ' + status);
      }
    });
  }
 
  async function handleSubmitClick(e){
    if(!isNaN(threshold) && threshold <= 100){
      setIsDisabled(true);
      setIsLoading(true);
      e.preventDefault();
      setIsHidden(false);
      fetchData(origin,destination)
      setIsPathButtonDisabled(false)
    }else {
      e.preventDefault();
      setThresholdError("Threshold must be a number and should not exceed 100");

      // Clear the threshold error after 3 seconds
      setTimeout(() => {
        setThresholdError("");
      }, 3000);
    }
  };

  useEffect(() => {
    // Action to perform after state update
    if(origin!==null && destination!==null && threshold!=="" && algorithm!=="" && elevation!=="")
    {
      setIsDisabled(false);
    }
  }, [origin,destination,threshold,algorithm,elevation, typeOfPath]);

  useEffect(() => {
    // Action to perform after state update
    console.log('State updated EleNa:', directionsResponseElena);
    console.log('State updated Shortest Path:', directionsResponseShortest);
  }, [directionsResponseElena, typeOfPath, directionsResponseShortest]);

  const resetStates = () => {
    setOrigin(null);
    setDestination(null);
    setDirectionsResponseElena(null);
    setDirectionsResponseShortest(null);
    setThreshold("");
    setAlgorithm("");
    setElevation("");
    setShortestDistanceValue(0.0000)
    setShortestDistanceGain(0.0000)
    setElenaDistanceValue(0.0000)
    setElenaDistanceGain(0.0000)
  };

  return (
  
    <form>
    <div style={{ display: 'flex', height: '100vh' }}>
      {/* Left section */}
      <div style={{ width: '35%',height:'110%', backgroundColor: 'black', padding: '10px', display: 'flex', flexDirection: 'column' }}>
        {/* Heading */}
        <Heading />
  
        {/* Inputs */}
        <div style={{ marginBottom: '10px', marginTop: '10px', color:'pink' }}>
          <Inputs  
            setHiddenState={setHiddenState}
            setDestination={setDestination} 
            setOrigin={setOrigin} 
            setThreshold={setThreshold}
            setAlgorithm={setAlgorithm}
            setElevation={setElevation}
          />
        </div>
  
        {/* Search and Reset buttons */}
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '10px' }}>
          <button onClick={handleSubmitClick} disabled={isDisabled} style={{ backgroundColor: isDisabled ? 'gray' : 'pink', color: 'black', padding: '0.5rem 1rem', border: 'none', borderRadius: '4px', cursor: 'pointer', marginRight: '1rem' }}>
            Search
          </button>
          <button onClick={resetStates} style={{ backgroundColor: 'pink', color: 'black', padding: '0.5rem 1rem', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Reset
          </button>
        </div>
  
        {/* Paths component */}
        <Paths setTypeOfPath={setTypeOfPath} isPathButtonDisabled={isPathButtonDisabled} />
  
<div>
  <span style={{ color: 'pink', marginBottom:'10px' }}>Shortest Path Metrics:</span>
  <div style={{ marginTop:'10px',backgroundColor: '#fff', color: 'black', padding: '10px', borderRadius: '2px' }}>
    {/* Metrics for EleNa Path distance */}
    <div style={{ marginBottom: '5px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>EleNa Path distance: {elenaDistanceValue.toFixed(4)}</span>
      </div>
    </div>

    {/* Metrics for EleNa Path elevation gain */}
    <div style={{ marginBottom: '5px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>EleNa Path elevation gain: {elenaDistanceGain.toFixed(4)}</span>
      </div>
    </div>

    {/* Metrics for Shortest Path distance */}
    <div style={{ marginBottom: '5px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>Shortest Path distance: {shortestDistanceValue.toFixed(4)}</span>
      </div>
    </div>

    {/* Metrics for Shortest Path elevation gain */}
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>Shortest Path elevation gain: {shortestDistanceGain.toFixed(4)}</span>
      </div>
    </div>
  </div>
</div>

      </div>
  
      {/* Right section */}
      <div style={{ width: '65%',height:'110%' }}>
        {/* Map section */}
        <div className="container" style={{ height: '100%', overflow: 'hidden' }}>
          <div className="loader-container">
            {/* Loader overlay */}
            {isLoading && (
              <div className="loader-overlay">
                <div style={{ display: 'flex', alignItems: 'center', background: '#fff', borderRadius: '8px', padding: '10px' }}>
                  <div className="spinner"></div>
                  <p style={{ textAlign: 'center', marginTop: '1rem', color: '#8a2be2', marginLeft: '10px', fontSize: '20px' }}>Loading path...</p> 
                </div>
              </div>
            )}
  
            {/* Map container */}
            <div className="half right">
              <div className="map-container">
                <GoogleMap
                  center={center}
                  zoom={15}
                  mapContainerStyle={{ height: '100%', width: '100%' }}
                >
                  {/* Conditional rendering based on type of path */}
                  {typeOfPath === 'shortest' && directionsResponseShortest ? (
                    <>
                      <DirectionsRenderer directions={directionsResponseShortest} />
                    </>
                  ) : (
                    <>
                      <DirectionsRenderer directions={directionsResponseElena} />
                    </>
                  )}
                </GoogleMap>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
  
  );
}

export default App;