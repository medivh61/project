
const url = window.location.href
// console.log(url)
const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')

const activateTimeer = (time) => {
    // console.log(time)

    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(() => {
        seconds--
        if (seconds < 0) {
            seconds = 59
            minutes--
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes
        } else {
            displayMinutes = minutes
        }

        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(() => {
                clearInterval(timer)
                alert('Время вышло')
                sendData()
            },500)
        }
        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}

$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function (response) {
        // console.log(response)
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
                // console.log(question)
                // console.log(answers)
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                    <div>
                        <input type="radio" class="ans" id="${question} - ${answer}" name="${question}" value="${answer}">
                        <label for="${question}">${answer}</label>
                    </div>
                    `;
                });
                console.log('test');
            }
        });
        activateTimeer(response.time)
    },
    error: function (error) {
        console.log(error)
    },
})

const quizForm = document.getElementById('quiz-form')

const sendData = () => {
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]')
    const elements = [...document.querySelectorAll('.ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf.value

    console.log(elements)
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}/save/`,
        data: data,
        success: function (response) {
            // console.log(response)
            // console.log(data)
            const results = response.results
            console.log(results)

            // quizForm.classList.add('invisible')
            document.getElementById("timer-box").remove()
            document.getElementById("quiz-box").remove()
            document.getElementById("button_save").remove()
            // const newDiv = document.createElement("div");
            // para.innerHTML = someHere;

            scoreBox.innerHTML = `<h6>${response.passed ? 'Поздравляю! Вы прошли тест.' : 'К сожалению, вы не прошли тест.'} Ваш результат ${response.score.toFixed(2)}%</h6>`

            results.forEach(res => {
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)) {
                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'text-light', 'h5']
                    resDiv.classList.add(...cls)

                    if (resp == 'not answered') {
                        resDiv.innerHTML += ' - Нет ответа'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` Ответ: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | Правильный ответ:  ${correct}`
                            resDiv.innerHTML += ` | Ваш ответ:  ${answer}`
                        }
                    }
                }
                // const body = document.getElementsByTagName('BODY')[0]
                resultBox.append(resDiv)
                // document.getElementById("BODY").appendChild(resDiv);
            })
        },
        error: function (error) {
            console.log(error)
        }
    })
}

quizForm.addEventListener('submit', e => {
    e.preventDefault()

    sendData()
})