import React, { useRef, useState, useEffect } from 'react';
import { MapComponent } from './MapComponent';


export const Inputs = (props) => {
  const [sourceLocation, setSourceLocation] = useState('');
  const [destinationLocation, setDestinationLocation] = useState('');

  function handleSourceChange(event) {
    setSourceLocation(event.target.value);
    }

  function handleDestinationChange(event) {
    setDestinationLocation(event.target.value);
  }
  function handlePathLimit(event) {
    props.setThreshold(event.target.value);
  }
  
  function onValueChangeElevation(event) {
    props.setElevation(event.target.value);
  }
  function onValueChangeAlgorithm(event) {
    props.setAlgorithm(event.target.value);
  }

    const autoCompleteRefSource = useRef();
    const inputRefSource = useRef();
    const autoCompleteRefDest = useRef();
    const inputRefDest = useRef();
    const options = {
    fields: ["address_components", "geometry", "icon", "name"],
    }

    useEffect(() => {
     autoCompleteRefSource.current = new window.google.maps.places.Autocomplete(
      inputRefSource.current,
      options
     );
     autoCompleteRefSource.current.addListener("place_changed", async function () {
        const source = await autoCompleteRefSource.current.getPlace();
        console.log({ source });
        setSourceLocation(source);
        props.setOrigin(source);

       });
    
       autoCompleteRefDest.current = new window.google.maps.places.Autocomplete(
        inputRefDest.current,
        options
       );
       autoCompleteRefDest.current.addListener("place_changed", async function () {
          const dest = await autoCompleteRefDest.current.getPlace();
          setDestinationLocation(dest)
          props.setDestination(dest);
          console.log({ dest });
         });

    }, []);

  return (
    <form className = "input_forms">
    <div> 
        {/* <text style={{ marginLeft: '1rem'}}> Source </text> */}
        <input 
        style={{
          marginLeft: '1rem',
          padding: '0.5rem',
          borderRadius: '0px',
          border: '2px solid #000',
          outline: 'none',
          fontSize: '14px',
          width: '160px', 
          boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
        }}
        ref= {inputRefSource}
        id = "source"
          label="source"
          type="address" required
          name="source"
          onChange={handleSourceChange}
          placeholder="Enter Source"
          className="mbsc-col-12 mbsc-col-lg-6"
        />
        {/* <text style={{ marginLeft: '1rem'}}> Destination </text> */}
        <input
          style={{
            marginLeft: '1rem',
            padding: '0.5rem',
            borderRadius: '0px',
            border: '2px solid #000',
            outline: 'none',
            fontSize: '14px',
            width: '160px', 
            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
          }}
          ref= {inputRefDest}
          label="destination"
          type="address"
          name="destination"
          onChange={handleDestinationChange}
          placeholder="Enter Destination"
        />


        {/* <text style={{ marginLeft: '1rem'}}> Elevation </text> */}
        <input
          style={{
            marginLeft: '1rem',
            padding: '0.5rem',
            borderRadius: '0px',
            border: '2px solid #000',
            outline: 'none',
            fontSize: '14px',
            marginTop:'10px',
            width: '160px', 
            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
          }}
          type="integer"
          name="pathLimit"
          onChange={handlePathLimit}
          placeholder="Enter path limit (Max 100)"
        />

        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginTop: "10px" }}>
          <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
            <div style={{ marginRight: "1rem" }}>Choose elevation:</div>
            <div data-testid="elevation">
            <input data-testid="min" type="radio" value="min" name="elevationType" onChange = {onValueChangeElevation} style={{ marginRight: "0.1rem" }} /> Minimum  
            <input data-testid="max" type="radio" value="max" name="elevationType" onChange = {onValueChangeElevation} style={{ marginLeft:"1rem",marginRight: "0.1rem" }} /> Maximum 
            </div>
          </div>
          <div style={{ display: "flex", alignItems: "center" }}>
            <div style={{ marginRight: "1rem" }}>Choose the Algorithm:</div>
            <div data-testid="options">
            <input data-testid="astar" type="radio" value="AStar" name="AlgorithmType" id="astar" onChange = {onValueChangeAlgorithm} style={{ marginRight: "0.1rem" }} /> 
            <label>A* </label>
            <input data-testid="dijkstra" type="radio" value="Dijkstra" name="AlgorithmType" id="dijkstra" onChange = {onValueChangeAlgorithm} style={{marginRight: "0.1rem" }} /> 
            <label>Dijkstra </label>
            </div>
          </div>
        </div>

    </div>

    </form>
  );

  }
