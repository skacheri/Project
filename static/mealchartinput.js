//www.knowlarity.com/blog/creating-pie-chart-d3-js-step-step/ -->
    // https://www.youtube.com/watch?v=P8KNr0pDqio
    // https://www.dashingd3js.com/lessons/d3-and-html-forms


function show_input_chart(){
    // const width = 1000;
    // const height = 500;
    let colors = d3.scaleOrdinal()
        .domain(["Vegetables", "Fruits", "Carbohydrates", "Proteins"])
        .range(["green", "orange", "saddlebrown", "darkviolet"]);

    let svg = d3.select('#pie_chart').append('svg').attr('width', 1000).attr('height', 500);

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
    let plate=svg.append("circle")
                        .attr("cx", 330)
                        .attr("cy", 250)
                        .attr("r", 220)
                        .style("opacity", 1)
                        .attr("fill", "darkgoldenrod");

    // since data that i need to pass is an object, need to pass a function(d or data) which returns d.percent from details and sort null will sort in the order given
    let data = d3.pie()
                .sort(null)
                .value(function(d) {return d.percent})(details);

    let segments = d3.arc() //arc generator fucntion
        .innerRadius(0)
        .outerRadius(200)
        .padAngle(.04)
        .padRadius(50)
        .cornerRadius(5);

    // path elements for different sections
    let sections = svg.append("g").attr("transform", "translate(330, 250)")
        .selectAll("path").data(data); //join data

    //append path elements and attach onclick handlers to them
    sections.enter()
            .append("path")
            // .style('stroke', 'beige')
            // .style('stroke-width', 8)
            .attr("d", segments)
            .attr("fill", function(d) {
                return colors(d.data.foodgroup);
                })
            .attr("class", "pie_class")
            .on("click", function(d) {
                let current_foodgroup = d.data.next_foodgroup ? d.data.next_foodgroup : d.data.foodgroup;
                let next_foodgroup = "";
                for(let idx=0;idx<details.length;idx++){
                    if(details[idx].foodgroup == current_foodgroup){
                        next_id = (idx+1)%details.length;
                        next_foodgroup = details[next_id].foodgroup;
                        break;
                    }
                }
                d.data.next_foodgroup = next_foodgroup;
                d3.select(this)
                    .attr("fill", function(d) {
                        return colors(d.data.next_foodgroup);
                    });
                $("select[name='"+d.data.select_id+"']").val(d.data.next_foodgroup);
            });
    
    
    show_section_labels(data, segments);
    display_legend(svg, data, colors);
    
    let oil_data = [{name: "Unsaturated Fat", form_value:"Unsaturated_fat"},
                    {name: "Saturated Fat", form_value:"Saturated_fat"},
                    {name: "Trans Fat", form_value:"Trans_fat"}];
    
    let circle_oil = svg.append("circle")
                        .attr("cx", 100)
                        .attr("cy", 100)
                        .attr("r", 63)
                        .style("opacity", 1)
                        .attr("fill", "#FFFF00")
                        .style("stroke-width", 8)
                        .style("stroke", "darkgoldenrod");

    let oil_text = svg.append("text")
                    .attr("x", 40)
                    .attr("y", 100)
                    .data(oil_data)
                    .attr("class", "oil_text")
                    .text(function(d){
                        return d.name;
                        })
                    .on("click", function(d){
                        let current_name = d.next_name ? d.next_name : d.name;
                        let next_name = "";
                        let next_form_value = "";
                        for(let id=0;id<oil_data.length;id++){
                            if(oil_data[id].name == current_name){
                                next_id = (id+1)%(oil_data.length);
                                next_name = oil_data[next_id].name;
                                next_form_value = oil_data[next_id].form_value;
                                break;
                            }
                        }
                        d.next_name = next_name;
                        d3.select(this)
                            .text(function(d) {
                                return d.next_name;
                            });
                        $("select[name='meal_component_oil']").val(next_form_value);

                    });


    let drink_data = [{name: "Water", form_value:"Water"},
                        {name:"Juice", form_value:"Juice"}, 
                        {name:"Dairy", form_value:"Dairy"},
                        {name:"Soda", form_value:"Soda"},
                        {name:"Tea no sugar", form_value:"Tea_no_sugar"},
                        {name:"Coffee no sugar", form_value:"Coffee_no_sugar"},
                        {name:"Tea & sugar", form_value:"Tea_with_sugar"},
                        {name:"Coffee & sugar", form_value:"Coffee_with_sugar"}];

    let circle_drink = svg.append("circle")
                        .attr("cx", 560)
                        .attr("cy", 100)
                        .attr("r", 63)
                        .attr("fill", "lightblue")
                        .style("stroke-width", 8)
                        .style("stroke", "darkgoldenrod");


        let drink_text = svg.append("text")
                        .attr("x", 510)
                        .attr("y", 100)
                        .data(drink_data)
                        .attr("class", "drink_text")
                        .text(function(d){
                            return d.name;
                        })
                        .on("click", function(d){
                        let current_name = d.next_name ? d.next_name : d.name;
                        let next_name = "";
                        let next_form_value = "";
                        for(let id=0;id<drink_data.length;id++){
                            if(drink_data[id].name == current_name){
                                next_id = (id+1)%(drink_data.length);
                                next_name = drink_data[next_id].name;
                                next_form_value = drink_data[next_id].form_value;
                                break;
                            }
                        }
                        d.next_name = next_name;
                        d3.select(this)
                            .text(function(d) {
                                return d.next_name;
                            });
                        $("select[name='meal_component_drink']").val(next_form_value);
                        });
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
    let legends = svg.append("g").attr("transform", "translate(550, 300)").selectAll(".legends").data(data);
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