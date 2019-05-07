
var select = document.getElementById("heroes"); 
var h = ['All','Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree',
    'Mei','Pharah','Reaper','Soldier:76','Sombra','Symmetra','Torbjorn',
    'Tracer','Widowmaker','D.Va','Orisa','Reinhardt','Roadhog','Winston',
    'Wrecking Ball','Zarya','Ana','Baptiste','Bridgette','Lúcio','Mercy',
    'Moira','Zenyatta','General']; 

var maps = ['All','Hanamura','Horizon Lunar Colony','Paris','Temple of Anubis',
    'Volskaya Industries','Dorado','Junkertown','Rialto','Route 66',
    'Watchpoint: Gibralter','Blizzard World','Eichenwalde','Hollywood',
    'Kings Row','Numbani','Busan','Ilios','Lijang Tower','Nepal,Oasis','General'];
    
var difficulty = ['All', 'Beginner', 'Intermediate', 'Advanced', 'Expert'];


 $( document ).ready(function() {
 $.each(h, function(val, text) {
            $('#heroes').append( $('<option></option>').val(text).html(text) )
            }); 
            
  $.each(maps, function(val, text) {
           $('#maps').append( $('<option></option>').val(text).html(text) )
           });       
  
    $.each(difficulty, function(val, text) {
           $('#difficulty').append( $('<option></option>').val(text).html(text) )
           });    
           
 });