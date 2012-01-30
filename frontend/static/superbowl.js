
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

var patriotPosts = [];
var giantPosts = [];
var allPosts = [];

function processFeed(data){
    console.trace('processing home');
    alert('data rx');


    /*FB.api('/me/home',
        {
            //'since':'last week',
            'limit': '500'
        },
        processFeedResponse
    );*/

}

function processFeedResponse(response)
{
    //alert('data received!');
    //alert(JSON.stringify(response));
    if (!response.data || response.data.length == 0){
        alert(patriotPosts.length);
        alert(giantPosts.length);
        alert(allPosts.length);
        alert('done');
        return;
    }
    else
    {
        allPosts = allPosts.concat(response.data);
        searchAndAddByMessage(response.data, patriotPosts, 'atriots');
        searchAndAddByMessage(response.data, giantPosts, 'giant');
        //alert(response.paging.next.slice(27));
        FB.api(response.paging.next.slice(27), processFeedResponse);
    }
}



function searchAndAddByMessage(feed, arr, s)
{
    $(feed).each(function(){
      if (this.message && this.message.indexOf(s) !=-1){
          arr.push(this);
      }
    });
}