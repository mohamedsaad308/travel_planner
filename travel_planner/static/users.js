// document.querySelectorAll('.edit-user').forEach(element => {
//     element.onclick = () => console.log(element.value)
//     }
// )
let userID;
var csrf_token = "{{ csrf_token() }}";
function getID(id) {
    userID = id;
    console.log(userID);
}

console.log(userID)
// #when submiting the edit user form 
function edit_user() {
    // const emailField = querySelector(`#email-${userID}`);
    // const firstNameField =  querySelector(`#first-name-${userID}`);
    // const lastNameField =  querySelector(`#last-name-${userID}`);
    const email = document.querySelector('#email');
    const firstName = document.querySelector('#first_name');
    const lastName = document.querySelector('#last_name');

    const userToEdit = {
        'email' : email.value,
        'first_name' : firstName.value,
        'last_name' : lastName.value
    }

    fetch(`/users/${userID}`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(userToEdit),
        cache: 'no-cache',
        headers : new Headers({
            "content-type" : "application/json",
            'X-CSRFToken': csrf_token
        })
    }).then(function (response) {
        // console.log(response);
        return response.json();
    }).then(function (jsonResponse) {
        console.log(jsonResponse);
        if (jsonResponse.error) {
            console.log(jsonResponse.error);
            document.getElementById('editEmailError').textContent = 'Please enter valid email!';
        }
        else {
            console.log(jsonResponse);
        }

    })
}











// Helpful functions 
function validateEmail(email) 
    {
        var re = /\S+@\S+\.\S+/;
        return re.test(email);
    }