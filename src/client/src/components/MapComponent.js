import React, { useState } from 'react';
import GoogleMapReact from 'google-map-react'
import { Icon } from '@iconify/react'
import locationIcon from '@iconify/icons-mdi/map-marker'
import MyMarker from "./MyMarker";
import "./marker.css";
import {
  useJsApiLoader,
  GoogleMap,
  Marker,
  Autocomplete,
  DirectionsRenderer,
} from '@react-google-maps/api'

const center = { lat: 44.564588, lng: -123.275705}



export const MapComponent = () =>  {   

  
return(


  <div style={{ height: '400px', width: '900px' }}>;
  <GoogleMap
        data-testid="map"
        center={center}
        zoom={15}
        mapContainerStyle={{ width: '100%', height: '100%' }}>
        <Marker data-testid="marker" position={center} /> 
        

  </GoogleMap>
  
</div>


)
}
