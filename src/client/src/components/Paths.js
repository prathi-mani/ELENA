import React, { useState } from 'react';

export const Paths = (props) => {

  function handleMapClickElena(e)
  {
    props.setTypeOfPath("elena");

  }
  function handleMapClickShortest(e)
  {
    props.setTypeOfPath("shortest");
  }

    return (
      
      <div style={{ backgroundColor: 'black', display: "flex", justifyContent: "center", alignItems: "center", paddingTop: "10px", marginBottom:'10px' }}>
  <div style={{ marginRight: '8px' }}></div> {/* Add spacing */}
  {/* EleNa Path */}
  <div onClick={handleMapClickElena} disabled={props.isPathButtonDisabled} style={{ backgroundColor: props.isPathButtonDisabled ? 'grey' : "pink", color: "black", padding: "8px 16px", border: "none", borderRadius: "4px", cursor: "pointer", marginRight: '20px' }}>Elena Path</div>

  {/* Shortest Path */}
  <div onClick={handleMapClickShortest} disabled={props.isPathButtonDisabled} style={{ backgroundColor: props.isPathButtonDisabled ? 'grey' : "pink", color: "black", padding: "8px 16px", border: "none", borderRadius: "4px", cursor: "pointer", marginRight: '8px' }}>Shortest Path</div>
</div>


    );
  }
