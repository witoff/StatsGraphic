
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


function plotData(fbdata) {
    timeChart(fbdata.feed.time.posts, 'yourTime', "What time are YOU using facebook?");
    timeChart(fbdata.home.time.posts, 'friendsTime', "What time are your friends using facebook?");

    showTopPhotos(fbdata);
    presHistogram(fbdata, 'pres');

    var buffer = [];
    buffer.push('<b>CHECKINS</b>');
    buffer.push('Over time you have checked into ' + fbdata.checkins.total_count + ' places');
    buffer.push('This week you checked into ' + fbdata.checkins.week_count + ' places');
    $('#text').append(buffer.join('<br/>'));
    $('#text').append('<br/><br/>');

    buffer = [];
    buffer.push('<b>CUMULATIVE</b>');
    buffer.push('Your average status length: ' + fbdata.feed.average_status_length);
    buffer.push('Your friends averagae status length: ' + fbdata.home.average_status_length);
    $('#text').append(buffer.join('<br/>'));
    $('#text').append('<br/><br/>');

    buffer = [];
    buffer.push('<b>YOUR WALL:</b>');

    buffer.push('<br/>Active Friends:');
    var active = fbdata.feed.friend.active;
    for (var i=0; i<active.length;i++){
        var rank = 1+i;
        buffer.push('-rank: ' + rank);
        buffer.push('---name: ' + active[i]['name']);
        buffer.push('---checkins: ' + active[i]['checkin_count']);
        buffer.push('---links: ' + active[i]['link_count']);
        buffer.push('---photos: ' + active[i]['photo_count']);
        buffer.push('---status: ' + active[i]['status_count']);
        buffer.push('---<i>total: ' + active[i]['total_count'] + "</i>");
    }

    buffer.push('<br/>Liked Friends:');
    var active = fbdata.feed.friend.liked;
    for (var i=0; i<active.length;i++){
        var rank = 1+i;
        buffer.push('-rank: ' + rank);
        buffer.push('---name: ' + active[i]['name']);
        buffer.push('---count: ' + active[i]['like_count']);
    }
    buffer.push('<br/>Like Ratio:');
    var active = fbdata.feed.friend.ratio;
    for (var i=0; i<active.length;i++){
        var rank = 1+i;
        buffer.push('-rank: ' + rank);
        buffer.push('---name: ' + active[i]['name']);
        buffer.push('---posts: ' + active[i]['post_count']);
        buffer.push('---likes: ' + active[i]['like_count']);
        buffer.push('---ratio: ' + active[i]['like_ratio']);
    }

    $('#text').append(buffer.join('<br/>'));
    $('#text').append('<br/>');

    
});

function showTopPhotos(data){
    var photos = data.home.type.photo.top;
    var buffer = [];

    $(photos).each(function(){
        buffer.push('<div style="border: solid 1px;">');
        buffer.push('from: ' + this.from);
        buffer.push('<br/>likes: ' + this.like_count);
        buffer.push('<br/>message: ' + this.msg);
        buffer.push('<img src="' + this.picture + '" alt="">');
        buffer.push('</div>');
    })


    $('#topPhotos').html(buffer.join(''));
}

function presHistogram(data, div){

    var names = [];
    var count = [];
    for (k in data.home.presidents){
        names.push(k);
        count.push(data.home.presidents[k].length);
    }

    var ageChart = new Highcharts.Chart({
        chart: {
            renderTo: div,
            type: 'bar'
        },
        title: {
            text: 'President mentions'
        },
        xAxis: {
            title: {
                text: 'Time'
            },
            categories: names
        },
        yAxis: {
            title: {
                text: '# of Friends'
            }
        },
        series: [{
            name: 'All Friends',
            data: count
        }],
        tooltip: {
            formatter: function(){
                if (this.series.name=='Boy')
                    return 'boy names';
                return 'girl names';
            }}

    });
}

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