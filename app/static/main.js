function toHome(){
    window.location.replace("/");
}

//INDEX.HTML
$('.carousel').carousel({
    interval: 10000
});


//REGISTER.HTML
function validateUsername(){
    if($('.required').html() == None){
        return false;
    }else{
        return true;
    }
}


//QUIZ.HTML
$("#questions").ready(loadQuestion);
var current_q;
var questions;
var quiz_title;
var answers = [];

function loadQuestion(){
    questions = $("#questions").children();

    for(i = 1; i < questions.length; i++){
        $(questions[i]).addClass("question-hidden");
    }

    current_q = 1;

    quiz_title = $("#quiz-title").html();
    var message = quiz_title + ": Question " + current_q + " of " + questions.length;
    $("#quiz-title").html(message);

    if(questions.length == 1){
        $("#nextQuestionButton").attr('value', 'Submit');
        $("#nextQuestionButton").attr('onclick', 'submitQuiz()');
    }
}

function nextQuestion(){

    var answer = $(questions[current_q-1]).find('input').val();
    answers.push(answer);

    current_q += 1;

    if(current_q == questions.length){
        //Final question
        $("#nextQuestionButton").attr('value', 'Submit');
        $("#nextQuestionButton").attr('onclick', 'submitQuiz()');
    }else if(current_q == 2){
        $("#prevQuestionButton").removeClass("hidden");
    }

    var message = quiz_title + ": Question " + current_q + " of " + questions.length;
    $("#quiz-title").html(message);

    $(questions[current_q-2]).removeClass("question-visible");
    $(questions[current_q-2]).addClass("question-hidden");
    $(questions[current_q-1]).removeClass("question-hidden");
    $(questions[current_q-1]).addClass("question-visible");

}

function prevQuestion(){
    current_q -= 1;

    if(current_q == 1){
        //Going back to first question
        $("#prevQuestionButton").addClass("hidden");
    }

    var message = quiz_title + ": Question " + current_q + " of " + questions.length;
    $("#quiz-title").html(message);

    $(questions[current_q-1]).removeClass("question-hidden");
    $(questions[current_q-1]).addClass("question-visible");
    $(questions[current_q]).removeClass("question-visible");
    $(questions[current_q]).addClass("question-hidden");
}

function handleMarking(data){
    console.log(data);
}

function submitQuiz(){
    var answer = $(questions[current_q-1]).find('input').val();
    answers.push(answer);

    //Handle submit form
    jsonResults = [{"title": quiz_title}];

    for(i = 0; i < answers.length; i++){
        jsonResults.push({
            "question": $(questions[i]).find('p').html(),
            "answer": answers[i]
        });
    }

    //result = $.post( "/submit_quiz", JSON.stringify(jsonResults));

    post_quiz(jsonResults);

    
    $("#prevQuestionButton").addClass("hidden");
    $("#nextQuestionButton").addClass("hidden");

}

function post_quiz(results){
    $.ajax({
        type: "POST",
        url: "/submit_quiz",
        data: JSON.stringify(results),
        contentType: "text/json; charset=utf-8",
        dataType: "text",
        success: function (msg) {            
            handleFeedback(msg);
        }
    });
}

function handleFeedback(data){
    $("#feedback-div").removeClass("hidden");

    data = JSON.parse(data);

    for (var key in data){
        if (key != 'score'){
            var style;

            if(data[key][0] != data[key][1]){
                style = "background-color: rgba(219, 76, 76, 0.2);"
            }else{
                style = "background-color: rgba(85, 219, 76, 0.2);"
            }

            var new_row = "<tr style='"+style+"'><td>"+key+"</td><td>"+data[key][0]+"</td><td>"+data[key][1]+"</td></tr>";
            $("#feedback").append(new_row);
        }
    };

    var score = "<p>Well done! You scored "+data['score'][0]+" out of "+data['score'][1]+".</p>"

    $("#feedback-div").append(score);
}


//RESULT.HTML

const labels = [];
const dataPoints = [];

function addData(user_data){
    json = JSON.parse(user_data);
    
    for(var i = 0; i < json.length; i++){
        for (var key in json[i]){
            dataPoints.push(key);
            labels.push(json[i][key]);
        }
    }  

    const data = {
        labels: labels,
        datasets: [{
            label: 'Scores Over Time',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: dataPoints,
        }]
    };
    
    const config = {
        type: 'line',
        data,
        options: {}
    };

    var myChart = new Chart(
        document.getElementById("myChart").getContext("2d"),
        config
      );
}

$("#results-table").ready(drawResults);

function drawResults(){
    if($("#myChart").length > 0 ){
        $.get('get_results_json', addData);
    }
}