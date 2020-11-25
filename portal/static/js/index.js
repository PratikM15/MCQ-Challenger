function countdown(minutes) {
    var form = document.getElementById("test");
    var seconds = 60;
    var mins = minutes

    function tick() {
        //This script expects an element with an ID = "counter". You can change that to what ever you want. 
        var counter = document.getElementById("counter");
        var current_minutes = mins-1
        seconds--;
        if (current_minutes == 0 && seconds == 0){
            form.submit();
        }
        counter.innerHTML = current_minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
        document.title = "CHallenger " + current_minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
        
        if( seconds > 0 ) {
            setTimeout(tick, 1000);
        } else {
            if(mins > 1){
                countdown(mins-1);           
            } 
        }
        
        
    }
    tick();
}

function submitForm(){
    var form = document.getElementById("test");
    form.submit()
}

window.addEventListener('blur', submitForm);

window.addEventListener("onunload", submitForm);