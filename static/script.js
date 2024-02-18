$(".submit-button").click(async function (event) {
    event.preventDefault();
    let guess = $(".guess").val()
    let answer;

    axios.post("/game", { word: guess }).then(response => {
        if (response.data.check === "ok") {
            if (response.data.correctly_guessed_words.includes(guess)) {
                answer = "Word already found."
            } else {
                answer = "Yes, it's on the board.";
                axios.post("/game", { scoreAdded: guess.length, correctlyGuessedWord: guess }).then(response => {
                    $(".current-score").text(response.data.score);
                    $(".correct-guessed-words").empty()
                    for (let x of response.data.correctly_guessed_words) {
                        $(".correct-guessed-words").append(`<li>${x}</li>`)
                    }
                }
                )
            }
        } else if (response.data.check === "not-on-board") {
            answer = "Not on the board, but it's a word.";
        } else if (response.data.check === "not-word") {
            answer = "Not even a word.";
        } else {
            answer = "Unauthorized action."
        }
        $(".current-guess").text(`Current guess = ${guess}, Response = ${answer}`)
    }).catch(error => {
        answer = "ERROR"
        $(".current-guess").text(`${answer}`);
    });
    $(".guess").val("");
})

$(".restart-button").click(async function (event){
    event.preventDefault();
    axios.post("/game", {"restart":"rightNOW"}).then(response => {location.reload()})
    })

function timer(x, asTimer, afterTimer) {
    let endTime = Math.floor((new Date().getTime()) / 1000) + x;
    asTimer(x);
    let interval = setInterval(function () {
        let amtOfTimeLeft = endTime - Math.floor((new Date().getTime()) / 1000);
        if (amtOfTimeLeft > 0) {
            asTimer(amtOfTimeLeft);
        } else {
            asTimer(amtOfTimeLeft);
            clearInterval(interval);
            afterTimer();
        }
    }
        , 1000)
}

axios.post("/game", { "endTime": "None" }).then(response => {
    if (response.data.endTime - Math.floor((new Date().getTime()) / 1000) > 0) {
        let endTime = response.data.endTime;
        let totalTimeLeft = endTime - Math.floor((new Date().getTime()) / 1000)
        if (totalTimeLeft > 60){
            totalTimeLeft = 60;
        }
        timer(totalTimeLeft, timeLeft => {
            $(".timer").text(timeLeft);
        }, () => {
            $(".timer").text("Finished!")
            $(".guess").prop("disabled", true);
            $(".submit-button").prop("disabled", true);
            axios.post("/game", { "endTime": "Finished!" }).then(response =>{
                if (response.data.score > response.data.high_score){
                    $(".high-score-alert").text("New High Score!");
                }
            });
        });
    } else {
        $(".timer").text("Finished!");
        $(".guess").prop("disabled", true);
        $(".submit-button").prop("disabled", true);
        axios.post("/game", { "endTime": "Finished!" }).then(response =>{
            if (response.data.score > response.data.high_score){
                $(".high-score-alert").text("New High Score!");
            }
        });
    }
})