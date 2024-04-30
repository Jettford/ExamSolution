var slides = document.querySelectorAll("img");
for (var i = 0; i < slides.length; i++) {        
    var img=new Image();
    img.src=slides[i].src;

    // and we wonder why modern internet is so aggressively bloated and over-worked... this is the literal only smooth way to do this
}

var slideIndex = 0;
showSlides();

function showSlides() {
    var slides = document.querySelectorAll("img");
    
    slides[slideIndex].style.display = "block";
    for (var i = 0; i < slides.length; i++) {
        if (i != slideIndex) slides[i].style.display = "none";
    }

    slideIndex++;
    if (slideIndex >= slides.length) {
        slideIndex = 0;
    }
    
    setTimeout(showSlides, 5000);
}   