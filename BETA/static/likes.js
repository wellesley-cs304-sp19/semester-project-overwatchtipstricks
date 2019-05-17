

//when the document is ready
 $( document ).ready(function() {
     var URL="/likePost";

    //when the like button is clicked on the tip-list
     $(".tip-list").on('click',".like",function (evt){
         console.log("LIKE BUTTON CLICKED. SENDING TO BACKEND....");
         that=this;
         
         //get the text on the like button so we can update it after it was clicked
         //and get the tipID for the tip we are updating
         evt.preventDefault();
         likeButtonText = $(that).find("[name=likeButton]").attr("value");
         tipID = $(that).closest("[data-ID]").attr("data-ID");
         
         //send the likeButtonText and tipID to the backend, and then
         //call the updatePostList function to update the frontend
         $.post(URL,{likeButtonText: likeButtonText, tipID:tipID}, updatePostList);
         
         console.log("likeButtonText and tipID of tip");
         console.log(likeButtonText);
         console.log(tipID);
         
     });
     
 });

function updatePostList(obj){
    console.log("UPDATEPOSTLIST IN LIKES.JS");
    console.log(obj);

    //find where we store the totalLikes for a post, and update it to the new
    //number of likes
     $(".tip-list").find("[data-ID=" + obj.tipID+"]")
                    .find("#totalLikes")
                    .html(obj.newLikes);
                    
    //find where the likeButton is, and update the value of the button to
    //update the button text
    $(".tip-list").find("[data-ID=" + obj.tipID+"]")
                    .find("[name=likeButton]")
                    .val(obj.likeButtonText);
};
