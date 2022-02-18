function collectData(accessToken)
{
    var page = 1
    var data = new Array()
    var stillData = true
    while (stillData) {
        // get page of activities from Strava
        urlActivities = 'https://www.strava.com/api/v3/activities' + '?access_token=' + accessToken + '&per_page=200' + '&page=' + page.toString()
        r = httpGet(urlActivities)
        // if no results then exit loop
        if (r.slice(1, -1).length == 0){
            stillData = false
        }
        else{
            data.push(r)
            page += 1
        }
            
    }

    colsToRetrieve =[
        'resource_state',
        'name',
        'distance',
        'moving_time',
        'elapsed_time',
        'total_elevation_gain',
        'type',
        'id',
        'start_date',
        'start_date_local',
        'timezone',
        'utc_offset',
        'location_city',
        'location_state',
        'location_country',
        'achievement_count',
        'kudos_count',
        'comment_count',
        'athlete_count',
        'photo_count',
        'trainer',
        'commute',
        'manual',
        'private',
        'visibility',
        'flagged',
        'gear_id',
        'start_latlng',
        'end_latlng',
        'start_latitude',
        'start_longitude',
        'average_speed',
        'max_speed',
        'average_cadence',
        'has_heartrate',
        'average_heartrate',
        'max_heartrate',
        'heartrate_opt_out',
        'display_hide_heartrate_option',
        'elev_high',
        'elev_low',
        'upload_id',
        'upload_id_str',
        'external_id',
        'from_accepted_tag',
        'pr_count',
        'total_photo_count',
        'has_kudoed',
        'suffer_score',
        'workout_type',
        'average_watts',
        'max_watts',
        'weighted_average_watts',
        'kilojoules',
        'device_watts',
        'average_temp',
        'map'
    ]

    specialCols={
        'map':[
            'id',
            'summary_polyline',
            'resource_state',

        ]
    }
    
    return JSON.parse(data)

}
  

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false ); 
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
  
  

// function makeTable(data){
//     const body = document.body,
//     tbl = document.createElement('table');
//     tbl.style.display = 'block';
//     tbl.style.width = '100%';
//     tbl.style.height = '500px';
//     tbl.style.border = '1px solid black';
//     tbl.style.overflowY = 'auto';
//     tbl.style.overflowX = 'auto';

//     for (let i = -1; i < data.length; i++) {
//         if (i < 0){
//             const tr = tbl.insertRow();
//             for (let j = 0; j < colsToRetrieve.length; j++){
//                 col = colsToRetrieve[j]
//                 if (specialCols[col]){
//                     arrayOfSpecialCols = specialCols[col]
//                     for(el=0;el<arrayOfSpecialCols.length;el++){
//                         const td = tr.insertCell();
//                         specialCol=arrayOfSpecialCols[el]
//                         info = col+'.'+specialCol
//                         td.innerHTML = info
//                         td.style.border = '1px solid black';
//                         td.style.overflowY = 'scroll';
//                         td.style.overflowX = 'scroll';
//                         td.style.width = '5px';
//                     }
//                 }else{
//                     const td = tr.insertCell();
//                     info = col
//                     td.innerHTML = info
//                     td.style.border = '1px solid black';
//                     td.style.overflowY = 'scroll';
//                     td.style.overflowX = 'scroll';
//                     td.style.width = '5px';
//                 }
//             }
//         }
//         else{
//             activity = data[i]
//             const tr = tbl.insertRow();
//             for (let j = 0; j < colsToRetrieve.length; j++) {
//                 col = colsToRetrieve[j]
//                 if (specialCols[col]){
//                     arrayOfSpecialCols = specialCols[col]
//                     for(el=0;el<arrayOfSpecialCols.length;el++){
//                         const td = tr.insertCell();
//                         specialCol=arrayOfSpecialCols[el]
//                         info = activity[col][specialCol]
//                         if (typeof(info)  === 'undefined'){
//                             activity[col][specialCol] = null
//                             info = null
//                         }
//                         td.innerHTML = info
//                         td.style.border = '1px solid black';
//                         td.style.overflowY = 'scroll';
//                         td.style.overflowX = 'scroll';
//                         td.style.width = '5px';
//                     }
//                 }else{
//                     const td = tr.insertCell();
//                     info = activity[col]
//                     if (typeof(info)  === 'undefined'){
//                         activity[col] = null
//                         info = null
//                     }
//                     td.innerHTML = info
//                     td.style.border = '1px solid black';
//                     td.style.overflowY = 'scroll';
//                     td.style.overflowX = 'scroll';
//                     td.style.width = '5px';
//                 }
//             }
//         }
//     }
//     body.appendChild(tbl);
// }

function cleanData(data){
    for (let i = 0; i < data.length; i++) {
        activity = data[i]
        for (let j = 0; j < colsToRetrieve.length; j++) {
            col = colsToRetrieve[j]
            if (specialCols[col]){
                arrayOfSpecialCols = specialCols[col]
                for(el=0;el<arrayOfSpecialCols.length;el++){
                    specialCol=arrayOfSpecialCols[el]
                    info = activity[col][specialCol]
                    if (typeof(info)  === 'undefined'){
                        activity[col][specialCol] = null
                        info = null
                    }
                }
            }else{
                info = activity[col]
                if (typeof(info)  === 'undefined'){
                    activity[col] = null
                    info = null
                }
            }
        }
    }

    return data
}

// data = collectData(accessToken);
// data = cleanData(data)
// $.ajax({
//     type: "POST",
//     url: user_url,
//     data: {
//         'activities': JSON.stringify(data),
//         csrfmiddlewaretoken: csrftoken
//     },
//     success: function () {
//         console.log('sent activities!')   
//         window.location.href = user_url;
//     }
// });


