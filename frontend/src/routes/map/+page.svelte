<script>
    import {control, divIcon, DomUtil, layerGroup, map, polyline, tileLayer, LatLng} from "leaflet";
    import * as markerIcons from './markers.js';

    import {geoTransform, select, geoPath} from "d3";

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
        let m = map(container, {preferCanvas: false}).setView(initialView, 2);
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

    const rawJson = {
        "type": "FeatureCollection", "features": [
            {
                "type": "Feature",
                "id": "01",
                "properties": {"name": "Alabama"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [-87.359296, 35.00118]
                }
            },
            {
                "type": "Feature",
                "id": 2,
                "properties": {"name": "Brazil"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [-49.2712, -25.4296]
                }
            }
        ]
    }

    const otherPoints = {
        "type": "FeatureCollection", "features": [
            {
                "type": "Feature",
                "id": "01",
                "properties": {"name": "Germany"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [51.1334813439932, 10.0183432948567]
                }
            },
            {
                "type": "Feature",
                "id": 2,
                "properties": {"name": "France"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [47.8249046208979, 2.61878695312962]
                }
            }
        ]
    }

    function createPoints(map1) {
        var d3Svg2 = select(map1.getPanes().overlayPane).select("svg")
        var g = d3Svg2.append("g").attr("class", "leaflet-zoom-hide")
        var feature = g.selectAll("circle").data(otherPoints.features).enter().append("circle")
            .style("fill", "teal")

        function update() {
            feature.attr("cx",function(d) {console.log(d, map1.latLngToLayerPoint(d.geometry.coordinates), map1.latLngToLayerPoint(d.geometry.coordinates).x ); return map1.latLngToLayerPoint(d.geometry.coordinates).x})
            feature.attr("cy",function(d) { return map1.latLngToLayerPoint(d.geometry.coordinates).y})
            feature.attr("r",function(d) { return 1*Math.pow(2, map1.getZoom())})
        }
        map1.on("zoom", update);
        update();
    }

    function createPaths(map1) {
        var d3Svg = select(map1.getPanes().overlayPane).append("svg")
        var g = d3Svg.append("g").attr("class", "leaflet-zoom-hide")

        //d3.json("us-states.json", function(error, collection) {
        //    if (error) throw error;

        // code here
        //       });
        function projectPoint(x, y) {
            const point = map1.latLngToLayerPoint(new LatLng(y, x));
            this.stream.point(point.x, point.y);
        }

        const transform = geoTransform({point: projectPoint})
        const path = geoPath().projection(transform);
        const feature = g.selectAll("path")
            .data(rawJson.features)
            .enter().append("path");

        map1.on('zoomend', reset);
        reset();

        function reset() {
            //console.log("Reset called")
            const bounds = path.bounds(rawJson)
            const topLeft = bounds[0]
            const bottomRight = bounds[1];

            d3Svg.attr("width", bottomRight[0] - topLeft[0])
                .attr("height", bottomRight[1] - topLeft[1])
                .style("left", topLeft[0] + "px")
                .style("top", topLeft[1] + "px");

            g.attr("transform", "translate(" + -topLeft[0] + "," + -topLeft[1] + ")");
            feature.attr("d", path);
        }
    }

    let map1

    function onMount(container) {
        map1 = createMap(container);
        const lineLayers = createLines();
        lineLayers.addTo(map1);
        createPaths(map1 = map1)

        createPoints(map1)

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