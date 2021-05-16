function toHome(){
    window.location.replace("/");
}

//INDEX.HTML
$('.carousel').carousel({
    interval: 10000
});





//REGISTER.HTML
function validateUsername(){
    if($('.required').innerHTML == None){
        return false;
    }else{
        return true;
    }
}
