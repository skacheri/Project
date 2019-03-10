function getEventData(){
    $.ajax({
        url: "/calendar/get_data",
    }).done(function( events ) {
        for(event_id in events){
            event = events[event_id];
            event.start_utc = moment.utc(event.start_utc);
            event.start=moment(event.start_utc).local().format("YYYY-MM-DD HH:mm:ss");
        }
        setCalendarContent(events);
    });
}

function setCalendarContent(events) {
    //from fullcalendar, to initialize calendar
    $('#calendar').fullCalendar({
        //passing in events
        events: events,
        eventRender: function(eventObj, element) {
            content = function() {
                // Create data for graph sections of plate removing drink and oil
                piechart_data = []
                for(fg_id in eventObj.meal_foodgroups){ 
                    d = eventObj.meal_foodgroups[fg_id];
                    if (d.percentage_meal == 40 || d.percentage_meal == 25 || d.percentage_meal == 10) {
                        piechart_data.push(d);
                    }
                }

                //Create our wrapper div (optional).
                let element = $('<div id="#my-popover-div"></div>');
                element.append(getpie_svg(piechart_data).node());
                let element1 = $('<div id="#my-popover-drink-div"></div>');
                let element2 = $('<div id="#my-popover-fat-div"></div>');

                for(fg_id in eventObj.meal_foodgroups){
                    if(eventObj.meal_foodgroups[fg_id].percentage_meal == 1){
                        element1.append("<small> Drink type: " + eventObj.meal_foodgroups[fg_id].foodgroup_name + "</small>")
                    }
                    if(eventObj.meal_foodgroups[fg_id].percentage_meal == 2){
                        element2.append("<small> Fat type: " + eventObj.meal_foodgroups[fg_id].foodgroup_name + "</small>")
                    }
                }
                
                element.append(element1);
                element.append(element2);
                //Return the jQuery collection.
                return element;
            };

            // Set the data elements that popover library will use to show the popover
            element.data('title', 'Meal foodgroup info');
            element.data('content', content);
            element.data('html', true);
            element.data('toggle', 'popover');
            element.data('trigger', 'click');
            element.data('placement', 'top');

            // Enable the popover for this event element
            element.popover();
        },
    })
}

$(getEventData);