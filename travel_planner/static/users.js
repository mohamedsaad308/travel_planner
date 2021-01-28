// document.querySelectorAll('.edit-user').forEach(element => {
//     element.onclick = () => console.log(element.value)
//     }
// )
let userID;

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
    const email = querySelector('#email');
    const firstName = querySelector('#first_name');
    const lastName = querySelector('#last_name');
    
    const userToEdit = {
        'email' : email.value,
        'first_name' : firstName.value,
        'last_name' : lastName.value
    }
    console.log(`/users/${userID}`)
    fetch(`/users/${userID}`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(userToEdit),
        cache: 'no-cache',
        headers : new Headers({
            "content-type" : "application/json"
        })
    })
}
