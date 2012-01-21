
function newFilledArray(len, val) {
    var rv = new Array(len);
    while (--len >= 0) {
        rv[len] = val;
    }
    return rv;
}

function newIncreasingArray(len) {
    var rv = new Array(len);
    while (--len >= 0) {
        rv[len] = len;
    }
    return rv;
}

$(document).ready(function() {

    //
    //Preprocess
    //

    function timeChart(data, div, title)
    {
        var ageChart = new Highcharts.Chart({
        chart: {
            renderTo: div,
            type: 'area'
        },
        title: {
            text: title
        },
        xAxis: {
            title: {
                text: 'Time'
            },
            categories: newIncreasingArray(24)
        },
        yAxis: {
            title: {
                text: '# of Friends'
            }
        },
        series: [{
            name: 'All Friends',
            data: data
        }],
        tooltip: {
            formatter: function(){
                if (this.series.name=='Boy')
                    return 'boy names';
                return 'girl names';
            }}

        });
    }
    timeChart(fbdata.feed.time.posts, 'ageGender', "What time are your friends using facebook?");
    timeChart(fbdata.home.time.posts, 'ageOutliers', "What time are YOU using facebook?");




    /*var maxAge = 40;
    var skipFirstAges = 18;
    var ages = newFilledArray(maxAge, 0);
    var boyAges = newFilledArray(maxAge, 0);
    var girlAges = newFilledArray(maxAge, 0);

    var fe = friendEvents;
    //Add in birth year and agewhere available
    for (var i in fe){
        if (fe[i].user.birthday){
            var segments = fe[i].user.birthday.split('/');
            if (segments.length == 3){
                fe[i].user.birthyear = parseInt(segments[2]);
                fe[i].user.age = 2012 - fe[i].user.birthyear;
            }
        }
    }

    //
    //Extract Stats
    //

    //Age arrays
    var friendsWithAge = 0;
    for (var i in fe){
        var age = fe[i].user.age;
        if (age)
        {
            friendsWithAge++;
            if (age<=maxAge){
               ages[age]++;
                var gender = fe[i].user.gender;
                if (gender){
                    if (gender=='male')
                        boyAges[age]++
                    else if (gender=='female')
                        girlAges[age]++
                }
            }
        }
    }

    var boys = 0;
    var boysWithAge = 0;
    var girls = 0;
    var girlsWithAge = 0;
    //Gender Age publicity
    for (var i in fe){
        var age = fe[i].user.age;
        var gender = fe[i].user.gender;
        if (gender=='male'){
            boys++;
            if (age)
                boysWithAge++;
        }
        if (gender=='female'){
            girls++;
            if (age)
                girlsWithAge++;
        }
    }


    var friendCount = fe.length;


    //
    //Plot
    //

    fillAgePublicity(friendCount, friendsWithAge);
    fillGenderAgePublicity(boys, boysWithAge, 'Boys');
    fillGenderAgePublicity(girls, girlsWithAge, 'Girls');
    fillAgeChart(ages, maxAge, skipFirstAges);
    fillAgeGender(boyAges, girlAges, maxAge, skipFirstAges);

*/
});


function fillAgePublicity(total, ages)
{
    var publicityChart = new Highcharts.Chart({
        chart: {
            renderTo: 'agePublicity',
            type: 'pie'
        },
        title: {
            text: 'Age on Facebook'
        },
        series: [{
            name: 'Boy',
            data: [{y: total-ages, name: 'No Age'},{ y: ages, name: 'Ages'}]
        }]

    });
}
function fillGenderAgePublicity(total, minority, gender)
{
    var publicityChart = new Highcharts.Chart({
        chart: {
            renderTo: 'agePublicity' + gender,
            type: 'pie'
        },
        title: {
            text: gender + '\'s with Ages'
        },
        series: [{
            name: gender,
            data: [{y: total-minority, name: 'No Age'},{ y: minority, name: 'Ages'}]
        }]
    });
}

function fillAgeChart(ages, maxAge, skipFirstAges){


    var age = newIncreasingArray(maxAge).slice(skipFirstAges);
    var ages = ages.slice(skipFirstAges);


    var ageChart = new Highcharts.Chart({
        chart: {
            renderTo: 'age',
            type: 'area'
        },
        title: {
            text: 'How old are your friends?'
        },
        xAxis: {
            title: {
                text: 'Age'
            },
            categories: age
        },
        yAxis: {
            title: {
                text: '# of Friends'
            }
        },
        series: [{
            name: 'All Friends',
            data: ages
        }],
        tooltip: {
            formatter: function(){
                if (this.series.name=='Boy')
                    return 'boy names';
                return 'girl names';
            }}

    });

}

function fillAgeGender(boyAges, girlAges, maxAge, skipFirstAges){


    var age = newIncreasingArray(maxAge).slice(skipFirstAges);
    boyAges = boyAges.slice(skipFirstAges);
    girlAges = girlAges.slice(skipFirstAges);


    var ageChart = new Highcharts.Chart({
        chart: {
            renderTo: 'ageGender',
            type: 'area'
        },
        title: {
            text: 'How old are your friends?'
        },
        xAxis: {
            title: {
                text: 'Age'
            },
            categories: age
        },
        yAxis: {
            title: {
                text: '# of Friends'
            }
        },
        series: [{
            name: 'Boy',
            data: boyAges
        }, {
            name: 'Girl',
            data: girlAges
        }],
        tooltip: {
            formatter: function(){
                if (this.series.name=='Boy')
                    return 'boy names';
                return 'girl names';
            }}

    });

}