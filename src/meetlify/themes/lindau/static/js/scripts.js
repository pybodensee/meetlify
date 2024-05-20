/*!
* Start Bootstrap - Modern Business v5.0.7 (https://startbootstrap.com/template-overviews/modern-business)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-modern-business/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

//JavaScript
const handleSubmit = (event) => {
    event.preventDefault();

    const myForm = event.target;
    const formData = new FormData(myForm);

    fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(formData).toString(),
    })
        .then(() => document.querySelector("#submitSuccessMessage").classList.replace("d-none", "d-show"))
        .catch((error) => document.querySelector("#submitErrorMessage").classList.replace("d-none", "d-show"));
};

try {
    document
        .querySelector("form")
        .addEventListener("submit", handleSubmit);
} catch (error) {
}