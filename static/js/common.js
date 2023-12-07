
function checkLoginStatus() {
    fetch('/api/check_login_status', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        const loginSignupElement = document.getElementById('logout')
        const logoutElement = document.getElementById('login-signup')

        if (data.isLoggedIn) {
            loginSignupElement.style.display ='inline-block'
            logoutElement.style.display = 'none';
        } else {
            loginSignupElement.style.display ='none'
            logoutElement.style.display = 'inline-block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

