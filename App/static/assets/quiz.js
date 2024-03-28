var currentQuestion = 0;
var totalQuestions = 0;
var timerInterval;
var timeLeft = 60; // Set timer duration in seconds


function displayQuestion() {
    // console.log(quizData.questions[currentQuestion]);
    document.getElementById('question-container').innerHTML = currentQuestion+1+'. '+ quizData.questions[currentQuestion].content ;
    var optionsHtml = '';
    quizData.questions[currentQuestion].options.forEach(function (option) {
        optionsHtml +=
            '<div class="form-check"><input class="form-check-input" type="checkbox" value="' + option +
            '" id="' + option + '"><label class="form-check-label" for="' + option + '">' + option +
            '</label></div>';
    });
    document.getElementById('option-container').innerHTML = optionsHtml;
}

function nextQuestion() {
    currentQuestion++;
    if (currentQuestion >= totalQuestions) {
        currentQuestion = totalQuestions - 1;
        displayResult();
    } else {
        displayQuestion();
    }
}

function prevQuestion() {
    currentQuestion--;
    if (currentQuestion < 0) {
        currentQuestion = 0;
    }
    displayQuestion();
}

function submitQuiz() {
    clearInterval(timerInterval);
    displayResult();
}

function displayResult() {
    // Code to calculate and display result goes here
    alert('Quiz submitted!');
}

function updateTimer() {
    document.getElementById('time-left').innerText = timeLeft;
    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        displayResult();
    }
    timeLeft--;
}