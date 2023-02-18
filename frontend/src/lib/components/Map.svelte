<script>
    import {
        control,
        divIcon,
        DomUtil,
        layerGroup,
        map,
        polyline,
        tileLayer,
        LatLng,
        svg
    } from "leaflet";

    import { geoTransform, select, geoPath, arc, pie, scaleOrdinal } from "d3";

    import countries from "$lib/geojson/countries.json"

    const initialView = [20, 0];

    function createMap(container) {
        // Setting initial position and zoom of map and restricting zoom posibilites
        let m = map(container, {
            preferCanvas: false,
            maxZoom: 8,
            minZoom: 2,
            maxBounds: [
                //south west
                [-90, -200],
                //north east
                [90, 200],
            ],
        }).setView(initialView, 3);
        // available basemaps: https://leaflet-extras.github.io/leaflet-providers/preview/
        tileLayer(
            "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
            {
                attribution:
                    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: "abcd",
                maxZoom: 20,
            }
        ).addTo(m);
        return m;
    }
    function createPoints(map1) {
        var data2 = [{
                    "type": "Feature",
                    "properties": {
                        "name": "Andorra",
                        "code": "ad",
                        "un_classes": [
                            { label: "B", value: 20 },
                            { label: "C", value: 30 },
                            { label: "D", value: 25 },
                            { label: "A", value: 10 },
                            { label: "E", value: 50 },
                            { label: "F", value: 15 },
                        ]
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            42.5486542501806,
                            1.57676643468505
                        ]
                    }
                }]
        //Adds a svg to the map which always contains all the things we add into it
        svg({clickable:true}).addTo(map1)
        var d3Svg = select(map1.getPanes().overlayPane).select("svg")
        d3Svg.append("g").attr("id", "donutGroup")
        var donutGroups = d3Svg.select("#donutGroup").selectAll("g").data(countries.features).enter().append("g")

        var colorScale = scaleOrdinal()
            .range(["#7F3C8D","#11A579","#3969AC","#F2B701","#E73F74","#80BA5A","#E68310",
                    "#008695","#CF1C90","#f97b72","#4b4b8f","#A5AA99"]) // bold from carto.com

        //arc generator


        // pie generator
        var pie1 = pie()
            .sort(null)
            .value(function(d) {return d.value});


        //slices
        var slice1 = donutGroups.selectAll("path")
            //.data(d => pie1(d.properties.un_classes))
            .data(pie1(data2[0].properties.un_classes))
            .enter()
            .append("path")
            .attr("fill", function(d) { return colorScale(d.data.label); });


        function update(e) {
            var radius = 20;
                ///0.5 * Math.pow(2,e.zoom);

            var arc1 = arc()
                .innerRadius(radius*0.5)
                .outerRadius(radius);

            donutGroups.selectAll("path")
                .attr("d", arc1)

            donutGroups.attr("style", function (d) {
                var coord = map1._latLngToNewLayerPoint(d.geometry.coordinates, e.zoom, e.center);
                return 'transform: translate('+coord.x+'px,'+coord.y+'px)';
            })
            /*
            slice1.attr("cx", function (d) {
                // console.log(
                //     d,
                //     map1.latLngToLayerPoint(d.geometry.coordinates),
                //     map1.latLngToLayerPoint(d.geometry.coordinates).x
                // );
                return map1.latLngToLayerPoint(d.geometry.coordinates).x;
            });
            slice1.attr("cy", function (d) {
                return map1.latLngToLayerPoint(d.geometry.coordinates).y;
            });
            feature.attr("r", function (d) {
                return 1 * Math.pow(2, map1.getZoom());
            });*/
        }
        map1.on("zoomanim", e => update(e));
        update({"zoom":map1.getZoom(), "center": map1.getCenter()});
    }
    function createLinesBetweenCountries(map1){
        var d3Svg = select(map1.getPanes().overlayPane).select("svg")
        d3Svg.append("g").attr("id", "pathGroup")
        var pathGroups = d3Svg.select("#pathGroup").selectAll("g").data(countries.features).enter().append("g")

        function selectRandomNotGiven(length, index){

            Math.floor(Math.random() * length)
        }



        const feature = pathGroups
            .selectAll("line")
            .data((datum, index) => {return [[datum, countries.features[Math.floor(Math.random() * countries.features.length)], countries.features[Math.floor(Math.random() * countries.features.length)]]]})
            .enter()
            .append("line")
            .attr("stroke-width", 1)
            .attr("stroke", "black");
/*
        const areaPaths = pathGroups.append("path")
            .attr('fill-opacity', 0.3)
            .attr('stroke', 'black')
            .attr("z-index", 3000)
            .attr('stroke-width', 2.5)
            .attr("d", (d,i) => console.log(d, i ))
*/

        function mapGeometry(countries, zoom, center){
            var radius = 20
            var cords1 = map1._latLngToNewLayerPoint(countries[0].geometry.coordinates, zoom, center)
            var cords2 = map1._latLngToNewLayerPoint(countries[1].geometry.coordinates, zoom, center)
            var directionVector = {"x": (cords2.x - cords1.x), "y": (cords2.y - cords1.y)};
            var lengthOfVector = Math.sqrt(directionVector.x**2 + directionVector.y**2)
            directionVector.x = directionVector.x/lengthOfVector;
            directionVector.y = directionVector.y/lengthOfVector;
            var newCords1 = {"x": cords1.x + directionVector.x * radius, "y": cords1.y + directionVector.y * radius};
            var newCords2 = {"x": cords2.x - directionVector.x * radius, "y": cords2.y - directionVector.y * radius};
            return {"chords1": newCords1, "chords2" : newCords2}
        }

        function update(e) {
            //var chords = map1.latLngToLayerPoint()

            //var coord = map1._latLngToNewLayerPoint(d.geometry.coordinates, e.zoom, e.center);
            feature
                .attr("x1", d => mapGeometry(d,e.zoom, e.center).chords1.x)
                .attr("y1", d => mapGeometry(d,e.zoom, e.center).chords1.y)
                .attr("x2", d => mapGeometry(d,e.zoom, e.center).chords2.x)
                .attr("y2", d => mapGeometry(d,e.zoom, e.center).chords2.y);

        }
        map1.on("zoomanim", e => update(e));
        update({"zoom":map1.getZoom(), "center": map1.getCenter()});
    }

    let map1;

    function onMount(container) {
        map1 = createMap(container);
        createPoints(map1);
        createLinesBetweenCountries(map1)

        return {
            destroy: () => {
                map1.remove();
                map1 = null;
            },
        };
    }

    function resizeMap() {
        if (map1) {
            map1.invalidateSize();
        }
    }
</script>

<svelte:window on:resize={resizeMap} />

<link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
    integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI="
    crossorigin=""
/>
<div id="map" class="w-100 h-full" use:onMount />

<style>
    .map :global(.marker-text) {
        width: 100%;
        text-align: center;
        font-weight: 600;
        background-color: #444;
        color: #eee;
        border-radius: 0.5rem;
    }

    .map :global(.map-marker) {
        width: 30px;
        transform: translateX(-50%) translateY(-25%);
    }
    .leaflet-zoom-anim .svg-zoom-animated > g {
        width: 2000px;
        transition: transform 0.25s cubic-bezier(0,0,0.25,1);
    }
</style>
