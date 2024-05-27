const base_url = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", (event) => {
    const signUpButton = document.getElementById("signUp");
    const signInButton = document.getElementById("signIn");
    const container = document.getElementById("container");
    const signUpContainer = document.getElementById("signUpContainer");
    const signInContainer = document.getElementById("signInContainer");

    signUpButton.addEventListener("click", () => {
        container.classList.add("right-panel-active");
        signInContainer.classList.remove("active");
        signUpContainer.classList.add("active");
    });

    signInButton.addEventListener("click", () => {
        container.classList.remove("right-panel-active");
        signUpContainer.classList.remove("active");
        signInContainer.classList.add("active");
    });

    // Initially display the sign-in container
    signInContainer.classList.add("active");
});

const signupForm = document.getElementById("sign-up");
async function SignUp() {
    var data = {
        username: document.getElementById("username").value,
        firstname: document.getElementById("firstname").value,
        lastname: document.getElementById("lastname").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
    };
    try {
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        const response = await fetch(base_url + "/api/registration", {
            method: "POST",
            body: JSON.stringify(data),
            headers: myHeaders,
        });
        const result = await response.json()
        console.log(result);
        if (!response.ok) {
            throw new Error(result.error);
        }
        window.location.href = '/';
    } catch (e) {
        console.error(e);
        document.getElementById("error").innerHTML = e;
        document.getElementById("error").style.backgroundColor = "#fbeaea";
        signupForm.reset();
    }
}

signupForm.addEventListener("submit", (event) => {
    event.preventDefault();
    SignUp();
});

const LoginForm = document.getElementById("sign-in");
async function LogIn() {
    var prevURL = window.location.href;
    var data = {
        username: document.getElementById("name").value,
        password: document.getElementById("pwd").value,
    };
    try {
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        const response = await fetch(base_url + "/api/login", {
            method: "POST",
            body: JSON.stringify(data),
            headers: myHeaders,
        });
        console.log(await response.json());
        if (!response.ok) {
            throw new Error("Invalid Credentials");
        }
        var parsedUrl = new URL(prevURL)
        var params = new URLSearchParams(parsedUrl.search);
        if (params.has('next')) {
            var nextValue = params.get('next');
            window.location.href = nextValue;
        }
        window.location.href = '/';
    } catch (e) {
        console.error(e);
        document.getElementById("login_error").innerHTML = e;
        document.getElementById("login_error").style.backgroundColor = "#fbeaea";
        LoginForm.reset();
    }
}

LoginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    LogIn();
});