

 $( document ).ready(function() {
     var URL="/likePost";

    
     $(".tip-list").on('click',".like",function (evt){
         console.log("LIKE BUTTON CLICKED. SENDING TO BACKEND....");
         that=this;
         evt.preventDefault();
         likeButtonText = $(that).find("[name=likeButton]").attr("value");
         tipID = $(that).closest("[data-ID]").attr("data-ID");
         
         $.post(URL,{likeButtonText: likeButtonText, tipID:tipID}, updatePostList);
         
         console.log("likeButtonText and tipID of tip");
         console.log(likeButtonText);
         console.log(tipID);
         
     });
     
 });

function updatePostList(obj){
    console.log("UPDATEPOSTLIST IN LIKES.JS");
    console.log(obj);

     $(".tip-list").find("[data-ID=" + obj.tipID+"]")
                    .find("#totalLikes")
                    .html(obj.newLikes);
                    
    $(".tip-list").find("[data-ID=" + obj.tipID+"]")
                    .find("[name=likeButton]")
                    .val(obj.likeButtonText);
};
