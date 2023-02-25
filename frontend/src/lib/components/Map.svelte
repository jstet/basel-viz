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
        GeoJSON,
        svg,
    } from "leaflet";
    import { palette } from "$lib/data/palette";
    import { geoTransform, select, geoPath, arc, pie, scaleOrdinal } from "d3";

    import countries from "$lib/geojson/countries.json";

    export let flows;
    export let points;

    let bidirectional;
    let unidirectional;
    $: bd = flows.bidirectional
    $: ud = flows.unidirectional

    let filterdFlows = [];
    let maxFlowAmount;
    let mappedFlows;

    $:console.log(ud)

    
    $: {
        filterdFlows = flows.filter(
            (d) => d.origin_code !== d.destination_code
        );

        mappedFlows = filterdFlows.map((d) => {
            return {
                total: d.un_classes.reduce(
                    (partial, current) => partial + current.value,
                    0
                ),
                original: d,
            };
        });
        maxFlowAmount = mappedFlows.reduce((prev, current) =>
            prev.total > current.total ? prev : current
        );
        if (map1) {
            createLinesBetweenCountries(map1);
            createCountryDonuts(map1);
        }
    }

    const initialView = [20, 0];

    var UnClassesColorScale = scaleOrdinal()
        .domain(palette.labels)
        .range(palette.colors); // bold from carto.com

    function createMap(container) {
        // Setting initial position and zoom of map and restricting zoom
        let m = map(container, {
            preferCanvas: false,
            maxZoom: 9,
            minZoom: 3,
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

    function createCountryDonuts(map1) {
        //Adds a svg to the map which always contains all the things we add into it
        var d3Svg = select(map1.getPanes().overlayPane).select("svg");
        // if stuff already there, delete first
        select("#donutGroup").remove();

        d3Svg.append("g").attr("id", "donutGroup");
        var donutGroups = d3Svg
            .select("#donutGroup")
            .selectAll("g")
            .data(points)
            .enter()
            .append("g");

        // pie generator
        var pie1 = pie()
            .sort(null)
            .value(function (d) {
                return d.value;
            });

        //slices
        var slice1 = donutGroups
            .selectAll("path")
            //.data(d => pie1(d.properties.un_classes))
            .data((d) => pie1(d.un_classes))
            .enter()
            .append("path")
            .attr("fill", function (d) {
                return UnClassesColorScale(d.data.label);
            });

        function update(e) {
            var radius = 20;
            ///0.5 * Math.pow(2,e.zoom);

            //arc generator
            var arc1 = arc()
                .innerRadius(radius * 0.5)
                .outerRadius(radius);

            donutGroups.selectAll("path").attr("d", arc1);
            donutGroups
                .attr("style", function (d) {
                    var coord = map1._latLngToNewLayerPoint(
                        countries[d.origin_code].coordinates,
                        e.zoom,
                        e.center
                    );
                    return (
                        "transform: translate(" +
                        coord.x +
                        "px," +
                        coord.y +
                        "px)"
                    );
                })
                .attr("class", "leaflet-zoom-hide");
        }

        map1.on("zoomanim", (e) => update(e));
        update({ zoom: map1.getZoom(), center: map1.getCenter() });
    }

    function createLinesBetweenCountries(map1) {
        var d3Svg = select(map1.getPanes().overlayPane).select("svg");
        // if stuff already there, delete first
        select("#linkGroup").remove();
        d3Svg
            .append("g")
            .attr("id", "linkGroup")
            .attr("class", "leaflet-zoom-hide");

        const feature = d3Svg
            .select("#linkGroup")
            .selectAll("line")
            .data(filterdFlows)
            .enter()
            .append("line")
            .attr("stroke-width", 1)
            .attr("stroke", function (d) {
                const max = d.un_classes.reduce((prev, current) =>
                    prev.value > current.value ? prev : current
                );
                return UnClassesColorScale(max.label);
            });

        function mapGeometry(link, zoom, center) {
            var radius = 20;
            var coords1 = map1._latLngToNewLayerPoint(
                countries[link.origin_code].coordinates,
                zoom,
                center
            );
            var coords2 = map1._latLngToNewLayerPoint(
                countries[link.destination_code].coordinates,
                zoom,
                center
            );
            var directionVector = {
                x: coords2.x - coords1.x,
                y: coords2.y - coords1.y,
            };
            var lengthOfVector = Math.sqrt(
                directionVector.x ** 2 + directionVector.y ** 2
            );
            directionVector.x = directionVector.x / lengthOfVector;
            directionVector.y = directionVector.y / lengthOfVector;
            var newCoords1 = {
                x: coords1.x + directionVector.x * radius,
                y: coords1.y + directionVector.y * radius,
            };
            var newCoords2 = {
                x: coords1.x + (coords2.x - coords1.x) / 2,
                y: coords1.y + (coords2.y - coords1.y) / 2,
            };
            if (
                isNaN(newCoords1.x) ||
                isNaN(newCoords2.x) ||
                isNaN(newCoords1.y) ||
                isNaN(newCoords2.y)
            )
                console.log(
                    link,
                    coords1,
                    coords2,
                    directionVector,
                    lengthOfVector,
                    newCoords1,
                    newCoords2
                );
            return { coords1: newCoords1, coords2: newCoords2 };
        }

        function update(e) {
            feature
                .attr("x1", (d) => mapGeometry(d, e.zoom, e.center).coords1.x)
                .attr("y1", (d) => mapGeometry(d, e.zoom, e.center).coords1.y)
                .attr("x2", (d) => mapGeometry(d, e.zoom, e.center).coords2.x)
                .attr("y2", (d) => mapGeometry(d, e.zoom, e.center).coords2.y);
        }

        map1.on("zoomanim", (e) => update(e));
        update({ zoom: map1.getZoom(), center: map1.getCenter() });
    }

    let map1;

    function onMount(container) {
        map1 = createMap(container);
        svg({ clickable: true }).addTo(map1);

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

    $: {
        if (map1) {
            createLinesBetweenCountries(map1);
            createCountryDonuts(map1);
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

<style global>
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

    :global(.leaflet-zoom-anim #donutGroup > g) {
        transition: transform 0.25s cubic-bezier(0, 0, 0.25, 1);
    }
</style>
