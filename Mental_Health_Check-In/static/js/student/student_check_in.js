document.addEventListener("DOMContentLoaded", function () {
    const questions = [
        {
            title: "1. How have you’ve been lately?",
            description: "Choose the answer that best describes your current mood.",
            options: ["Very Good", "Good", "Okay", "Not Good", "Bad"]
        },
        {
            title: "2. How often do you feel mentally and physically exhausted at the same time?",
            description: "Think about how energetic or tired you feel.",
            options: ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            title: "3. On a scale from 1 to 10, how would you rate your overall stress or tension level over the past week?",
            description: "Choose the option that best describes your stress level.",
            options: [
                "1–3: Low stress (Manageable, occasional worry)",
                "4–7: Moderate stress (Impacting focus, or daily energy)",
                "8–10: Severe stress (Overwhelming, significantly disrupting daily functioning)"
            ]
        },
        {
            title: "4. Over the last 2 weeks, how often have you been bothered by feeling nervous, anxious, on edge, or unable to stop worrying?",
            description: "Think about how you have felt over the last two weeks.",
            options: [
                "0: Not at all",
                "1: Several days",
                "2: More than half the days",
                "3: Nearly every day"
            ]
        },
        {
            title: "5. How would you describe your overall well-being this week?",
            description: "It is okay to ask for help whenever you need it.",
            options: ["Excellent", "Good", "Fair", "Poor", "Very Poor"]
        }
    ];

    let currentQuestion = 0;
    const answers = new Array(questions.length).fill("");

    const questionTitle = document.getElementById("question-title");
    const questionDescription = document.getElementById("question-description");
    const answerOptions = document.getElementById("answer-options");
    const questionCount = document.getElementById("question-count");
    const progressBar = document.getElementById("progress-bar");
    const backButton = document.getElementById("back-button");
    const nextButton = document.getElementById("next-button");
    const errorMessage = document.getElementById("error-message");

    function renderQuestion() {
        const question = questions[currentQuestion];

        questionTitle.textContent = question.title;
        questionDescription.textContent = question.description;
        questionCount.textContent =
            `Question ${currentQuestion + 1} of ${questions.length}`;

        const progress = ((currentQuestion + 1) / questions.length) * 100;
        progressBar.style.width = `${progress}%`;

        answerOptions.innerHTML = "";

        question.options.forEach(function (option) {

            const isSelected = answers[currentQuestion] === option;
            const normalBg = "#f4f5fb";
            const hoverBg = "#ecedf9";
            const selectedBg = "#e3e4fb";

            const label = document.createElement("label");
            label.className =
                "flex cursor-pointer items-center gap-4 rounded-xl px-5 py-4 transition";
            label.style.backgroundColor = isSelected ? selectedBg : normalBg;

            label.addEventListener("mouseenter", function () {
                if (answers[currentQuestion] !== option) {
                    label.style.backgroundColor = hoverBg;
                }
            });
            label.addEventListener("mouseleave", function () {
                if (answers[currentQuestion] !== option) {
                    label.style.backgroundColor = normalBg;
                }
            });

            const radio = document.createElement("input");
            radio.type = "radio";
            radio.name = "answer";
            radio.value = option;
            radio.checked = isSelected;
            radio.className = "h-5 w-5";
            radio.style.accentColor = "#272263";

            radio.addEventListener("change", function () {
                answers[currentQuestion] = option;
                errorMessage.classList.add("hidden");
                renderQuestion();
            });

            const text = document.createElement("span");
            text.className = "text-base " + (isSelected ? "font-semibold" : "font-medium");
            text.style.color = "#1f1f5c";
            text.textContent = option;

            label.appendChild(radio);
            label.appendChild(text);
            answerOptions.appendChild(label);
        });

        
        backButton.disabled = currentQuestion === 0;

        
        nextButton.textContent =
            currentQuestion === questions.length - 1 ? "Submit" : "Next";
    }


    nextButton.addEventListener("click", function () {

        if (!answers[currentQuestion]) {
            errorMessage.classList.remove("hidden");
            return;
        }

        errorMessage.classList.add("hidden");

        if (currentQuestion < questions.length - 1) {
            currentQuestion++;
            renderQuestion();
        } else {
            document.getElementById("questionnaire").classList.add("hidden");
            console.log("Check-in answers:", answers);
        }
    });

    backButton.addEventListener("click", function () {
        if (currentQuestion > 0) {
            currentQuestion--;
            errorMessage.classList.add("hidden");
            renderQuestion();
        }
    });

    renderQuestion();
});