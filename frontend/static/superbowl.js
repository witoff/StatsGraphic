//------------------------------------------------------------------------------
function newFilledArray(len, val) {
    var rv = new Array(len);
    while (--len >= 0) {
        rv[len] = val;
    }
    return rv;
}

//------------------------------------------------------------------------------
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

var patsLikeCount      = 0;
var patsCommentCount   = 0;
var giantsLikeCount    = 0;
var giantsCommentCount = 0;

//------------------------------------------------------------------------------
function processFeed(data)
{
    console.trace('Received fb feed. Processing... ');
    
    //alert('data received!');
    //alert(JSON.stringify(response));
    if (!data || data.length == 0) {
        console.trace('Failed =(\n');
    
        // Show Error dialog to user or something.
        alert("Error retrieving your Facebook feed. What have your friends been saying?...");
        
        // For debugging.
        /*
        alert(patriotPosts.length);
        alert(giantPosts.length);
        alert(allPosts.length);
        */
        
        return;
    }
    else {
        // allPosts = allPosts.concat(data);
        patsLikeCount      += data['patriots']['like_count'];
        patsCommentCount   += data['patriots']['comment_count'];
        giantsLikeCount    += data['giants']['like_count'];
        giantsCommentCount += data['giants']['comment_count'];
        udpateTeamStatsView();
        console.trace('Success!\n');
        // FB.api(response.paging.next.slice(27), processFeedResponse);
    }

    /*
    FB.api('/me/home',
        {
            //'since':'last week',
            'limit': '500'
        },
        processFeedResponse
    );
    */
}

//------------------------------------------------------------------------------
function udpateTeamStatsView()
{
    // Set the number value of the stats bars.
    document.getElementById('patriots_comment_like_count').innerHTML = patsLikeCount;
    document.getElementById('patriots_comment_count').innerHTML = patsCommentCount;;
    document.getElementById('giants_comment_like_count').innerHTML = giantsLikeCount;;
    document.getElementById('giants_comment_count').innerHTML = giantsCommentCount;;

    // Figure out which one is the longest, so we can scale the stats bars.
    var longestCount = patsLikeCount;
    if (patsCommentCount > longestCount)
        longestCount = patsCommentCount;
    if (giantsLikeCount > longestCount)
        longestCount = giantsLikeCount;
    if (giantsCommentCount > longestCount)
        longestCount = giantsCommentCount;
    // alert("longestCount " + longestCount);
    
    // Calculate the percentage of each stats bar to fill.
    var patsLikeRatio = 0;
    var patsCommentRatio = 0;
    var giantsLikeRatio = 0;
    var giantsCommentRatio = 0;
    
    if (longestCount != 0) {
        // Multiply by 65% so a bar can never be more than 65% 'full'. I.e. 65% is the max width. You get the idea.
        // Also, set a min-width of 20% (which translates to 48px) by adding 0.2, so there is always room for the icon and text. So, the max is really 85%. Yeah I know I misled you with that previous comment =P. This comment's really long. Fuck new-lines.
        patsLikeRatio = patsLikeCount / longestCount * 0.65 + 0.2;
        patsCommentRatio = patsCommentCount / longestCount * 0.65 + 0.2;
        giantsLikeRatio = giantsLikeCount / longestCount * 0.65 + 0.2;
        giantsCommentRatio = giantsCommentCount / longestCount * 0.65 + 0.2;
    }
    
    // All the stats-bars are the same width (see div.stat_bar in main.css).
    // parseInt removes the 'px' from the end.
    var statsBarWidth = parseInt(document.getElementById('giants_comments_bar').style.width);
    // alert("statsBarWidth " + statsBarWidth);
    
    // Calculate the pixel widths of each stats bar to fill.
    var patsLikeWidth = Math.round(patsLikeRatio * statsBarWidth);
    var patsCommentWidth = Math.round(patsCommentRatio * statsBarWidth);
    var giantsLikeWidth = Math.round(giantsLikeRatio * statsBarWidth);
    var giantsCommentWidth = Math.round(giantsCommentRatio * statsBarWidth);
    
    // Set the inactive regions first, so the formatting won't temporarilly be 
    // curfuffled if the active region is longer than it was.
    // Subtract 2, because of the 2-pixel gap between the active region and the inactive region.
    document.getElementById('patriots_comment_likes_inactive_region').style.width = (statsBarWidth - patsLikeWidth - 2) + "px";
    document.getElementById('patriots_comments_inactive_region').style.width = (statsBarWidth - patsCommentWidth - 2) + "px";
    document.getElementById('giants_comment_likes_inactive_region').style.width = (statsBarWidth - giantsLikeWidth - 2) + "px";
    document.getElementById('giants_comments_inactive_region').style.width = (statsBarWidth - giantsCommentWidth - 2) + "px";
    
    document.getElementById('patriots_comment_likes_active_region').style.width = patsLikeWidth + "px";
    document.getElementById('patriots_comments_active_region').style.width = patsCommentWidth + "px";
    document.getElementById('giants_comment_likes_active_region').style.width = giantsLikeWidth + "px";
    document.getElementById('giants_comments_active_region').style.width = giantsCommentWidth + "px";
}

//------------------------------------------------------------------------------
function searchAndAddByMessage(feed, arr, s)
{
    $(feed).each(function(){
      if (this.message && this.message.indexOf(s) !=-1){
          arr.push(this);
      }
    });
}