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
    import {palette} from "$lib/data/palette";
    import {geoTransform, select, geoPath, arc, pie, scaleOrdinal, scaleLog} from "d3";

    export let zoom;

    export let flows_in;
    export let points_in;
    export let coords_in;

    $: flows = flows_in["0"]
    $: points = points_in["0"]
    $: coords = coords_in["0"]
    
    $: console.log(coords)

    let summedFlows
    let lineWidthScale

    $: {
        summedFlows = {}
        Object.keys(flows).forEach(key => {
            summedFlows[key] = flows[key].map((d) => {
                return {
                    total: d.un_classes.reduce(
                        (partial, current) => partial + current.value,
                        0
                    ),
                    original: d,
                };
            });
        });

        let maxFlowAmount = 0;
        for (const flow of [...summedFlows.bidirectional, ...summedFlows.unidirectional]) {
            if (flow.total > maxFlowAmount) {
                maxFlowAmount = flow.total;
            }
        }
        //console.log("maxFlowAmount: ", maxFlowAmount)
        lineWidthScale = scaleLog()
            .base(Math.E)
            .domain([0.01, maxFlowAmount]) // min and max values the trash amount can take
            .range([1, 8]); // min and max width of lines for the flows
        if (map1) {
            createLinesBetweenCountries(map1)
            createCountryDonuts(map1);
        }
    }

    const initialView = [20, 0];

    const UnClassesColorScale = scaleOrdinal()
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
                        coords[d.origin_code].coordinates,
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
        update({zoom: map1.getZoom(), center: map1.getCenter()});
    }

    function createLinesBetweenCountries(map1) {
        var d3Svg = select(map1.getPanes().overlayPane).select("svg");
        // if stuff already there, delete first
        select("#linkGroup").remove();
        select("#greyLinkGroup").remove();

        d3Svg
            .append("g")
            .attr("id", "greyLinkGroup")
            .attr("class", "leaflet-zoom-hide");

        d3Svg
            .append("g")
            .attr("id", "linkGroup")
            .attr("class", "leaflet-zoom-hide");
        const greyLinks = d3Svg
            .select("#greyLinkGroup")
            .selectAll("line")
            .data(summedFlows.unidirectional)
            .enter()
            .append("line")
            .attr("stroke-width", 1)
            .attr("stroke", "#525252")
            .style("stroke-dasharray", ("3, 3"));

        const coloredLinks = d3Svg
            .select("#linkGroup")
            .selectAll("line")
            .data([...summedFlows.bidirectional, ...summedFlows.unidirectional])
            .enter()
            .append("line")
            .attr("stroke-width", d => lineWidthScale(d.total))
            .attr("stroke", function (d) {
                const max = d.original.un_classes.reduce((prev, current) =>
                    prev.value > current.value ? prev : current
                );
                return UnClassesColorScale(max.label);
            });

        function mapGeometry(link, zoom, center, zeroflow = false) {
            var radius = 20;
            if (zeroflow === false) {
                var coords1 = map1._latLngToNewLayerPoint(
                    coords[link.original.origin_code].coordinates,
                    zoom,
                    center
                );
                var coords2 = map1._latLngToNewLayerPoint(
                    coords[link.original.destination_code].coordinates,
                    zoom,
                    center
                );
            } else { // change the direction of the relationship between the two nodes destination and origin
                var coords1 = map1._latLngToNewLayerPoint(
                    coords[link.original.destination_code].coordinates,
                    zoom,
                    center
                );
                var coords2 = map1._latLngToNewLayerPoint(
                    coords[link.original.origin_code].coordinates,
                    zoom,
                    center
                );
            }

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
            return {coords1: newCoords1, coords2: newCoords2};
        }

        function update(e) {
            // update grey links before colored links, so they are underneath them
            greyLinks
                .attr("x1", (d) => mapGeometry(d, e.zoom, e.center, true).coords1.x)
                .attr("y1", (d) => mapGeometry(d, e.zoom, e.center, true).coords1.y)
                .attr("x2", (d) => mapGeometry(d, e.zoom, e.center, true).coords2.x)
                .attr("y2", (d) => mapGeometry(d, e.zoom, e.center, true).coords2.y);

            coloredLinks
                .attr("x1", (d) => mapGeometry(d, e.zoom, e.center).coords1.x)
                .attr("y1", (d) => mapGeometry(d, e.zoom, e.center).coords1.y)
                .attr("x2", (d) => mapGeometry(d, e.zoom, e.center).coords2.x)
                .attr("y2", (d) => mapGeometry(d, e.zoom, e.center).coords2.y);
        }

        map1.on("zoomanim", (e) => update(e));
        update({zoom: map1.getZoom(), center: map1.getCenter()});
    }

    let map1;

    function onMount(container) {
        map1 = createMap(container);
        svg({clickable: true}).addTo(map1);

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
            map1.on("zoomend", function (e) { zoom = map1.getZoom()  });
            createLinesBetweenCountries(map1);
            createCountryDonuts(map1);
        }
    }

</script>

<svelte:window on:resize={resizeMap}/>

<link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
        integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI="
        crossorigin=""
/>
<div id="map" class="w-100 h-full" use:onMount/>

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
