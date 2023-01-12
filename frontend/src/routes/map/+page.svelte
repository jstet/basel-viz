<script>
    import {control, divIcon, DomUtil, layerGroup, map, polyline, tileLayer} from "leaflet";
    import * as markerIcons from './markers.js';
    import * as d3 from "d3"


    const markerLocations = [
        [29.8283, -96.5795],
        [37.8283, -90.5795],
        [43.8283, -102.5795],
        [48.40, -122.5795],
        [43.60, -79.5795],
        [36.8283, -100.5795],
        [38.40, -122.5795],
    ];

    const initialView = [39.8283, -98.5795];

    function createMap(container) {
        let m = map(container, {preferCanvas: false}).setView(initialView, 4);
        tileLayer(
            'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
            {
                attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,
    &copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`,
                subdomains: 'abcd',
                maxZoom: 14,
            }
        ).addTo(m);

        return m;
    }

    function createLines() {
        return polyline(markerLocations, {color: '#E4E', opacity: 0.5, weight: 5});
    }

    let lineLayers;

    function createGlyphs(map1) {
        var d3Svg = d3.select(map1.getPanes().overlayPane).append("svg")
        var g = d3Svg.append("g").attr("class", "leaflet-zoom-hide")

        d3.json("us-states.json", function(error, collection) {
            if (error) throw error;

            // code here
        });
        function projectPoint(x, y) {
            var point = map.latLngToLayerPoint(new L.LatLng(y, x));
            this.stream.point(point.x, point.y);
        }
    }

    function onMount(container) {
        let map1 = createMap(container);

        lineLayers = createLines();
        lineLayers.addTo(map1);
        createGlyphs(map1 = map1)

        return {
            destroy: () => {
                map1.remove();
                map1 = null;
            }
        };
    }

    function resizeMap() {
        if (map1) {
            map1.invalidateSize();
        }
    }


</script>
<svelte:window on:resize={resizeMap}/>

<style>
    .map :global(.marker-text) {
        width: 100%;
        text-align: center;
        font-weight: 600;
        background-color: #444;
        color: #EEE;
        border-radius: 0.5rem;
    }

    #map {
        width: 100%;
        height: 700px;
        width: 1300px;
    }

    .map :global(.map-marker) {
        width: 30px;
        transform: translateX(-50%) translateY(-25%);
    }
</style>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
      integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI="
      crossorigin=""/>
<div id="map" class="map" use:onMount/>