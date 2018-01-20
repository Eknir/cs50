// TODO! Drop down menu for add
// TODO! create stars for ranking
// TODO! Querry the organization (name, website, city, country)
// TODO! Upcoming events in sidebar
// TODO! Layout

var map;
var markers = [];


// initialize map
function initMap() {
  var home = {lat: 52.098314, lng: 5.014109};

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 2,
    center: home
  });
}


// TODO! Making this a function
// add a marker for all organizations in in database
$.getJSON(Flask.url_for("organization"))
    .done(function ( data ){
        for (var i = 0; i < data.length; i ++)
        {
           // pass all data related to the organization for which we want to make a marker
            addMarker(data[i]);
        }
    })
     .fail(function( error ) {
   console.log("ERROR READING EVENTS");
    });

// function to add the marker
function addMarker(organization) {
    address = organization.country + " " + organization.city;
    name = organization.name;

    // Get JSON from Google GEOCODING API
    $.getJSON("https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=AIzaSyB6oqrJGfdzeoS8wUD1VImCheHWT7CSbBY", (function() {
    // make name a local variable
        var name_1 = name;
        return function(data) {
            // initialize marker
            var marker = new google.maps.Marker({
                // position is the latlng from the geocoding api
                position: data.results[0].geometry.location,
                map: map,
                title: name_1
                });
            markers.push(marker);
            // Execute GetInfo function when marker is clicked
            marker.addListener('click', function() {
                getInfo(organization);
            });
        };
    })());
}

// This function is executed if a marker is clicked and pastes relevant info of the organization in the sidebar.
function getInfo(organization){
var organization_id=organization['organization_id'];
    // access the relevant /organization page for the marker that is being clicked
  $.getJSON(Flask.url_for("organization"), 'organization_id=' + organization_id, (function() {
            return function(data) {

            if(data[0]['website'] == "")
            {
                var website = "<p><b>Website:</b> No website available";
            }
            else
            {
                var website = "<p><b>Website:</b> <a href=" +  data[0]['website'] + ">"+ data[0]['website'] + "</a></p>";
            }

            // change sidebar information to visible
            document.getElementById('ranking_form').style.visibility = "visible";
            // past all relevant information into string content
            name = "<b>Name:</b> " + organization['name'];
            city = "</p><p><b>City:</b> " + organization['city'];
            country = "</p><p><b>Country:</b> " + organization['country'];
            website = "</p>" + website;

            document.getElementById('organization_id').innerHTML = organization['organization_id'];
            // past content into sidebar under the div id event_info
            document.getElementById('organization_name').innerHTML = name;
            document.getElementById('country').innerHTML = country;
            document.getElementById('website').innerHTML = website;
            // put the organization_id into the DOM (hidden)


            };
    })());

    $.getJSON(Flask.url_for("review"), 'organization_id=' + organization_id, (function() {
        return function(data) {

            var reviews = "";
            document.getElementById('reviews').innerHTML = reviews;

            if(data.length == 0)
            {
                var ranking = "<p>Average rating No rating available</p>";
            }
            else
            {
                var cum_ranking = 0;
                var reviews_text = "";
                for (var i = 0; i < data.length; i ++)
                    {
                        cum_ranking += data[i].rate;
                        if (!data[i].review == "")
                        {
                            reviews_text = reviews_text + "<p><i>\"" + data[i].review + "\"</i></p>";
                        }
                    }
                    if (!reviews_text == "")
                    {
                        reviews = "<p><b>Reviews:</b></p>" + reviews_text;
                        document.getElementById('reviews').innerHTML = reviews;
                    }
                if(data.length == 1)
                {
                    review = " review";
                }
                else
                {
                    review = " reviews";
                }
                ranking = "<p><b>Average rating:</b> " + String(cum_ranking / data.length).slice(0,3) +  " based on " + String(data.length) + review + "</p>";
            }

            document.getElementById('average_rating').innerHTML = ranking;

        };
    })());


}

//TODO! source referencing
// This function is called when the user submits a form and is used to substract DATA from the HTML and add it (unseen) to the form that is being submitted
function submitHandler()
 {
    // get the data from the div with id event_name and slice is (such that only the event name is taken
     submitVal = $('#organization_id').text()
    // append the submitted form with submitVal
     $('#myForm').append("<input type='hidden' name='submitValue' value='"+ submitVal+"' />");
 }


function validateSubmit() {
    var rating = document.forms["myForm"]["rating"].value
    if (rating == "") {

        document.getElementById("errorRate").innerHTML = "No rate given";
        return false;
    }
    submitHandler()
    document.getElementById('myForm').submit();
}


// function to valide addform submission via javascript
function validateAddForm() {
    var name = document.forms["addForm"]["name"].value;
    var city = document.forms["addForm"]["city"].value;
    var country = document.forms["addForm"]["country"].value;


    if (name == "" || city =="" || country =="") {
      if (name =="") {
        document.getElementById("errorName").innerHTML = "Fill in the name";
      }
      else {
         document.getElementById("errorName").innerHTML = "";
      }
      if (city =="") {
        document.getElementById("errorCity").innerHTML = "Fill in the city";
      }
      else {
         document.getElementById("errorCity").innerHTML = "";
      }
      if (country == "") {
        document.getElementById("errorCountry").innerHTML = "Fill in the country";
      }
      else {
        document.getElementById("errorCountry").innerHTML = "";
      }
      return false;
    }
};
