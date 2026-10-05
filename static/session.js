const SESSION_TIMEOUT = 45000;

let logoutTimer;

let lastActivitySent = 0;


// ============================================================
// RESET TIMER
// ============================================================

function resetTimer() {

    clearTimeout(logoutTimer);

    logoutTimer = setTimeout(
        sessionTimedOut,
        SESSION_TIMEOUT
    );

    updateServerActivity();
}


// ============================================================
// INFORM SERVER THAT USER IS ACTIVE
// ============================================================

function updateServerActivity() {

    const currentTime = Date.now();

    /*
        Prevent sending hundreds of requests
        while the mouse is moving.

        Activity is sent to the server at most
        once every 5 seconds.
    */

    if (
        currentTime - lastActivitySent < 5000
    ) {
        return;
    }

    lastActivitySent = currentTime;


    fetch(
        "/activity",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            }
        }
    )
    .then(response => {

        if (response.status === 401) {

            window.location.href =
                "/login";

        }

    })
    .catch(error => {

        console.log(
            "Activity update failed:",
            error
        );

    });

}


// ============================================================
// SESSION TIMEOUT
// ============================================================

function sessionTimedOut() {

    fetch(
        "/session-expired",
        {
            method: "POST"
        }
    )
    .finally(() => {

        alert(
            "Session timed out"
        );

        window.location.href =
            "/login";

    });

}


// ============================================================
// USER ACTIVITIES
// ============================================================

const activityEvents = [

    "mousedown",
    "mousemove",
    "keydown",
    "scroll",
    "touchstart",
    "click"

];


// ============================================================
// ADD EVENT LISTENERS
// ============================================================

activityEvents.forEach(eventName => {

    document.addEventListener(
        eventName,
        resetTimer,
        true
    );

});


// ============================================================
// START TIMER
// ============================================================

resetTimer();