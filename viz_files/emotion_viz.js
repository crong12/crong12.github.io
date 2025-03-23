// Set the dimensions and margins of the graph
const margin = {top: 20, right: 30, bottom: 150, left: 50}, // Increased bottom margin for slider and buttons
      width = 1000 - margin.left - margin.right,
      height = 600 - margin.top - margin.bottom;

// Append the svg object to the div
const svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Parse the Data
d3.json("/viz_files/emotion_counts.json").then(function(data) {
    // List of emotions = keys in the JSON excluding "episode"
    const keys = Object.keys(data[0]).filter(k => k !== "episode");
    
    // Get episode range
    const episodeMin = d3.min(data, d => d.episode);
    const episodeMax = d3.max(data, d => d.episode);
    
    // Initialize filter range to show all episodes
    let filterRange = [episodeMin, episodeMax];
    
    // Define One Piece arcs with episode ranges
    const arcs = [
        { name: "Enies Lobby", start: 293, end: 312 },
        { name: "Thriller Bark", start: 337, end: 377 },
        { name: "Sabaody", start: 385, end: 405 },
        { name: "Amazon Lily", start: 408, end: 417 },
        { name: "Impel Down", start: 422, end: 452 },
        { name: "Marineford", start: 457, end: 489 },
        { name: "Fishman Island", start: 523, end: 574 },
        { name: "Punk Hazard", start: 579, end: 628 },
        { name: "Dressrosa", start: 629, end: 746 },
        { name: "Zou", start: 751, end: 774 },
    ];

    // Create main visualization functions
    function createVisualization(filteredData) {
        // Clear previous visualization elements
        svg.selectAll(".main-viz").remove();
        
        const mainViz = svg.append("g").attr("class", "main-viz");
    
        // Add X axis
        const x = d3.scaleLinear()
            .domain([filterRange[0], filterRange[1]])
            .range([0, width]);
            
        const xAxis = mainViz.append("g")
            .attr("transform", `translate(0,${height * 1})`) 
            .call(d3.axisBottom(x).tickSize(-height * 0.8).ticks(20)) 
            .attr("class", "x-axis");
            
        xAxis.select(".domain").remove();
        // Customization
        xAxis.selectAll(".tick line").attr("stroke", "#b8b8b8");
    
        // Add X axis label
        mainViz.append("text")
            .attr("text-anchor", "end")
            .attr("x", width)
            .attr("y", height+30) 
            .text("Episode Number");
    
        // Add Y axis (optional for streamgraph, but included for reference)
        const y = d3.scaleLinear()
            .domain([-d3.max(filteredData, d => d3.sum(keys, k => d[k])) / 2, 
                    d3.max(filteredData, d => d3.sum(keys, k => d[k])) / 2])
            .range([height, 0]); // Y range remains tied to full height
    
        // Color palette
        const color = d3.scaleOrdinal()
            .domain(keys)
            .range(d3.schemeDark2);
    
        // Stack the data with streamgraph offset
        const stackedData = d3.stack()
            .offset(d3.stackOffsetSilhouette)
            .keys(keys)
            (filteredData);
    
        // Create a tooltip
        const Tooltip = mainViz
            .append("text")
            .attr("x", 10)
            .attr("y", 20)
            .style("opacity", 0)
            .style("font-size", "17px");
    
        // Tooltip functions
        const mouseover = function(event, d) {
            Tooltip.style("opacity", 1);
            d3.selectAll(".myArea").style("opacity", 0.2);
            d3.select(this)
                .style("stroke", "black")
                .style("opacity", 1);
        };
        const mousemove = function(event, d) {
            Tooltip.text(d.key);
        };
        const mouseleave = function(event, d) {
            Tooltip.style("opacity", 0);
            d3.selectAll(".myArea").style("opacity", 1).style("stroke", "none");
        };
    
        // Area generator
        const area = d3.area()
            .x(d => x(d.data.episode))
            .y0(d => y(d[0]))
            .y1(d => y(d[1]))
            .curve(d3.curveCatmullRom); // Smooth streamgraph curves
    
        // Show the areas
        mainViz.selectAll("mylayers")
            .data(stackedData)
            .join("path")
            .attr("class", "myArea")
            .style("fill", d => color(d.key))
            .attr("d", area)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave);
    }

    // Function to update the filter range and redraw visualization
    function updateFilterRange(start, end) {
        // Update the range
        filterRange = [start, end];
        
        // Update slider handles and labels
        updateHandles();
        
        // Update visualization
        const filteredData = data.filter(d => 
            d.episode >= filterRange[0] && d.episode <= filterRange[1]
        );
        createVisualization(filteredData);
    }

    // Create the range slider
    function createRangeSlider() {
        const sliderHeight = 50;
        
        // Create a scale for the slider
        const sliderScale = d3.scaleLinear()
            .domain([episodeMin, episodeMax])
            .range([0, width])
            .clamp(true);
            
        // Create slider group
        const slider = svg.append("g")
            .attr("class", "slider")
            .attr("transform", `translate(0,${height + 80})`);
            
        // Add slider track
        slider.append("line")
            .attr("class", "track")
            .attr("x1", sliderScale.range()[0])
            .attr("x2", sliderScale.range()[1])
            .attr("stroke", "#ccc")
            .attr("stroke-width", 10)
            .attr("stroke-linecap", "round");
            
        // Add slider active track (between handles)
        const activeTrack = slider.append("line")
            .attr("class", "track-active")
            .attr("x1", sliderScale(filterRange[0]))
            .attr("x2", sliderScale(filterRange[1]))
            .attr("stroke", "#6a51a3")
            .attr("stroke-width", 10)
            .attr("stroke-linecap", "round");
            
        // Define drag behavior
        const drag = d3.drag()
            .on("start", function(event, d) {
                d3.select(this).raise().attr("stroke", "black");
            })
            .on("drag", function(event, d) {
                // Get handle index from the data
                const handleIndex = d.index;
                
                // Get new position value
                const newValue = sliderScale.invert(event.x);
                
                // Update range with constraints
                if (handleIndex === 0 && newValue < filterRange[1]) {
                    filterRange[0] = Math.max(episodeMin, newValue);
                } else if (handleIndex === 1 && newValue > filterRange[0]) {
                    filterRange[1] = Math.min(episodeMax, newValue);
                }
                
                // Update handle positions
                updateHandles();
                
                // Update visualization
                const filteredData = data.filter(d => 
                    d.episode >= filterRange[0] && d.episode <= filterRange[1]
                );
                createVisualization(filteredData);
                
                // Reset active button state
                d3.selectAll(".arc-button").classed("active", false);
            })
            .on("end", function() {
                d3.select(this).attr("stroke", "#333");
            });
            
        // Create slider handles
        const handles = slider.selectAll(".handle")
            .data([{value: filterRange[0], index: 0}, {value: filterRange[1], index: 1}])
            .enter()
            .append("circle")
            .attr("class", "handle")
            .attr("cx", d => sliderScale(d.value))
            .attr("cy", 0)
            .attr("r", 8)
            .attr("fill", "white")
            .attr("stroke", "#333")
            .attr("stroke-width", 2)
            .call(drag);
            
        // Add labels showing current values
        const labels = slider.selectAll(".label")
            .data([{value: filterRange[0], index: 0}, {value: filterRange[1], index: 1}])
            .enter()
            .append("text")
            .attr("class", "label")
            .attr("x", d => sliderScale(d.value))
            .attr("y", -15)
            .attr("text-anchor", "middle")
            .text(d => Math.round(d.value));
            
        // Function to update handle and label positions
        window.updateHandles = function() {
            slider.selectAll(".handle")
                .data([{value: filterRange[0], index: 0}, {value: filterRange[1], index: 1}])
                .attr("cx", d => sliderScale(d.value));
                
            slider.selectAll(".label")
                .data([{value: filterRange[0], index: 0}, {value: filterRange[1], index: 1}])
                .attr("x", d => sliderScale(d.value))
                .text(d => Math.round(d.value));
                
            activeTrack
                .attr("x1", sliderScale(filterRange[0]))
                .attr("x2", sliderScale(filterRange[1]));
        }
        
        // Add title for the slider
        slider.append("text")
            .attr("x", width / 2)
            .attr("y", -20)
            .attr("text-anchor", "middle")
            .style("font-size", "14px")
            .text("Episode Range Filter");
    }
    
    // Create the arc preset buttons
    function createArcButtons() {
        // Create container for buttons
        const buttonContainer = d3.select("#my_dataviz")
            .append("div")
            .attr("class", "arc-buttons-container")
            .style("width", `${width}px`)
            .style("margin-left", `${margin.left}px`)
            .style("margin-top", "10px")
            .style("display", "flex")
            .style("flex-wrap", "wrap")
            .style("gap", "8px")
            .style("justify-content", "center");
        
        // Add a title
        buttonContainer.append("div")
            .style("width", "100%")
            .style("text-align", "center")
            .style("margin-bottom", "8px")
            .style("font-weight", "bold")
            .text("Arc Selection");
        
        // Add "All Episodes" button
        buttonContainer.append("button")
            .attr("class", "arc-button active")
            .style("padding", "6px 12px")
            .style("background-color", "#f0f0f0")
            .style("border", "1px solid #ccc")
            .style("border-radius", "4px")
            .style("cursor", "pointer")
            .style("font-size", "12px")
            .html("All Episodes")
            .on("click", function() {
                updateFilterRange(episodeMin, episodeMax);
                
                // Update active button state
                d3.selectAll(".arc-button").classed("active", false);
                d3.select(this).classed("active", true);
            });
        
        // Add arc buttons
        arcs.forEach(arc => {
            buttonContainer.append("button")
                .attr("class", "arc-button")
                .style("padding", "6px 12px")
                .style("background-color", "#f0f0f0")
                .style("border", "1px solid #ccc")
                .style("border-radius", "4px")
                .style("cursor", "pointer")
                .style("font-size", "12px")
                .html(`${arc.name}<br/>(${arc.start}-${arc.end})`)
                .on("click", function() {
                    updateFilterRange(arc.start, arc.end);
                    
                    // Update active button state
                    d3.selectAll(".arc-button").classed("active", false);
                    d3.select(this).classed("active", true);
                });
        });
        
        // Add some CSS for active state
        const style = document.createElement('style');
        style.textContent = `
            .arc-button.active {
                background-color: #6a51a3 !important;
                color: white !important;
                border-color: #4a3183 !important;
            }
            .arc-button:hover {
                background-color: #e0e0e0;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Initial visualization with all data
    createVisualization(data);
    
    // Create the range slider
    createRangeSlider();
    
    // Create arc preset buttons
    createArcButtons();
});