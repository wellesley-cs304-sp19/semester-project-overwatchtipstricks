
console.log("heyyy we're in likes.js");

var URL = "{{url_for('likePost')}}";


// SEND TO BACKEND!
$(".tip-list").on('click',".like",function (evt) { 
    console.log('SENDING TO BACKEND...');

        that = this; 
        likeStatus = $(that).find("[name=likeButton]").attr("value");
        console.log(likeStatus);
        tipID = $(that).closest("[data-tipID]").attr('data-tipID');
        console.log(tipID);
        $.post(URL, {likeSymbol:likeStatus, tipID:tipID},updateTipList);

});

// UPDATE FRONTEND!
function updateTipList(obj){
};