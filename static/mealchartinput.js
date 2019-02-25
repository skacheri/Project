//www.knowlarity.com/blog/creating-pie-chart-d3-js-step-step/ -->
    // https://www.youtube.com/watch?v=P8KNr0pDqio
    // https://www.dashingd3js.com/lessons/d3-and-html-forms

function show_input_chart(){
    const width = 750;
    const height = 500;
    let colors = d3.scaleOrdinal()
        .domain(["Vegetables", "Fruits", "Carbohydrates", "Proteins"])
        .range(["green", "orange", "saddlebrown", "darkviolet"]);

    let svg = d3.select('#pie_chart').append('svg').attr('width', width).attr('height', height);

    let details = [{
        foodgroup: "Vegetables",
        percent: 40,
        select_id: "meal_component_40"
    }, {
        foodgroup: "Fruits",
        percent: 10,
        select_id: "meal_component_10"
    }, {
        foodgroup: "Carbohydrates",
        percent: 25,
        select_id: "meal_component_25"
    }, {
        foodgroup: "Proteins",
        percent: 25,
        select_id: "meal_component_2_25"
    }]

    // since data that i need to pass is an object, need to pass a function(d or data) which returns d.percent from details and sort null will sort in the order given
    let data = d3.pie().sort(null).value(function(d) {
        return d.percent;
    })(details);


    console.log(data);

    let segments = d3.arc() //arc generator fucntion
        .innerRadius(0)
        .outerRadius(200)
        .padAngle(.01)
        .padRadius(50);

    // path elements for different sections
    let sections = svg.append("g").attr("transform", "translate(250, 250)")
        .selectAll("path").data(data); //join data

    //append path elements and attach onclick handlers to them
    sections.enter()
            .append("path")
            .attr("d", segments)
            .attr("fill", function(d) {
                return colors(d.data.foodgroup);
                })
            // .on("click", function(d, i) {
            //     let current_foodgroup = d.data.next_foodgroup ? d.data.next_foodgroup : d.data.foodgroup;
            //     let next_foodgroup = "";
            //     for(let idx=0;idx<details.length;idx++){
            //         if(details[idx].foodgroup == current_foodgroup){
            //             next_id = (idx+1)%details.length;
            //             next_foodgroup = details[next_id].foodgroup;
            //             break;
            //         }
            //     }
            //     d.data.next_foodgroup = next_foodgroup;
            //     d3.select(this)
            //         .attr("fill", function(d) {
            //             return colors(d.data.next_foodgroup);
            //         });
            //     $("select[name='"+d.data.select_id+"']").val(d.data.next_foodgroup);
            // });
    show_section_labels(data, segments);
    display_legend(svg, data, colors);
}

function show_section_labels(data, segments){
    let content = d3.select("g").selectAll("text").data(data);
    content.enter().append("text").each(function(d) {
        let center = segments.centroid(d);
        d3.select(this).attr("x", center[0]).attr("y", center[1])
            .text(d.data.percent);
    });
}

function display_legend(svg, data, colors){
    let legends = svg.append("g").attr("transform", "translate(500, 200)").selectAll(".legends").data(data);
    let legend = legends.enter().append("g").attr("transform", function(d, i) {
        return "translate(0," + (i + 1) * 30 + ")";
    });
    legend.append("rect").attr("width", 20).attr("height", 20).attr("fill", function(d) {
        return colors(d.data.foodgroup);
    });
    legend.append("text").text(function(d) {
            return d.data.foodgroup;
        })
        .attr("fill", function(d) {
            return colors(d.data.foodgroup);
        })
        .attr("x", 30)
        .attr("y", 15);
}
$(show_input_chart);