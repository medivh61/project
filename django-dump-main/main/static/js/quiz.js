// console.log("Hello")

const url = window.location.href
// console.log(url)
const quizBox = document.getElementById('quiz-box')

$.ajax({
    type:'GET',
    url:`${url}/data/`,
    success:function(response){
        // console.log(response)
        const data = response.data
        data.forEach(el => {
            for(const [question, answers] of Object.entries(el)){
                // console.log(question)
                // console.log(answers)
                quizBox.innerHTML +=`
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer =>{
                    quizBox.innerHTML +=`
                    <div>
                        <input type="radio" class="ans" id="${question} - ${answer}" name="${question}" value="${answer}">
                        <label for="${question}">${answer}</label>
                    </div>
                    `;
                });
                console.log('test');
            }
        });
    },
    error: function(error){
        console.log(error)
    },
});

const quizForm = document.getElementById('quiz-form')
const csrf = document.querySelector('[name=csrfmiddlewaretoken]')
const elements = [...document.querySelectorAll('.ans')]
console.log(elements)
console.log(csrf)

const sendData = () => {
    const data = {}
    data['csrfmiddlewaretoken'] = csrf.value
    elements.forEach(el =>{
        if(el.checked){
            data[el.name] = el.value
        }else{
            if(!data[el.name]){
                data[el.name] = null
            }
        }
    })
    

    $.ajax({
        type: 'POST',
        url:`${url}/save/`,
        data: data,
        success: function(response){
            console.log(response)
            console.log(data)
        },
        error: function(error){
        console.log(error)
        }
    })
}

quizForm.addEventListener('submit', e=>{
    e.preventDefault()

    sendData()
})