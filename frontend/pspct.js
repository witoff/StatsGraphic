
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
    var maxAge = 35;
    var skipFirstAges = 18;
    var ages = newFilledArray(maxAge, 0);

    var friendsWithAge = 0;
    for (var i in friendEvents)
    {
        var bday = friendEvents[i].user.birthday;
        if (bday)
        {
            var segments = bday.split('/');
            if (segments.length == 3)
            {
                friendsWithAge++;
                var age = 2012 - parseInt(segments[2]);
                if (age+1>maxAge)
                    continue;
                ages[age]++;
            }
        }
    }
    var friendCount = friendEvents.length;


    //
    //Plot
    //
    fillAgeChart(ages, maxAge, skipFirstAges);
    fillAgePublicity(friendCount, friendsWithAge);

});

function fillAgePublicity(total, ages)
{
    alert(total);
    alert(ages);
    var publicityChart = new Highcharts.Chart({
        chart: {
            renderTo: 'agePublicity',
            type: 'pie'
        },
        title: {
            text: 'How many friends have their age on Facebook?'
        },
        series: [{
            name: 'Boy',
            data: [{y: total-ages, name: 'No Age'},{ y: ages, name: 'Ages'}]
        }],
        tooltip: {
            formatter: function(){
                if (this.series.name=='Boy')
                    return 'boy names';
                return 'girl names';
            }}

    });
}

function fillAgeChart(ages, maxAge, skipFirstAges){


    var age = newIncreasingArray(maxAge).slice(skipFirstAges);
    var boyAgeCount = ages.slice(skipFirstAges);
    var girlAgeCount = ages.slice(skipFirstAges);


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
            name: 'Boy',
            data: boyAgeCount
        }, {
            name: 'Girl',
            data: girlAgeCount
        }],
        tooltip: {
            formatter: function(){
                if (this.series.name=='Boy')
                    return 'boy names';
                return 'girl names';
            }}

    });

}