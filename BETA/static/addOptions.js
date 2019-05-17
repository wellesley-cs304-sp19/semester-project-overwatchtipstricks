/*on document load, populate the hero, maps, and difficulty dropdowns. 
The text of each option item  as well as the "value" is the hero, map,
or difficulty name. */


//staic list of all heroes, maps, and difficulty in our DB
var heroes = ['All','Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree',
    'Mei','Pharah','Reaper','Soldier:76','Sombra','Symmetra','Torbjorn',
    'Tracer','Widowmaker','D.Va','Orisa','Reinhardt','Roadhog','Winston',
    'Wrecking Ball','Zarya','Ana','Baptiste','Bridgette','Lúcio','Mercy',
    'Moira','Zenyatta']; 

var maps = ['All','Hanamura','Horizon Lunar Colony','Paris','Temple of Anubis',
    'Volskaya Industries','Dorado','Junkertown','Rialto','Route 66',
    'Watchpoint: Gibralter','Blizzard World','Eichenwalde','Hollywood',
    'Kings Row','Numbani','Busan','Ilios','Lijang Tower','Nepal,Oasis'];
    
var difficulty = ['All', 'Beginner', 'Intermediate', 'Advanced', 'Expert'];


//on document ready, populate the menu bars
/*when posting tips, there are two different menu bars to populate, 
so fill in both ids (e.g. heroes and tipHero)*/

 $( document ).ready(function() {
 $.each(heroes, function(val, text) {
            $('#heroes').append( $('<option></option>').val(text).html(text) );
            $('#tipHero').append( $('<option></option>').val(text).html(text) );
            }); 
            
            
  $.each(maps, function(val, text) {
           $('#maps').append( $('<option></option>').val(text).html(text) );
           $('#tipMap').append( $('<option></option>').val(text).html(text) );
           });       
  
    $.each(difficulty, function(val, text) {
           $('#difficulty').append( $('<option></option>').val(text).html(text) )
           });    
 });
 