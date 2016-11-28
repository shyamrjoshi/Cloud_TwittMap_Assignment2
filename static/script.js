
      var map;
      function initMap(data) {
        console.log(data);
        //var myStringArray = ["Hello","World"];
        var arrayLength = data.length;
        var marker_feature = [];

        for (var i = 0; i < arrayLength; i++) {
            //console.log(data[i]["coordinates"][0]);
            var coordinates = data[i]["coordinates"];
            coordinates = coordinates.replace("[","");
            coordinates = coordinates.replace("]","");
            var coordinates_array = coordinates.split(",");
            console.log(coordinates_array[1],coordinates_array[0])
            var marker_entry = {
              position: new google.maps.LatLng(coordinates_array[1], coordinates_array[0]),
              type: data[i]["sentiment"]
            };

            //marker_entry["position"] = data[i]["coordinates"]
            marker_feature.push(marker_entry);
            //Do something
        }

       //var temp = marker_entry.position[0];
      //  var temp = marker_entry.position.split(",");
      //  var temp1 = temp[1] + "," + temp[0];

      //  marker_entry.position = temp1;
        //marker_entry.position[1] = temp;
       // console.log(marker_entry);
       console.log(marker_feature);
        map = new google.maps.Map(document.getElementById('map'), {
         center: new google.maps.LatLng(0,0),
		zoom: 2,
		mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
        var icons = {
          positive: {
            icon: iconBase + 'parking_lot_maps.png'
          },
          negative: {
              icon: iconBase + 'library_maps.png'
          },
          neutral: {
            icon: iconBase + 'info-i_maps.png'
          }
        };

        function addMarker(feature) {
          var marker = new google.maps.Marker({
            position: feature.position,
            icon: icons[feature.type].icon,
            map: map
          });
        }

        var features = [
          {
            position: new google.maps.LatLng(36.778259, -119.417931),
            type: 'positive'
          }, {
            position: new google.maps.LatLng(-33.91539, 151.22820),
            type: 'negative'
          }
        ];

        //for (var i = 0, feature; feature = features[i]; i++) {
          //addMarker(feature);
        //}
        //for (var i = 0, marker_feature; marker_feature = marker_feature[i]; i++) {
         // addMarker(marker_feature);
        //}
        for(var i = 0;i<marker_feature.length;i++){
          addMarker(marker_feature[i])
        }
      }
